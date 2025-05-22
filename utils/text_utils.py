import re
import string


def clean_text(text):
    """
    Basic text cleaning function for preprocessing input strings.

    Steps:
        - Convert text to lowercase
        - Remove URLs (http, https, www)
        - Remove mentions (@username) and hashtags (#)
        - Remove punctuation
        - Remove numeric digits
        - Remove extra whitespace

    Args:
        text (str): The input string to clean.

    Returns:
        str: The cleaned version of the input text.
    """
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", '', text)
    text = re.sub(r'\@\w+|\#','', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text