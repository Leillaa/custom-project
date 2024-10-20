from rest_framework import serializers

from .models import Content


class ContentSerializer(serializers.ModelSerializer):
    parent_title = serializers.ReadOnlyField(source='parent.title')

    class Meta:
        fields = [
            'id',
            'title',
            'proof_link',
            'parent',
            'parent_title',
            'date_off',
        ]
        model = Content


class ContentMediaSerializer(serializers.ModelSerializer):

    class Meta:
        fields = [
            'program',
            'media',
            'file_id',
            'date_on',
            'date_off',
        ]
        model = Content
