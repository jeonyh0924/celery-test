import logging

from django.contrib.auth import get_user_model
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from config.celery import create_users_async

User = get_user_model()

logger = logging.getLogger(__name__)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()

    @action(methods=['POST'], detail=False)
    def create_user(self, request):
        is_async = request.data['is_async']
        user_count = request.data['user_count']

        if is_async:
            # worker한테 일을 위임
            create_users_async.delay(user_count)
        else:
            # 장고에서 직접
            create_users_async(user_count)

        return Response(data={'user_count': user_count}, status=status.HTTP_201_CREATED)


class HealthViewSet(APIView):
    def get(self, request, *args, **kwargs):
        logger.info(
            'Health Page Test!! : info'
        )
        logger.warning(
            'Health Page Test!! : warning'
        )
        logger.error(
            'Health Page Test !! : error'
        )

        first_user = User.objects.first()
        data = {
            'first_user': first_user.username
        }
        return Response(data=data)
