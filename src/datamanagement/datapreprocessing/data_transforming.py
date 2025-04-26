import pandas as pd
from collections import Counter
import os
import gc
import torch
from transformers import pipeline
import spacy
from dotenv import load_dotenv

load_dotenv()
os.environ['CUDA_LAUNCH_BLOCKING'] = '1'
def create_features_from_pretrained_models(
                        model_configuration: dict,
                        df: pd.DataFrame,
                        columns: list
                        ) -> pd.DataFrame:
    """ Generate features from the pretrained models for the specified columns
    in the given dataframe and return DataFrame

    Arguments:
        - model_configuration: a dict in which the key stats the feature to be
            extracted values of model parameters in a dict
        - df: a pandas.DataFrame on which the data is stored
        - columns: the features on which the models to be used

    Returns:
        - pd.DataFrame: A dataframe with updated features
    """
    def retrieve_model_response(text: str) -> str:
        """ Generate the model response from the given text and return result
        generated

        Arguments:

            - text: a text to generate the model response

        Returns:

            - str: a response of the model generated

        """
        if not isinstance(text, str):
            text = " "
        if text is None:
            text = " "
        results = pipe(text)
        if len(results) <= 0:
            return " "

        try:
            label = results[0].get("label")
        except Exception as oops:
            print(f"Error occurred while retrieve_model_response as {oops}")
            label = "None"
        return label

    # All the features to be used
    for column in columns:
        # Model configuration with model parameters
        for key, value in model_configuration.items():
            # Prefix to be stored as feature in the dataframe
            column_prefix = f"{column}_{key}"
            # Initiate with the None
            df[column_prefix] = "None"
            try:
                # set the model configuration
                pipe = pipeline(**value)
                df[column_prefix] = df[column].apply(retrieve_model_response)

                # Delete the unused variables and Empty the cuda cache
                # to optimize the system
                del pipe
                gc.collect()
                torch.cuda.empty_cache()
            except Exception as oops:
                print(f"error in {df[column_prefix]}")
                print(f"Error occurred while extracting feature as {oops}")
    return df


def retrieve_counts_on_part_of_speech(df: pd.DataFrame,
                                      columns: list) -> pd.DataFrame:
    """ Retrieve the counts on part of speech of for all the features given 
    dataframe. Return a pandas dataframe with the updated features of part 
    of speech
    
    Arguments: 
        - df: a pandas Dataframe
        - columns: a list of features on which the part of speech is
          to be applied

    Returns: 
        - Dataframe: with updated features of part of speech 

    """

    def count_part_of_speech(text: str) -> Counter:
        """ Calculates the part of speech for the given text

        Arguments: 
            - text: a str to count the part of speech

        Returns: 
            - Counter: a value counts of part of speech 
        """
        tokens = nlp(str(text))
        pos_counts = dict(Counter([token.pos_ for token in tokens]))
        return pos_counts

    def search_all_organization(text: str) -> Counter:
        """ Calculates the organization for the given text

        Arguments: 
            - text: a str to count the part of speech

        Returns: 
            - Counter: a value counts of part of speech 
        """
        tokens = nlp(str(text))
        organizations = dict(Counter([ent.text for ent in tokens.ents if ent.label_ == "ORG"]))
        return organizations

    nlp = spacy.load("en_core_web_sm")
    for column in columns:
        df[f"{column}_pos_counts"] = df[column].apply(count_part_of_speech)
        df[f"{column}_org_counts"] = df[column].apply(search_all_organization)
    return df



# new_df = create_features_from_pretrained_models(model_configuration, df, ["article_description", "article_title"])
# new_df.to_csv("../data/transformed_data.csv",index=False)

# This is used after Load in the dbt
# transformed_df = pd.read_csv("../data/transformed_data.csv")
# nlp_df = retrieve_counts_on_part_of_speech(
#             df=transformed_df,
#             columns=["article_content", "article_description", "article_title"]
#             )
# nlp_df.to_csv("transformation_new.csv",index=False)
# print("Hello")