from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealers_by_state
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
        return render(request,"djangoapp/dealers.html",context)
        

def get_dealerships_by_state(request,state):
    if request.method == "GET":
        url = "https://eu-de.functions.appdomain.cloud/api/v1/web/francesco_ferrari_francescofer_space/dealership-package/get-dealership.json?state="+state
        dealerships = get_dealers_by_state(url,state)
        context = {"dealers":dealerships}
        return render(request,"djangoapp/dealers.html",context)
        






# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

