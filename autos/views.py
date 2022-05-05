from tarfile import PAX_FIELDS
from urllib import request
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.mail import send_mail
from django.contrib import messages
from .models import *
from .serializers import *
from account.models import *
from rest_framework import serializers, viewsets, status, filters
from rest_framework.response import Response
# , api_view, authentication_classes, permission_classes
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib import messages

# Create your views here.


class UserViewSetREST(viewsets.ModelViewSet):
    UserModel = get_user_model()
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    @action(detail=False, methods=['GET'])
    def current_user(self, request):
                curuser = User.objects.get(id=request.user.id)
                serializer = UserSerializer(curuser, many=False)
                response =  serializer.data
                return Response(response, status=status.HTTP_200_OK)

class AutoViewSetREST(viewsets.ModelViewSet):
    serializer_class = AutoSerializer
    queryset = Auto.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['name']
     
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    
    # @action(detail=False, methods=['POST'])
    # def create_new(self, request, pk=None):
    #      name = request.data['name']
    #      year = request.data['year']
    #      make = Make.objects.get(id=request.data['make'])
    #      model = Model.objects.get(id=request.data['model'])
    #      trim = Trim.objects.get(id=request.data['trim'])
    #      category = Category.objects.get(id=request.data['category'])
    #      location = request.data['location']
    #      price = request.data['price']
    #      stock = request.data['stock']
    #      image = request.data['image']
    #      auto = Auto.objects.create(
    #          name=name,
    #          year=year,
    #          make=make,
    #          model=model,
    #          trim=trim,
    #          category=category,
    #          location=location,
    #          price=price,
    #          stock=stock,
    #          image=image
    #      )
    #      serializer=AutoSerializer(auto, many=False)
    #      response = {
    #                 'message': "Auto created",
    #                 'result': serializer.data}
    #      return Response(response, status=status.HTTP_200_OK)
   
    # @action(detail=False, methods=['GET'])
    # def view_sold(self, request):
    #             sold_items = Auto.objects.filter(user=request.user)
    #             serializer = AutoSerializer(sold_items, many=True)
    #             response =  serializer.data
    #             print(response)
    #             return Response(response, status=status.HTTP_200_OK)
        
    @action(detail=True, methods=['POST'])
    def order_auto(self, request, pk=None):
        if 'qty' in request.data:
            auto = Auto.objects.get(id=pk)
            user = request.user
            qty = request.data['qty']
            print('auto ', auto)
            print('user ', user)
            print('qty', qty)
            
            # subject = request.data['subject']
            # email = request.data['email']
            # message = request.data['message']
       
            try:
               
                order = Order.objects.get(user=user, auto=auto, complete=False)
                print("Update Order")
                order.qty = qty
                order.save()
                serializer = OrderSerializer(order, many=False)
                response = {
                    'message': "Order updated",
                    'result': serializer.data}

                # auto.sold = auto.sold + qty
                # auto.save()
                # serializer = AutoSerializer(auto, many=False)

                return Response(response, status=status.HTTP_200_OK)
                # return redirect("/")
            except:
                print("New Order")    
                order = Order.objects.create(
                    user=user,auto=auto, qty=qty, complete=False)
              
                serializer = OrderSerializer(order, many=False)
                response = {
                    'message': "Order created",
                    'result': serializer.data}
                #send email
                #customerneed=  subject + ' ' + auto.name
                # message = message
                # email = email
                # send_mail(
                #     customerneed,
                #     message,
                #     email,
                #     ['gmeyer49s@gmail.com'],
                #     fail_silently=False,
                # )
               
                return Response(response, status=status.HTTP_200_OK)
                # return redirect("/")
        else:
            response = {'message': "Error you need to provide qty"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'])
    def rate_auto(self, request, pk=None):

        if 'stars' in request.data:
            auto = Auto.objects.get(id=pk)
            user = request.user
            rating = request.data['stars']
    
            try:
                vote = AutoRating.objects.get(user=user, auto=auto)
                vote.rating = rating
                vote.save()
                serializer = AutoRatingSerializer(vote, many=False)
                response = {
                    'message': "Rating updated",
                    'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
                #return redirect("/")
            except:
                vote = AutoRating.objects.create(
                    user=user, auto=auto, rating=rating)
                serializer = AutoRatingSerializer(vote, many=False)
                response = {
                    'message': "Rating created",
                    'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
                # return redirect("/")
        else:
            response = {'message': "Error you need to provide stars"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['POST'])
    def review(self, request, pk=None):
        if 'content' in request.data:
            auto = Auto.objects.get(id=pk)
            user = request.user
            content = request.data['content']
        
            try:
                review = AutoReview.objects.get(user=user, auto=auto)
                response = {'message': "Your already wrote a review for this auto"}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            except:
                review = AutoReview.objects.create(
                    user=user,auto=auto, content=content)
                serializer = AutoReviewSerializer(review, many=False)
                response = {
                    'message': "Review created",
                    'result': serializer.data}

                return Response(response, status=status.HTTP_200_OK)
                # return redirect("/")
        else:
            response = {'message': "Error you need to provide review"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'])
    def like(self, request, pk=None):
        print('LIKE', request.data['like'])
        #if 'like' in request.data:
        auto = Auto.objects.get(id=pk)
        user = request.user
        like = request.data['like']
        try:
            favorite = Favorite.objects.get(user=user, auto=auto)
            favorite.delete()
            serializer = OrderSerializer(favorite, many=False)
            response = {
                    'message': "Favorite deleted",
                    'result': serializer.data}
            return Response(response, status=status.HTTP_200_OK)
        except:
            #save to favorites
            favorite = Favorite.objects.create(
                user=user,auto=auto)
            serializer = FavoriteSerializer(favorite, many=False)
            response = {
                'message': "Favorite created",
                'result': serializer.data}

            return Response(response, status=status.HTTP_200_OK)
            # return redirect("/")
        
    # @action(detail=False, methods=['GET'])
    # def rating(self, request):
    #             print('user',request.user)
    #             print('auto', request.autoId)
    #             list_item = Favorite.objects.filter(user=request.user,auto=request.autoId)
    #             serializer = FavoriteSerializer(list_item, many=False)
    #             response =  serializer.data
    #             print(response)
    #             return Response(response, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def view_reviews(self, request,pk=None):
                auto = Auto.objects.get(id=pk)
                list_item = AutoReview.objects.filter(auto=auto)
                serializer = AutoReviewSerializer(list_item, many=True)
                response =  serializer.data
                print(response)
                return Response(response, status=status.HTTP_200_OK)


class AutoMakeViewSetREST(viewsets.ModelViewSet):
    serializer_class = AutoSerializer
    queryset = Auto.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['make']

    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)


class AutoCategoryViewSetREST(viewsets.ModelViewSet):
    serializer_class = AutoSerializer
    queryset = Auto.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']

    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    @action(detail=True, methods=['POST'])
    def order_auto(self, request, pk=None):
            if 'qty' in request.data:
                auto = Auto.objects.get(id=pk)
                user = request.user
                qty = request.data['qty']
            
                try:
                    order = Order.objects.get(user=user, auto=auto)
                    order.qty = qty
                    order.save()
                    serializer = OrderSerializer(order, many=False)
                    response = {
                        'message': "Order updated",
                        'result': serializer.data}
                    return Response(response, status=status.HTTP_200_OK)
                    # return redirect("/")
                except:
                    order = Order.objects.create(
                        user=user,auto=auto, qty=qty)
                    serializer = OrderSerializer(order, many=False)
                    response = {
                        'message': "Order created",
                        'result': serializer.data}

                    return Response(response, status=status.HTTP_200_OK)
                    # return redirect("/")
            else:
                response = {'message': "Error you need to provide qty"}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

class AutoSearchViewSetREST(viewsets.ModelViewSet):
    serializer_class = AutoSerializer
    queryset = Auto.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name')
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

class LatestAutoViewSetREST(viewsets.ModelViewSet):
    
    #serializer_class = MovieMiniSerializer
    serializer_class = AutoSerializer
    queryset = Auto.objects.filter(
        featured=False).order_by('created_at').reverse()[:6]
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

class FeaturdAutoViewSetREST(viewsets.ModelViewSet):
    
    #serializer_class = MovieMiniSerializer
    serializer_class = AutoSerializer
    queryset = Auto.objects.filter(
        featured=True).reverse()[:6]
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

class BestSellersAutoViewSetREST(viewsets.ModelViewSet):
    
    #serializer_class = MovieMiniSerializer
    serializer_class = AutoSerializer
    queryset = Auto.objects.order_by('sold').reverse()[:6]
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

class OnSaleAutoViewSetREST(viewsets.ModelViewSet):
    
    #serializer_class = MovieMiniSerializer
    serializer_class = AutoSerializer
    queryset = Auto.objects.filter(
         discountpct__gt=0)[:6]
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

class CategoryViewSetREST(viewsets.ModelViewSet):
    
    #serializer_class = MovieMiniSerializer
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

class MakeViewSetREST(viewsets.ModelViewSet):
    
    #serializer_class = MovieMiniSerializer
    serializer_class = MakeSerializer
    queryset = Make.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)


class ModelViewSetREST(viewsets.ModelViewSet):
    
    #serializer_class = MovieMiniSerializer
    serializer_class = ModelSerializer
    queryset = Model.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)


class TrimViewSetREST(viewsets.ModelViewSet):
    
    #serializer_class = MovieMiniSerializer
    serializer_class = TrimSerializer
    queryset =Trim.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)


