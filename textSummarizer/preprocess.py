
from bs4 import BeautifulSoup
import requests

def webprocess(web):

    soup = BeautifulSoup(web, features="html.parser")
    p_tags = soup.find_all('p')
    p_tags_text = [tag.get_text().strip() for tag in p_tags]
    sentence_list = [sentence for sentence in p_tags_text if not '\n' in sentence]
    sentence_list = [sentence for sentence in sentence_list if '.' in sentence]
    processed_text= ' '.join(sentence_list)

    return processed_text


def query(payload):
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }
    response = requests.post(API_URL, headers=headers, json={"inputs": payload})
    return response.json()