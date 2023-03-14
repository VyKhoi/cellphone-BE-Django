from rest_framework import serializers
from .models import *

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
class CommentSerializer(serializers.ModelSerializer):
    userName = serializers.ReadOnlyField(source='idUser.userName')

    class Meta:
        model = Comment
        fields = '__all__'
