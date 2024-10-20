from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import Content, ContentLog
from .serializers import ContentMediaSerializer, ContentSerializer

User = get_user_model()


class MainContentViewSet(ViewSet):

    http_method_names = ['get', 'post']

    def list(self, request, telegram_id, *args, **kwargs):
        """GET запрос выдаёт контент верхнего уровня - кнопка 'Начало'."""
        user = User.objects.get_or_create(telegram_id=telegram_id)[0]
        objects_back = ContentLog.objects.filter(user=user, date_back=None)
        if objects_back:
            objects_back.update(date_back=datetime.now())
        content = Content.objects.filter(parent=None)
        serializer = ContentSerializer(content, many=True)
        return Response(serializer.data)

    def retrieve(self, request,  telegram_id, pk, *args, **kwargs):
        """ GET запрос выдаёт дочерний контент
         для контента, ID которого передан в pk.
         """
        User.objects.get_or_create(telegram_id=telegram_id)
        try:
            Content.objects.get(pk=pk)
            content = Content.objects.filter(
                parent=pk
            ).exclude(date_off__lt=datetime.today().date())
            serializer = ContentSerializer(content, many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request, telegram_id, pk, *args, **kwargs):
        """По POST запросу создается запись в content_log, что пользователь с
        Telegram_id нажал на content.
        """
        user = User.objects.get_or_create(telegram_id=telegram_id)[0]
        content = get_object_or_404(Content, id=pk)
        if ContentLog.objects.create(user=user, content=content):
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get', 'post'])
    def media(self, request, pk, *args, **kwargs):
        """Реализация чтения медиа-контента и записи ID фото,
        загруженных в Telegram.
        """
        if request.method == 'POST':
            content = Content.objects.get(pk=pk)
            serializer = ContentMediaSerializer(content, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        content = Content.objects.filter(pk=pk)
        serializer = ContentMediaSerializer(content, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def back(self, request, telegram_id, *args, **kwargs):
        """Реализация кнопки 'Назад'."""
        user = User.objects.get_or_create(telegram_id=telegram_id)[0]
        objects_back = ContentLog.objects.filter(user=user, date_back=None)
        if objects_back:
            parent_id = objects_back.values_list(
                'content__parent_id', flat=True
            ).order_by('-id').first()
            current_object_back = objects_back.order_by('-id').first()
            current_object_back.date_back = datetime.now()
            current_object_back.save()
            back_content = Content.objects.filter(
                parent_id=parent_id
            ).exclude(date_off__lt=datetime.today().date())
        else:
            back_content = Content.objects.filter(parent=None)
        serializer = ContentSerializer(back_content, many=True)
        return Response(serializer.data)