class OrderViewSetREST(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    @action(detail=False, methods=['GET'])
    def view_cart(self, request):
                cart_items = Order.objects.filter(user=request.user, complete=False)
                serializer = OrderSerializer(cart_items, many=True)
                response =  serializer.data
                return Response(response, status=status.HTTP_200_OK)
    

    # @action(detail=True, methods=['DELETE'])
    # def delete_cart_item(self, request):
    #             print('order id:',request.id)
    #             cart_item = Order.objects.delete(id=request.id)
    #             serializer = OrderSerializer(cart_item, many=True)
    #             response =  serializer.data
    #             print(response)
    #             return Response(response, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def place_order(self, request, pk=None):
            try:
                user = request.user
                qty = request.data['qty']
                complete = request.data['complete']
                order = Order.objects.get(id=pk )
                print(order.auto.id)
                order.complete=True
                order.save()
                serializer = OrderSerializer(order, many=False)
                response = {
                    'message': "Order Placed",
                    'result': serializer.data}
                print("Completed order")
                auto = Auto.objects.get(id=order.auto.id)
                auto.sold = auto.sold + qty
                auto.save()
                serializer = AutoSerializer(auto, many=False)

                return Response(response, status=status.HTTP_200_OK)
            except:
                response={'message': 'Error'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
  
    @action(detail=False, methods=['GET'])
    def view_orders(self, request):
                cart_items = Order.objects.filter(user=request.user, complete=True)
                serializer = OrderSerializer(cart_items, many=True)
                response =  serializer.data
                return Response(response, status=status.HTTP_200_OK)
    
class FavoriteViewSetREST(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    @action(detail=False, methods=['GET'])
    def view_list(self, request):
                print('user',request.user)
                list_items = Favorite.objects.filter(user=request.user)
                serializer = FavoriteSerializer(list_items, many=True)
                response =  serializer.data
                print(response)
                return Response(response, status=status.HTTP_200_OK)

    
class AutoReviewViewSetREST(viewsets.ModelViewSet):
    queryset = AutoReview.objects.all()
    serializer_class = AutoReviewSerializer
   
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

  