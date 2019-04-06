from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from .models import User
from . import serializers
import json


class UserDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except:
            return HttpResponseBadRequest(json.dumps(
                {"message": "User does not exist."}), content_type="application/json")
        returned = {"id": user.id,
                    "username": user.username, "name": user.name}
        return HttpResponse(json.dumps(returned), content_type="application/json")


class CreateAccount(APIView):

    def post(self, request):
        try:
            username = request.data["username"]
            password = request.data["password"]
            name = request.data["name"]
        except:
            return HttpResponseBadRequest(json.dumps(
                {"message": "Required fields missing."}), content_type="application/json")
        try:
            User.objects.create_user(
                username=username, password=password, email=username, name=name)
        except:
            return HttpResponseBadRequest(json.dumps(
                {"message": "Account already exists."}), content_type="application/json")
        return HttpResponse(json.dumps({"message": "Account created."}), content_type="application/json")
