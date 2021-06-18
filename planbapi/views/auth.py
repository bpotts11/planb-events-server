import json
from django.http import HttpResponse, HttpResponseNotAllowed
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authtoken.models import Token
from planbapi.models import *


@csrf_exempt
def login_user(request):
    '''Handles the authentication of a user

    Method arguments:
      request -- The full HTTP request object
    '''

    req_body = json.loads(request.body.decode())

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':

        # Use the built-in authenticate method to verify
        email = req_body['email']
        password = req_body['password']
        authenticated_user = authenticate(username=email, password=password)

        # If authentication was successful, respond with their token
        if authenticated_user is not None and authenticated_user.is_staff == True:
            token = Token.objects.get(user=authenticated_user)
            data = json.dumps(
                {"valid": True, "token": token.key, "is_staff": True})
            return HttpResponse(data, content_type='application/json')

        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)
            data = json.dumps({"valid": True, "token": token.key})
            return HttpResponse(data, content_type='application/json')

        else:
            # Bad login details were provided. So we can't log the user in.
            data = json.dumps({"valid": False})
            return HttpResponse(data, content_type='application/json')

    return HttpResponseNotAllowed(permitted_methods=['POST'])


@csrf_exempt
def register_user(request):
    '''Handles the creation of a new user for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    # Load the JSON string of the request body into a dict
    req_body = json.loads(request.body.decode())

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    new_user = User.objects.create_user(
        username=req_body['email'],
        email=req_body['email'],
        password=req_body['password'],
        first_name=req_body['first_name'],
        last_name=req_body['last_name']
    )
    if req_body.get('authorized') == True:
        new_user.is_staff = True
        new_user.save()
        vendor = Vendor.objects.create(
            business_name=req_body['business_name'],
            about=req_body['about'],
            category_id=req_body['category_id'],
            phone=req_body['phone_number'],
            address=req_body['address'],
            city=req_body['city'],
            state=req_body['state'],
            user=new_user
        )
        # Commit the user to the database by saving it
        vendor.save()

    else:
        customer = Customer.objects.create(
            user=new_user
        )
        # Commit the user to the database by saving it
        customer.save()

    # new_user.save()

    # Use the REST Framework's token generator on the new user account
    token = Token.objects.create(user=new_user)

    # Return the token to the client
    data = json.dumps({"token": token.key, "id": new_user.id,
                      "is_vendor": new_user.is_staff})
    return HttpResponse(data, content_type='application/json', status=status.HTTP_201_CREATED)
