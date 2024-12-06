import os
import pandas as pd
import rpy2.robjects as robjs
from rpy2.robjects.packages import importr
from rpy2.rinterface_lib.embedded import RRuntimeError
from .db_connector import DatabaseHandler
import logging
import time


# Configure logging
logging.basicConfig(level=logging.INFO)

class CSVLoader:
    def __init__(self, conn: object, db_handler: object, schema: str):
        """
        Initialize the CSVLoader class.

        Args:
            conn (object): Database connection object.
            schema (str): Database schema name.
        """
        self.conn = conn
        self.schema = schema
        self.db_connect = db_handler
        self.db_connector = self.db_connect.get_db_connector()
        self._load_packages()

    def _load_packages(self) -> None:
        """
        Loads the required R packages using rpy2 and sets them as instance variables.

        Raises:
            ImportError: If an error occurs while importing the R packages.
        """
        try:
            self.readr = importr('readr')
            self.base = importr('base')
            self.lubridate = importr('lubridate')
            self.ymd = self.lubridate.ymd
            self.dplyr = importr('dplyr')
        except RRuntimeError as e:
            raise ImportError(f"Failed to import R package: {e}")

    def get_table_schema(self, table_name: str) -> dict:
        """
        Retrieve column names and data types from the target database table.

        Args:
            table_name (str): Name of the table.

        Returns:
            dict: A dictionary with column names as keys and data types as values.
        """
        query = f"""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = '{self.schema}'
              AND table_name = '{table_name}';
        """
        # Execute the query
        result = self.db_connector.querySql(self.conn, query)
        
        # Extract schema information into a dictionary
        colnames = robjs.r.colnames(result)
        data = {col_name: list(result.rx2(col_name)) for col_name in colnames}
        return dict(zip(data['COLUMN_NAME'], data['DATA_TYPE']))

    def compare_and_convert_data_types(self, rdf: object, schema_dict: dict) -> object:
        """
        Compare the data frame columns with the database schema and convert columns as necessary.

        Args:
            rdf (object): R data frame to be compared and converted.
            schema_dict (dict): Dictionary containing column names and expected data types.

        Returns:
            object: The modified R data frame with converted data types.
        """
        for col_name in self.base.colnames(rdf):
            col_name = str(col_name)
            expected_type = schema_dict.get(col_name)

            if not expected_type:
                logging.warning(f"Column '{col_name}' not found in database schema. Skipping conversion.")
                continue

            try:
                if 'date' in expected_type:
                    rdf = self.dplyr.mutate(rdf, **{col_name: self.ymd(rdf.rx2(col_name))})
                elif 'int' in expected_type:
                    rdf = self.dplyr.mutate(rdf, **{col_name: self.base.as_integer(rdf.rx2(col_name))})
                logging.info(f"Converted '{col_name}' to {expected_type} format.")
            except Exception as e:
                logging.warning(f"Failed to convert '{col_name}': {e}")

        return rdf

    def load_csv_to_db(self, file_path: str, table_name: str) -> None:
        """
        Load a CSV file into the specified database table.

        Args:
            file_path (str): Path to the CSV file.
            table_name (str): Name of the database table.

        Returns:
            None
        """
        try:
            # Empty the table.
            # Load CSV into R dataframe
            rdf = self.readr.read_delim(file=file_path, delim='\t', col_types=self.readr.cols(), 
            na=robjs.r("character(0)"), progress=False)
            # Retrieve the schema from the database
            schema_dict = self.get_table_schema(table_name)
            # Convert data types
            rdf = self.compare_and_convert_data_types(rdf, schema_dict)
            # Insert data into database
            self.db_connector.insertTable(
                connection=self.conn,
                tableName=f'{self.schema}.{table_name}',
                data=rdf,
                dropTableIfExists=False,
                createTable=False,
                tempTable=False,
                progressBar=True,
                useMppBulkLoad=False
            )
            logging.info(f"Loaded data into table '{self.schema}.{table_name}'.")

        except Exception as e:
            raise RuntimeError(f"Error loading '{file_path}' into '{table_name}': {e}")

    def load_all_csvs(self, folder_path: str) -> None:
        """
        Load all CSV files from the specified folder into the database schema.

        Args:
            folder_path (str): Path to the folder containing CSV files.

        Returns:
            None
        """
        table_order = [
            'vocabulary', 
            'domain',
            'concept_class', 'concept',
            'relationship', 'concept_relationship', 'concept_ancestor',
            'concept_synonym', 'drug_strength'
        ]

        file_to_table_mapping = {
            'vocabulary.csv': 'vocabulary',
            'domain.csv': 'domain',
            'concep_class.csv': 'concept_class',
            'concept.csv': 'concept',
            'relationship.csv': 'relationship',
            'concept_relationship.csv': 'concept_relationship',
            'concept_ancestor.csv': 'concept_ancestor',
            'concept_synonym.csv': 'concept_synonym',
            'drug_strength.csv': 'drug_strength'
        }

        missing_files = []

        try:
            print("\n\nDeleting data from table before loading...\n\n")
            time.sleep(10)
            a = [self.db_connect.empty_table(self.schema, table_name) for table_name in table_order]
            time.sleep(10)
            print("\n\n Next - Inserting data...\n\n")
            time.sleep(10)
        except Exception as e:
            logging.error(f"Failed to empty table': {e}")


        self.db_connect.disable_foreign_key_checks()
        for table in table_order:
            filename = file_to_table_mapping.get(f'{table}.csv')
            if filename:
                file_path = os.path.join(folder_path, f'{table.upper()}.csv')
                if os.path.exists(file_path):
                    try:
                        self.load_csv_to_db(file_path, table)
                    except Exception as e:
                        raise RuntimeError(f"Failed to load '{filename}' into '{table}': {e}")
                else:
                    logging.warning(f"File '{filename}' not found in folder '{folder_path}'.")
                    missing_files.append(filename)
        
        self.db_connect.enable_foreign_key_checks()


        if missing_files:
            logging.warning(f"Missing files: {missing_files}")

        logging.info("All CSV files have been processed.")