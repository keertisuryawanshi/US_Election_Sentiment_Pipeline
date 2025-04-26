import pandas as pd

# Load Historical and Real-time News Data
# historical_news_data = pd.read_csv("../data/historical_news_data.csv")
#realtime_news_data = pd.read_csv("../data/v1-realtime_data-news-api-2024-10-18.csv")

# Function to clean Historical News Data
def clean_historical_news(df):
    # Drop rows where all values are missing
    df.dropna(how='all', inplace=True)
    
    # replacing missing author names with "unknown"
    df['author_name'].fillna('Unknown', inplace=True)
    df['article_content'].fillna('No content available', inplace=True)
    
    # formatting the date column to datetimetype
    df['article_publishedAt'] = pd.to_datetime(df['article_publishedAt'], errors='coerce')
    
    # dropping any rows with invalid dates
    df.dropna(subset=['article_publishedAt'], inplace=True)
    
    df[["source_id", "article_description", "article_urlToImage"]] = \
        df[["source_id", "article_description", "article_urlToImage"]]\
            .fillna("No Information Available")
    # removing leading/trailing spaces from strings
    df['author_name'] = df['author_name'].str.strip()
    df['article_title'] = df['article_title'].str.strip()
    df['article_description'] = df['article_description'].str.strip()
    return df

# Function to clean Real-time News Data
# def clean_realtime_news(df):
#     # Drop rows where all values are missing
#     df.dropna(how='all', inplace=True)
    
#     # replacing missing author names with "unknown"
#     df['author_name'].fillna('Unknown', inplace=True)
#     df['article_content'].fillna('No content available', inplace=True)
    
#     # formatting the date column to datetimetype
#     df['article_publishedAt'] = pd.to_datetime(df['article_publishedAt'], errors='coerce')
    
#     # dropping any rows with invalid dates
#     df.dropna(subset=['article_publishedAt'], inplace=True)
    
#     # removing leading/trailing spaces from strings
#     df['author_name'] = df['author_name'].str.strip()
#     df['article_title'] = df['article_title'].str.strip()
#     df['article_description'] = df['article_description'].str.strip()
#     return df


# cleaned_historical_data = clean_historical_news(historical_news_data)
# #cleaned_realtime_data = clean_realtime_news(realtime_news_data)

# # saving the cleaned datasets to csv files
# cleaned_historical_data.to_csv("/cleaned_historical_news.csv", index=False)
# #cleaned_realtime_data.to_csv("cleaned_realtime_news.csv", index=False)

# print("Data cleaning complete. Cleaned data saved as CSV.")
