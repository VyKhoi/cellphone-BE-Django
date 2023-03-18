from rest_framework import serializers
from .models import *
from rest_framework import serializers

class YourDataSerializer(serializers.Serializer):
    data_field_1 = serializers.CharField()
    data_field_2 = serializers.CharField()
    # và các trường dữ liệu khác nếu cần thiết

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
class CommentSerializer(serializers.ModelSerializer):
    userName = serializers.ReadOnlyField(source='idUser.userName')

    class Meta:
        model = Comment
        fields = '__all__'
