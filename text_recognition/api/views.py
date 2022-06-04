

import numpy as np

from .models import Account, User, Picture
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .serializers import AccountSerializer, FileSerializer, LoginSerializer, PictureShowSerializer
from rest_framework import status
from .utils import check_password
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.models import AuthToken
from base64 import b64encode
import logging
import cv2
import pytesseract
import base64
import os
from django.conf import settings
from PIL import Image
logger = logging.getLogger('info')
# Create your views here.


 


@api_view(['POST'])
def register(request):
    data = request.data
    print(data)
    serializer = AccountSerializer(data=data)
    print(serializer.is_valid())
    if serializer.is_valid():
        print(check_password(serializer.data["password"]))
        if check_password(serializer.data["password"]):
            user_account = User.objects.create_user(username=serializer.data["username"],email=serializer.data["email"],password=serializer.data["password"])
            
            account = Account.objects.create(user=user_account,username=user_account.username,email=user_account.email)
            account.save()
            data = {
                "message": "Registeration successfull",
                "status": status.HTTP_201_CREATED,
                "data" : serializer.data
            }
            return Response(data=data)
        else:
            data = {
                "message": "Password not valid",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(data)
    else:
        errors = []
        for i in serializer.errors:
            errors.append("{} is required".format(i))
        data = {
            "status": status.HTTP_409_CONFLICT,
            "message": "Error!",
            "data": serializer.errors
        }
        return Response(data)


@api_view(['POST'])
def login_account(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.validated_data['user']
        try:
            accountObject = Account.objects.get(username=user.username)
            token = AuthToken.objects.create(user)[1]
            data = {
                "message": "User details",
                "status": status.HTTP_202_ACCEPTED,
                "data": {
                    "email": accountObject.email,
                    "username": accountObject.username,
                },
                "token": token
            }
            return Response(data)
        except User.DoesNotExist:
            data = {
                "message": "User not found!",
                "status": status.HTTP_204_NO_CONTENT,
            }
            return Response(data)
    else:
        data = {
            "message":"Error!",
            "status": status.HTTP_400_BAD_REQUEST,
            "data": serializer.error_messages
        }
        return Response(data)
    
        



@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@parser_classes([MultiPartParser,FormParser])
def uploadImage(request):
    serializer = FileSerializer(data=request.data)
    if serializer.is_valid():
        accountObject = Account.objects.get(username=request.user.username)
        try:
            file = request.data["image"]
            if bool(file) == False:
                raise KeyError
        except KeyError:
            data = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Image not uploaded",
            }
            return Response(data)
        pictureObject = Picture.objects.create(account=accountObject,image=file)
        pictureObject.save()
        data = {
            "status": status.HTTP_202_ACCEPTED,
            "message": "Uploaded Image",
            "data": {
                "account": accountObject.email,
                "image": pictureObject.image.url,
            }
        }
        return Response(data)
    else:
        data = {
            "status": status.HTTP_400_BAD_REQUEST,
            "message": serializer.errors,
        }
        return Response(data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def displayImages(request):
    account = Account.objects.get(username=request.user.username)
    pictureObjects = account.picture_set.all()
    serializer = PictureShowSerializer(instance=pictureObjects,many=True)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser,FormParser])
def get_text_from_image(request):
    # Read image with opencv
    serializer = FileSerializer(data=request.data)
    if serializer.is_valid():
        accountObject = Account.objects.get(username=request.user.username)
        try:
            file = request.data["image"]
            if bool(file) == False:
                raise KeyError
        except KeyError:
            data = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Image not uploaded",
            }
            return Response(data)
        pictureObject = Picture.objects.create(account=accountObject,image=file)
        pictureObject.save()
    # img_path = request.build_absolute_uri(pictureObject.image.url)
    
    img = Image.open(pictureObject.image).convert('RGB')
    open_cv_image = np.array(img)
    img = open_cv_image[:, :, ::-1]
    "media/images/testocr.png"
    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    result = pytesseract.image_to_string(image=img)
    logger.info(result)
    data = {
        "status": status.HTTP_200_OK,
        "message": "Image saved! \n Found text inside image.",
        "data": result,
    }
    return Response(data)
