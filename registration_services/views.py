import uuid

from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from main.sessions_storage import SessionsStorage

from .models import Guid, People

sessions_storage = SessionsStorage()


class UserView(APIView):
    def post(self, request):
       pass
