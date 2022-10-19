import requests
import json
from .models import CarDealer
from requests.auth import HTTPBasicAuth


def get_request(url, **kwargs):
    print(kwargs)
    print("GET REQUEST FROM {}".format(url))
    try:
        response = requests.get(url, 
            headers={
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

def get_dealer_reviews_from_cf(url, dealerId):
    result = []
    json_data = get_request(url, dealerId=dealerId)
    if json_data:
        reviews = json_data["result"]
        for review in reviews:
            new_review = DealerReview()


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



