#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#

"""
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests


def main(dict):
    databaseName = "dealerships"

    try:
        client = Cloudant.iam(
            account_name=dict["COUCH_USERNAME"],
            api_key=dict["IAM_API_KEY"],
            connect=True,
        )
        print("Databases: {0}".format(client.all_dbs()))
    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return {"dbs": client.all_dbs()}
"""
import os
import uuid
from dotenv import load_dotenv
from ibmcloudant.cloudant_v1 import CloudantV1,Document
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

load_dotenv()
API_KEY = os.environ.get("IAM_API_KEY")
URL = os.environ.get("URL")

def get_all_dbs():
    authenticator = IAMAuthenticator(API_KEY)
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(URL)    

    response = service.get_all_dbs().get_result()
    
    return {"dbs": response}



def get_all_reviews():
    authenticator = IAMAuthenticator(API_KEY)
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(URL)  
    response = service.post_all_docs(
            db='reviews',
            include_docs=True,
            ).get_result()

    return response

def get_review_by_id(dealer_id):
    all_reviews = get_all_reviews()
    reviews_by_id = []
    for review in all_reviews["rows"]:
        if review["doc"]["dealership"] == int(dealer_id):
            reviews_by_id.append(review["doc"])
    
    for review in reviews_by_id:
        del review['_id']
        del review['_rev']
    
    return reviews_by_id

def post_review(args):
    authenticator = IAMAuthenticator(API_KEY)
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(URL) 
    retrieve_arg = args["review"]
    if retrieve_arg["purchase"] == "false":
        purchase = False
    else:
        purchase = True
    review_create = Document(
        id=str(retrieve_arg["id"]),
        name=retrieve_arg["name"],
        dealership=int(retrieve_arg["dealership"]),
        review=retrieve_arg["review"],
        purchase=purchase,
        another=retrieve_arg["another"],
        purchase_date=retrieve_arg["purchase_date"],
        car_make=retrieve_arg["car_make"],
        car_model=retrieve_arg["car_model"],
        car_year=int(retrieve_arg["car_year"])
        )

    response = service.put_document(db="reviews",
                                    doc_id=str(uuid.uuid4()),
                                    document=review_create).get_result()
    return response

review_to_create = {
    "review": 
    { "id": "1114", 
    "name": "Upkar Lidder", 
    "dealership": 15, 
    "review": "Great service!", 
    "purchase": "false", 
    "another": "field", 
    "purchase_date": "02/16/2021", 
    "car_make": "Audi", 
    "car_model": "Car", 
    "car_year": 2021 
    }
}
post_review(review_to_create)


