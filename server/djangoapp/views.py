from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

def about(request):
    return render(request,"djangoapp/about_us.html")

def contact(request):
    return render(request,"djangoapp/contact_us.html")

def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        pwd = request.POST["pwd"]
        user = authenticate(username=username,password=pwd)
        if user is not None:
            login(request,user)
            return redirect("djangoapp:index")
        else:
            context["message"]="Invalid username or password"
            return render(request,"djangoapp/index.html",context)
    else:
        context["message"]="Not a message"
        return render(request,"djangoapp/index.html",context)
        

def logout_request(request):
    logout(request)
    return redirect("djangoapp:index")

def registration_request(request):
    context = {}
    if request.method == "GET":
        return render(request,"djangoapp/registration.html",context)
    elif request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        password = request.POST["pwd"]
        #try creating the user, check if exists
        user_exist = False
        try:
            user = User.objects.get(username=username)
            user_exist = True
        except:
            #u can create it
            logger.debug("{} is the new user".format(username))
        if not user_exist:
            user = User.objects.create_user(username=username,first_name=first_name,last_name=last_name,password=password)
            login(request,user)
            return redirect("djangoapp:index")
        else:
            context["error"] = "User already exists!"
            return render(request,"djangoapp/registration.html",context)





# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://eu-de.functions.appdomain.cloud/api/v1/web/francesco_ferrari_francescofer_space/dealership-package/get-dealership.json"
        dealerships = get_dealers_from_cf(url)
        context = {"dealers":dealerships}
        return render(request,"djangoapp/index.html",context)
        

def get_dealerships_by_state(request,state):
    if request.method == "GET":
        url = "https://eu-de.functions.appdomain.cloud/api/v1/web/francesco_ferrari_francescofer_space/dealership-package/get-dealership.json?state="+state
        dealerships = get_dealers_by_state(url,state)
        context = {"dealers":dealerships}
        return render(request,"djangoapp/dealers.html",context)
        
def get_dealer_id(request,dealer_id):
    if request.method == "GET":
        url = "https://eu-de.functions.appdomain.cloud/api/v1/web/francesco_ferrari_francescofer_space/dealership-package/get-dealership.json?id="+dealer_id
        dealer = get_dealer_by_id(url,dealer_id)
        if dealer:
            return HttpResponse("<h1>"+dealer[0].full_name+"</h1>")
        else:
            return HttpResponse("<h1>No dealer with that id!</h1>")

def get_dealer_details(request,dealerId):
    if request.method == "GET":
        url = "https://eu-de.functions.appdomain.cloud/api/v1/web/francesco_ferrari_francescofer_space/review-package/get-review.json?dealerId="+dealerId
        dealer_review = get_dealer_reviews_from_cf(url, dealerId)
        return render(request,"djangoapp/review.html",context={"reviews":dealer_review,"dealerId":dealerId})


def add_review(request):
    if request.method == "POST" and "login" not in request.POST:
            review = {}
            review["id"] = request.POST["id"]
            review["name"] = request.POST["name"]
            review["dealership"] = request.POST["dealership"]
            review["review"] = request.POST["review"]
            review["car_make"] = request.POST["car_make"]
            review["car_model"] = request.POST["car_model"]
            review["car_year"] = request.POST["car_year"]
            review["purchase"] = request.POST["purchase"]
            review["purchase_date"] =  request.POST["purchase_date"]
            review["another"] = request.POST["another"]
            json_payload = {}
            json_payload["review"] = review
            url = "https://eu-de.functions.appdomain.cloud/api/v1/web/francesco_ferrari_francescofer_space/review-package/post-review.json"
            status_code = post_request(url, json_payload)
            return render(request,"djangoapp/add_review.html",context={"status_code":status_code})
    else: 
        return render(request,"djangoapp/add_review.html")


