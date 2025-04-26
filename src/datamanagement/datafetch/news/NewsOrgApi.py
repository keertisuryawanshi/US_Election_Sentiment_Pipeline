""" The functionalities of the newsorg api.
For further details check out 
https://newsapi.org/
"""
from newsapi import NewsApiClient
import pandas as pd
import os
from dotenv import load_dotenv
import datetime
load_dotenv()

class NewsORGAPI:

    newsapi = NewsApiClient(api_key=os.getenv("NEWS_ORG_API"))

    def _format_articles_into_list(self, all_articles: dict):
        """ Converts the json from the newsapi.org into the list.

        Arguments: 
            - all_articles: A json with all the articles information in it.

        Returns:

        Yields: 
        - tuple: The information of the article such as (source_id, source_name, author_name,
                article_title, article_description, article_urlToImage,
                article_publishedAt, article_content)
        """
        for article in all_articles:
            source = article.get("source",{})
            source_id = source.get("id", None)
            source_name = source.get("name", None)

            author_name = article.get("author", None)
            article_title = article.get("title", None)
            article_description = article.get("description", None)
            article_urlToImage = article.get("urlToImage", None)
            article_publishedAt = article.get("publishedAt", None)
            article_content = article.get("content", None)

            yield (source_id, source_name, author_name, article_title,
                article_description,article_urlToImage,article_publishedAt, article_content)
           
 
    def retrieve_past_data_for_category(self,
                                        from_date: str,
                                        categories: list) -> pd.DataFrame:
        """ Retrieve data from the api for all the categories given

        Arguments: 
            - from_date: a string of date in the format of YYYY-MM-DD
            - categories: a list of categories based on which 

        Returns:

            - Pandas DataFrame: A dataframe with news information
        
        """
        # Create the default pandas dataframe with the features
        df = pd.DataFrame(columns=["source_id", "source_name", "author_name", "article_title",
                   "article_description","article_urlToImage","article_publishedAt", "article_content"])
        try:
            # Fetch api for each category
            for each_category in categories:
                # Until Page 5 could be accessed for the Free API version
                for page in range(1, 6):
                    # Retrieve every news on the particular category
                    all_articles = self.newsapi.get_everything(q=each_category,
                                                    sources="",
                                                    domains="",
                                                    from_param=from_date,
                                                    language="en",
                                                    sort_by="relevancy",
                                                    page=page)
                    # Checks if the information are retrieved successfully
                    status = all_articles.get("status", "failed")
                    if status == "ok":
                        all_articles = all_articles.get("articles", [])
                        print(all_articles[0])
                        # articles from the api are converted to the list
                        converted_articles = list(self._format_articles_into_list(all_articles))
                        # Create a new Dataframe with converted list
                        new_df = pd.DataFrame(data=converted_articles, columns=["source_id", "source_name", "author_name", "article_title", 
                                "article_description","article_urlToImage","article_publishedAt", "article_content"])
                        # Concat the default dataframe with the new dataframe
                        df = pd.concat([df, new_df])
                    break
                break
        except Exception as oops:
            print(f"Erorr occurred as {oops}")

        return df
    
    def retrieve_real_time_data(self, categories: list) -> pd.DataFrame:
        """ Fetch data from all the categories and store it in dataframe

        Arguments: 

            - categories: A list of appropriate categories from api

        Returns:

            - pd.Dataframe: A pandas Dataframe with the latest news information

        """           
        df = pd.DataFrame(columns=["source_id", "source_name", "author_name", "article_title", 
                    "article_description","article_urlToImage","article_publishedAt", "article_content"])
        for category in categories:
            top_headlines = self.newsapi.get_top_headlines(q='',
                                                    language='en',
                                                    category=category,
                                                    page_size=100
                                                    )
            status = top_headlines.get("status", "failed")
            if status == 'ok':

                all_articles = top_headlines.get("articles", [])
                converted_articles = list(self._format_articles_into_list(all_articles))
                new_df = pd.DataFrame(data=converted_articles, columns=["source_id", "source_name", "author_name", "article_title", 
                        "article_description","article_urlToImage","article_publishedAt", "article_content"])
                df = pd.concat([df, new_df])
                print("Information stored successfully into the dataframe")
        return df


if __name__ == "__main__":
    categories =  ["business","entertainment","general","health","science","sports","technology"]
    date_30_days_ago = datetime.datetime.today() - datetime.timedelta(days=30)
    date_30_days_ago_str = date_30_days_ago.strftime("%Y-%m-%d")
    news_categories = ["Politics", "Business & Economy", "Technology", "Health",
        "Science","Sports", "Entertainment", "Environment", "Education", "World/International News",
        "Local News", "Lifestyle", "Crime & Law", "Weather", "Arts & Culture",
        "Travel", "Opinion/Editorials", "Fashion", "Real Estate", "Food & Dining",
        "History", "Social Issues", "Automotive"]
    news_api = NewsORGAPI()
    try:
        historical_df = news_api.retrieve_past_data_for_category(
                        from_date=date_30_days_ago,
                        categories=news_categories)
        historical_df.to_csv("historical_news_data.csv")
    except Exception as oops:
        print(f"Error occurred while storing historical data as {oops}")

    try:
        df = news_api.retrieve_real_time_data(categories=news_categories)
        df.to_csv("realtime.csv")
    except Exception as oops:
        print(f"Error occurred while storing realtime data as {oops}")

