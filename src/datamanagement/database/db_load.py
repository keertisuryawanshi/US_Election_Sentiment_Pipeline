import sqlite3
import pandas as pd
import uuid

def load_csv_to_dataframe(csv_file_path):
    """Load a CSV file into a pandas DataFrame."""
    return pd.read_csv(csv_file_path)

def generate_uuids(data):
    """Generate UUIDs for each required column in the DataFrame."""
    data['article_id'] = [str(uuid.uuid4()) for _ in range(data.shape[0])]
    data['article_title_id'] = [str(uuid.uuid4()) for _ in range(data.shape[0])]
    data['article_description_id'] = [str(uuid.uuid4()) for _ in range(data.shape[0])]
    data['article_content_id'] = [str(uuid.uuid4()) for _ in range(data.shape[0])]
    return data

def create_sqlite_connection(db_name):
    """Create or connect to a SQLite database."""
    return sqlite3.connect(db_name)

def create_tables(cursor):
    """Create tables in the SQLite database."""
    cursor.execute('DROP TABLE IF EXISTS FactNews')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS FactNews (
            article_id TEXT PRIMARY KEY,
            source_id VARCHAR(50),
            source_name VARCHAR(100),
            author_name VARCHAR(100)
        );
    ''')
    
    cursor.execute('DROP TABLE IF EXISTS DimArticle')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS DimArticle (
            article_id TEXT PRIMARY KEY,
            article_title_id TEXT,
            article_description_id TEXT,
            article_content_id TEXT,
            article_urlToImage VARCHAR(500),
            article_publishedAt DATETIME,
            FOREIGN KEY(article_title_id) REFERENCES DimArticleTitle(article_title_id),
            FOREIGN KEY(article_description_id) REFERENCES DimArticleDescription(article_description_id),
            FOREIGN KEY(article_content_id) REFERENCES DimArticleContent(article_content_id)
        );
    ''')
    
    cursor.execute('DROP TABLE IF EXISTS DimArticleTitle')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS DimArticleTitle (
            article_title_id TEXT PRIMARY KEY,
            article_title VARCHAR(500),
            article_title_pos_counts JSON
        );
    ''')
    
    cursor.execute('DROP TABLE IF EXISTS DimArticleDescription')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS DimArticleDescription (
            article_description_id TEXT PRIMARY KEY,
            article_description TEXT,
            article_description_pos_counts JSON
        );
    ''')
    
    cursor.execute('DROP TABLE IF EXISTS DimArticleContent')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS DimArticleContent (
            article_content_id TEXT PRIMARY KEY,
            article_content TEXT,
            article_content_pos_counts JSON
        );
    ''')

def insert_data(cursor, table_name, data_frame, columns):
    """Insert data from a DataFrame into the specified table."""
    for _, row in data_frame.iterrows():
        placeholders = ', '.join(['?'] * len(columns))
        cursor.execute(f'''
            INSERT INTO {table_name} ({', '.join(columns)})
            VALUES ({placeholders})
        ''', tuple(row[col] for col in columns))

def create_and_insert_to_db(data, db_name="newsdb"):
    """ Create and insert to the database """
    # Load and process data
    data = generate_uuids(data)

    # Create data frames for different tables
    fact_news_df = data[['article_id', 'source_id', 'source_name', 'author_name']].drop_duplicates()
    dim_article_df = data[['article_id', 'article_title_id', 'article_description_id', 'article_content_id', 'article_urlToImage', 'article_publishedAt']].drop_duplicates()
    dim_article_title_df = data[['article_title_id', 'article_title', 'article_title_pos_counts']].drop_duplicates()
    dim_article_description_df = data[['article_description_id', 'article_description', 'article_description_pos_counts']].drop_duplicates()
    dim_article_content_df = data[['article_content_id', 'article_content', 'article_content_pos_counts']].drop_duplicates()

    try:
        # Connect to SQLite and create tables
        conn = create_sqlite_connection(f'{db_name}.db')
        cursor = conn.cursor()
        create_tables(cursor)

        # Insert data
        insert_data(cursor, 'FactNews', fact_news_df, ['article_id', 'source_id', 'source_name', 'author_name'])
        insert_data(cursor, 'DimArticle', dim_article_df, ['article_id', 'article_title_id', 'article_description_id', 'article_content_id', 'article_urlToImage', 'article_publishedAt'])
        insert_data(cursor, 'DimArticleTitle', dim_article_title_df, ['article_title_id', 'article_title', 'article_title_pos_counts'])
        insert_data(cursor, 'DimArticleDescription', dim_article_description_df, ['article_description_id', 'article_description',  'article_description_pos_counts'])
        insert_data(cursor, 'DimArticleContent', dim_article_content_df, ['article_content_id', 'article_content', 'article_content_pos_counts'])
    except Exception as oops:
        print("Error occurred while inserting the table as ", oops)
        return False

    # Commit and close the connection
    conn.commit()
    conn.close()
    print("Data successfully loaded into the SQLite database!")
    return True