import sqlite3
import pandas as pd
from google.oauth2 import service_account
from pandas_gbq import to_gbq

def load_sqlite_to_bigquery(sqlite_db_path, credentials_path, project_id, dataset_id):
    """
    Load data from an SQLite database into BigQuery tables.
    
    Args:
    sqlite_db_path (str): Path to the SQLite database file.
    credentials_path (str): Path to the Google Cloud service account JSON key file.
    project_id (str): Google Cloud project ID.
    dataset_id (str): BigQuery dataset ID.
    """
    # Set up BigQuery credentials
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    
    # Connect to the SQLite database
    conn = sqlite3.connect(sqlite_db_path)
    
    # Load data from each table in SQLite into pandas DataFrames
    fact_news_df = pd.read_sql_query("SELECT * FROM FactNews", conn)
    dim_article_df = pd.read_sql_query("SELECT * FROM DimArticle", conn)
    dim_article_title_df = pd.read_sql_query("SELECT * FROM DimArticleTitle", conn)
    dim_article_description_df = pd.read_sql_query("SELECT * FROM DimArticleDescription", conn)
    dim_article_content_df = pd.read_sql_query("SELECT * FROM DimArticleContent", conn)
    
    # Close the SQLite connection
    conn.close()
    
    # Define table names for BigQuery
    fact_news_table = f"{dataset_id}.FactNews"
    dim_article_table = f"{dataset_id}.DimArticle"
    dim_article_title_table = f"{dataset_id}.DimArticleTitle"
    dim_article_description_table = f"{dataset_id}.DimArticleDescription"
    dim_article_content_table = f"{dataset_id}.DimArticleContent"
    
    # Upload DataFrames to BigQuery
    to_gbq(fact_news_df, fact_news_table, project_id=project_id, if_exists='replace', credentials=credentials)
    to_gbq(dim_article_df, dim_article_table, project_id=project_id, if_exists='replace', credentials=credentials)
    to_gbq(dim_article_title_df, dim_article_title_table, project_id=project_id, if_exists='replace', credentials=credentials)
    to_gbq(dim_article_description_df, dim_article_description_table, project_id=project_id, if_exists='replace', credentials=credentials)
    to_gbq(dim_article_content_df, dim_article_content_table, project_id=project_id, if_exists='replace', credentials=credentials)
    
    print("Data successfully loaded into BigQuery!")

# Example usage
#load_sqlite_to_bigquery('newsdb1.db', 'newsanalytics-440610-81d148518740.json', 'newsanalytics-440610', 'testnews')