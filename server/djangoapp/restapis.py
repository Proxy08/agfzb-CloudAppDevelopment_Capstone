from email.mime import image
import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview
import os
from os.path import join, dirname
from ibm_watson import AssistantV1
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, EmotionOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.fhn,j


#response = assistant.list_workspaces(headers={'Custom-Header': 'custom_value'})
# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        if "apikey" in kwargs:
            response = requests.get(url, headers={'Content-Type':'application/json'}, params=kwargs, auth=HTTPBasicAuth("apikey", kwargs["apikey"]))
        else:
            response = requests.get(url, headers={'Content-Type':'application/json'}, params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, payload, **kwargs):
    print(url)
    print(payload)
    print(kwargs)
    try:
        response = requests.post(url, params=kwargs, json=payload)
    except Exception as e:
        print("Error" ,e)
    print("Status Code ", {response.status_code})
    data = json.loads(response.text)
    return data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list

def get_dealers_from_cf(url, **kwargs):
    results = []
    print(kwargs)
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results
# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, id):
    results = []
    print(id)
    json_results = get_request(url)
    print(url)
    image = "/static/media/emoji/neutral.png" 
    if json_results:
        # Get the row list in JSON as dealers
        reviews = json_results["rows"]
        # For each dealer object
        for review in reviews:
            # Get its content in `doc` object
            review_doc = review["doc"]
            sentiment = analyze_review_sentiments(review_doc["review"])
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(name=review_doc["name"], dealership=review_doc["dealership"],
                                   review=review_doc["review"], car_model=review_doc["car_model"], car_make=review_doc["car_make"],
                                   car_year=review_doc["car_year"],
                                   purchase=review_doc["purchase"], purchase_date=review_doc["purchase_date"],sentiment= sentiment,id=review_doc["id"])
            results.append(review_obj)
        review = getReviewById(results, id) 
    return review
print('sentiment: ')
# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
def analyze_review_sentiments(text):
    API = "TssHvxUZ7WS6E1GEfOE0ty9Bjj4grbPifnmAsGLbCcJZ"
    URL = "https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/9cc94652-0fc2-4d03-9d3d-10920ff388f8"
    print('text: ')
    print(text)
    # In the constructor, letting the SDK manage the token
    authenticator = IAMAuthenticator(API)
    service = NaturalLanguageUnderstandingV1(
    version='2021-08-01',
    authenticator=authenticator)
    service.set_service_url(URL)
    response = service.analyze(
    text=text,
    features=Features(entities=EntitiesOptions(sentiment=True))).get_result()
    if(len(response['entities'])==0):
        return  "neutral"
    else:
        print(response['entities'][0]['sentiment']['label'])
        return response['entities'][0]['sentiment']['label']

# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

def getById(dealers,id):
    result = []
    result = [x for x in dealers if x.id == id]
    return result

def getReviewById(dealers,id):
    result = []
    result = [x for x in dealers if x.dealership == id]
    return result
