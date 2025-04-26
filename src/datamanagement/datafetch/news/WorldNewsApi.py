""" The functionalities of the WorldNewsAPI
For further details check out https://worldnewsapi.com
"""

import pandas as pd
import os
import requests
from dotenv import load_dotenv
import datetime
import time

load_dotenv()

class WorldNewsAPI:

    WORLD_NEWS_API = os.getenv("WORLD_NEWS_API")
    HEADERS = {
        'x-api-key': WORLD_NEWS_API
    }
    def _format_articles_into_list(self, top_news: dict):
        """ Converts the json from the worldnewsapi.org into the list.

        Arguments: 
            - top_news: A json with all the articles information in it.

        Returns:

        Yields: 
        - tuple: The information of the article such as (source_id, source_name, author_name,
                article_title, article_description, article_urlToImage,
                article_publishedAt, article_content)
        """
        for news in top_news:
            for article in news['news']:
                source_id = article.get("id", None)
                source_name = article.get("author", None)
                author_name = article.get("authors", [None])[0]
                article_title = article.get("title", None)
                article_description = article.get("summary", None)
                article_urlToImage = article.get("image", None)
                article_publishedAt = article.get("publish_date", None)
                article_content = article.get("text", None)

                yield (source_id, source_name, author_name, article_title, 
                            article_description,article_urlToImage,article_publishedAt, article_content)

    def _format_historic_news_into_list(self, top_news: dict):
        """ Converts the json from the worldnewsapi.org into the list.

        Arguments: 
            - top_news: A json with all the articles information in it.

        Returns:

        Yields: 
        - tuple: The information of the article such as (source_id, source_name, author_name,
                article_title, article_description, article_urlToImage,
                article_publishedAt, article_content)
        """
        for article in top_news['news']:
            source_id = article.get("id", None)
            article_title = article.get("title", None)
            article_content = article.get("text", None)
            article_description = article.get("summary", None)
            article_urlToImage = article.get("image", None)
            article_publishedAt = article.get("publish_date", None)
            author_name = article.get("authors", [None])[0]
            source_name = article.get("url", None)
            category = article.get("category", None)
            sentiment = article.get("sentiment", None)
            yield (source_id, source_name, author_name, article_title, 
                   article_description,article_urlToImage,article_publishedAt,
                   article_content, category, sentiment)


    def retrieve_real_time_data(self,
                         country_codes: list,
                         language_code: str = "en") -> pd.DataFrame:
        """ Fetch data from all the categories and store it in dataframe

        Arguments: 

            - country_codes: A list of appropriate categories from api
            - language_code: an appropriate language_code to get the news on

        Returns:

            - pd.Dataframe: A pandas Dataframe with the latest news information

        """
        # Create the default pandas dataframe with the features
        df = pd.DataFrame(columns=["source_id", "source_name", "author_name", "article_title",
                 "article_description","article_urlToImage","article_publishedAt", "article_content"])
        # Get the current date in YYYY-MM-DD format
        current_date = datetime.datetime.today().strftime("%Y-%m-%d")
        try:
            # Retrieval of data for specific country
            for country_code in country_codes:
                url = f"https://api.worldnewsapi.com/top-news?source-country={country_code}&language={language_code}&date={current_date}"
                # Make the api call the get the real time news data
                response = requests.get(url, headers=self.HEADERS, timeout=10)
                # Whether the response is successful
                if response.status_code == 200:
                    # news data in json format
                    data = response.json()
                    top_news = data.get("top_news", [])
                    # articles from the api are converted to the list
                    converted_articles = list(self._format_articles_into_list(top_news))
                    # Create a new Dataframe with converted list
                    new_df = pd.DataFrame(data=converted_articles, 
                            columns=["source_id", "source_name", "author_name", "article_title",
                            "article_description","article_urlToImage","article_publishedAt",
                             "article_content"])
                    # Concat the default dataframe with the new dataframe
                    df = pd.concat([df, new_df])
        except Exception as oops:
            print(f"Error occurred while retrieval of real time data as {oops}")
        return df

    def retrieve_historical_data(self,
                                 categories: list = ["politics"],
                                 start_date: str = "2024-10-05",
                                 end_date: str = "2024-11-05",
                                 offset: int = 0,
                                 n_post = None
                                 ) -> bool:
        """ Retrieve Historical Data from for the category and date given"""
        df = pd.DataFrame(columns=["source_id", "source_name", "author_name", "article_title",
                                   "article_description", "article_urlToImage","article_publishedAt",
                                   "article_content", "article_category", "article_sentiment"])
        for category in categories:
            print("Scraping the data of the current category ", category)
            url = "https://api.worldnewsapi.com/search-news?"
            url += f"categories={category}&language=en&earliest-publish-date={start_date}"
            url += f"&number=100&source-country=us&latest-publish-date={end_date}"

            response = requests.get(url, headers=self.HEADERS)
            if response.status_code != 200 or float(response.headers.get("X-API-Quota-Left", 0)) <= 2:
                print(f"Error: {response.status_code}")
                return df

            data = response.json()
            # articles from the api are converted to the list
            converted_articles = list(self._format_historic_news_into_list(data))

            available_posts = data.get("available", 0)
            print(available_posts, " available_posts")
            if available_posts <= 100:
                # Create a new Dataframe with converted list
                new_df = pd.DataFrame(data=converted_articles, 
                        columns=["source_id", "source_name", "author_name", "article_title",
                                "article_description", "article_urlToImage","article_publishedAt",
                                "article_content", "article_category", "article_sentiment"])
                # Concat the default dataframe with the new dataframe
                df = pd.concat([df, new_df])

                continue

            if (n_post is not None ) and (n_post <= available_posts):
                available_posts = n_post
            print(f"The available_news is {available_posts}")
            for num in range(100, int(available_posts), 100):
                print(f"Current offset is {num}")
                time.sleep(1)

                offset_url = url + f"&offset={num}"
                response = requests.get(offset_url, headers=self.HEADERS)
                if response.status_code != 200 or float(response.headers.get("X-API-Quota-Left",0)) <= 2:
                    print(f"Error: {response.status_code}")
                    return df
                
                data = response.json()
                converted_articles = list(self._format_historic_news_into_list(data))

                new_df = pd.DataFrame(data=converted_articles, 
                        columns=["source_id", "source_name", "author_name", "article_title",
                                "article_description", "article_urlToImage","article_publishedAt",
                                "article_content", "article_category", "article_sentiment"])
                # Concat the default dataframe with the new dataframe
                df = pd.concat([df, new_df])

        return df

    # data = (my_custom_function())
if __name__ == "__main__":
    country_codes_based_on_continents = ["ke", "ng", "cn", "in",
                                        "ru", "de", "uk", "ca", "us",
                                        "ir", "jp", "tw", "sg" ]
    world_news_api = WorldNewsAPI()
    # try:
    #     realtime_data = world_news_api.retrieve_real_time_data(
    #                                              country_codes=country_codes_based_on_continents,
    #                                              language_code="en"
    #                                              )
    #     realtime_data.to_csv("realtime_world_news.csv")
    # except Exception as oops:
    #     print(f"Error occurred while storing historical data as {oops}")

    date_30_days_ago = datetime.datetime.today() - datetime.timedelta(days=31)
    date_30_days_ago_str = date_30_days_ago.strftime("%Y-%m-%d")

    try:
        realtime_data = world_news_api.retrieve_historical_data(start_date="2024-10-05")
        realtime_data.to_csv("../data/realtime_world_news.csv")
    except Exception as oops:
        print(f"Error occurred while storing historical data as {oops}")
