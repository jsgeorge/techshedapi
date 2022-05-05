from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image']



class MakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Make
        fields = ['id', 'name']


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ['id', 'name']


class TrimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trim
        fields = ['id', 'name']


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['id', 'name']




class AutoSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    make = MakeSerializer(many=False)
    model = ModelSerializer(many=False)
    trim = TrimSerializer(many=False)
    #feature = FeatureSerializer(many=False)
    
    class Meta:
        model = Auto
        fields = ['id',  'name', 'category', 'make', 'model',
                  'trim',   'price', 'discountpct', 'stock', 
                  'color',  'image', 'image2', 'image3', 
                  'location', 'description', 'featured', 
                  'created_at', 'rating_cnt', 'ave_rating',
                  'review_cnt',  'discount_price', 'sold']
    
    def get_votes(self, obj):
        return obj.votes.count()

    def get_reviews(self, obj):
        return obj.reviews.count()


class AutoRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoRating
        fields = ['id', 'auto', 'user', 'rating']

class AutoReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoReview
        fields = ['id', 'auto', 'user', 'content']

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'auto', 'user']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','user','auto','qty', 'created_at','complete']
 