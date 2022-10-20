import requests
import json
import os
from dotenv import load_dotenv
from .models import CarDealer,DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, KeywordsOptions, SentimentOptions


def get_request(url, **kwargs):
    print(kwargs)
    print("GET REQUEST FROM {}".format(url))
    try:
        if "apikey" in kwargs.keys():
            
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]

            response = requests.get(url, 
                headers={
                    'Content-Type':'application/json'
                },
                
                 auth=HTTPBasicAuth('apikey',kwargs["apikey"]),
                 params=params
            )
        else:
            response = requests.get(url,headers={
                'Content-Type':'application/json'
            },
                params=kwargs
            )
    except:
        print("Network error occurred")
    
    status_code = response.status_code
    print("With status {}".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def get_dealers_from_cf(url, **kwargs):
    result = []
    json_result = get_request(url)
    if json_result:
        all_dealers = json_result["result"]
        for dealer in all_dealers:
            dealer_doc = dealer["doc"]
            new_car_dealer = CarDealer(address=dealer_doc["address"],
                            city=dealer_doc["city"],full_name=dealer_doc["full_name"],
                            id=dealer_doc["id"], lat=dealer_doc["lat"],long=dealer_doc["long"],
                            short_name=dealer_doc["short_name"],st=dealer_doc["st"],
                            state=dealer_doc["state"],zip=dealer_doc["zip"])
            result.append(new_car_dealer)
    
    return result

def get_dealers_by_state(url,state):
    result = []
    json_result = get_request(url, state=state)
    if json_result:
        dealers_state = json_result["result"]
        for dealer in dealers_state:
            new_dealer = CarDealer(address=dealer["address"],
                            city=dealer["city"],full_name=dealer["full_name"],
                            id=dealer["id"], lat=dealer["lat"],long=dealer["long"],
                            short_name=dealer["short_name"],st=dealer["st"],
                            state=dealer["state"],zip=dealer["zip"])
            result.append(new_dealer)
    
    return result

def get_dealer_by_id(url,id):
    result = []
    json_result = get_request(url, id=id)
    if json_result:
        dealers_id = json_result["result"]
        for dealer in dealers_id:
            new_dealer = CarDealer(address=dealer["address"],
                            city=dealer["city"],full_name=dealer["full_name"],
                            id=dealer["id"], lat=dealer["lat"],long=dealer["long"],
                            short_name=dealer["short_name"],st=dealer["st"],
                            state=dealer["state"],zip=dealer["zip"])
            result.append(new_dealer)
    
    return result

def get_dealer_reviews_from_cf(url, dealerId):
    result = []
    json_data = get_request(url, dealerId=dealerId)
    if json_data:
        reviews = json_data["result"]
        for review in reviews:
            new_review = DealerReview(dealership=review["dealership"],
                        car_make=review["car_make"],name=review["name"],
                        purchase=review["purchase"],purchase_date=review["purchase_date"],
                        review=review["review"],car_year=review["car_year"],car_model=review["car_model"],
                        another=review.get('another'),sentiment="",id=dealerId)
            new_review.sentiment = analyze_review_sentiments(review["review"])
            result.append(new_review)
    
    return result


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(review_text):
    load_dotenv()
    authenticator = IAMAuthenticator(os.environ.get('IAM_API_KEY'))
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url(os.environ.get("SERVICE_URL"))
    response = natural_language_understanding.analyze(
            language="en",
            text=review_text,
            features=Features(sentiment=SentimentOptions())).get_result()
    
    sentiment_review = response["sentiment"]["document"]["label"]
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
    return sentiment_review

def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print("POST REQUEST FROM {}".format(url))
    try:
            response = requests.post(url,headers={
                'Content-Type':'application/json'
            },
                params=kwargs,
                json=json_payload
            )
    except:
        print("Network error occurred")
    
    status_code = response.status_code
    print("With status {}".format(status_code))
    json_data = json.loads(response.text)
    return status_code



