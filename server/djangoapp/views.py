from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from .models import DealerReview
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, getById , post_request
# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context={}
    if request.method == "GET":
        url = "https://693a3003.eu-de.apigw.appdomain.cloud/dealer/entries"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        context["dealership_list"]=dealerships
        return render(request, 'djangoapp/index.html',context)



# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    context={}
    url_dealer = "https://693a3003.eu-de.apigw.appdomain.cloud/api/dealers"
    url = "https://693a3003.eu-de.apigw.appdomain.cloud/api/reviews"
    apikey=""
    print("dealer_id: ")
    print(dealer_id)
    # Get dealers from the URL
    #dealer_details = get_dealer_reviews_from_cf(url_dealer,dealer_id)
    reviews = get_dealer_reviews_from_cf(url,dealer_id)
    context["dealer_id"]=dealer_id
  #  context["dealership"]=dealer_details
    context["reviews"]= reviews
    return render(request, 'djangoapp/dealer_details.html', context)
# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):

def add_review(request, dealer_id):
    context={}
    new_review= {}
    url = "https://693a3003.eu-de.apigw.appdomain.cloud/dealer/entries"
    # Get dealers from the URL
    print("review add: ")
    print(request.user.username)
    dealerships = get_dealers_from_cf(url)
    dealer = getById(dealerships,dealer_id)
    if request.method == "GET":
        context["dealer_id"] = dealer_id
        context["dealer"] = dealer[0]
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        url = "https://693a3003.eu-de.apigw.appdomain.cloud/api/addreview"
        # Check if user exists
        new_review['name'] = request.user.username
        new_review['dealership'] = dealer_id
        new_review['car_name'] = request.POST['car_name']
        new_review['review'] = request.POST['review']
        new_review['car_model'] = request.POST['car_model']
        new_review['car_make'] = request.POST['car_maker']
        new_review['car_year'] = request.POST['car_year']
        purchase = request.POST['purchased']
        new_review['purchase'] = purchase
        print(purchase)
        if purchase == False :
            new_review['purchase_date'] = False
        else :
            new_review['purchase_date'] = request.POST['purchased_date']
        print(new_review)
        post_request(url, new_review, dealerId=dealer_id)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
# ...

