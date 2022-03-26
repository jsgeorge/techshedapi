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


# def home_view(request):
#     requests = []

#     if request.user.is_authenticated:
#         requests = Request.objects.filter(user=request.user)

#     categories = Category.objects.order_by('name')
#     cars_featured = Featured.objects.all()
#     cars_latest = Auto.objects.order_by('created_at').reverse()[:6]
#     makes = Make.objects.order_by('name')
#     inv_makes = Auto.objects.values_list('make', flat=True).distinct()
#     inv_models = Auto.objects.values_list('model', flat=True).distinct()
#     models = Model.objects.order_by('name')
#     trims = Trim.objects.all()
#     staff = Staff.objects.all()
#     context = {
#         'requests': requests,
#         'categories': categories,
#         'cars_featured': cars_featured,
#         'cars_latest': cars_latest,
#         'makes': makes,
#         'inv_makes': inv_makes,
#         'models': models,
#         'inv_models': inv_models,
#         'trims': trims,
#         'staff': staff
#     }

#     return render(request, "autos/pages/home2.html", context)


# def autos_view(request):
#     if request.user.is_authenticated:
#         requests = Request.objects.filter(user=request.user)

#     categories = Category.objects.order_by('name')
#     makes = Make.objects.order_by('name')
#     models = Model.objects.order_by('name')
#     trims = Trim.objects.all()
#     cars = Auto.objects.all()
#     paginator = Paginator(cars, 6)
#     page = request.GET.get('page')
#     paged_cars = paginator.get_page(page)
#     context = {
#         'requests': requests,
#         'categories': categories,
#         'makes': makes,
#         'models': models,
#         'trims': trims,
#         'cars': paged_cars,
#         'cnt': cars.count()
#     }
#     return render(request, "autos/pages/autos.html", context)


# def autos_ctgry_view(request, id, name):
#     if request.user.is_authenticated:
#         requests = Request.objects.filter(user=request.user)

#     categories = Category.objects.order_by('name')
#     makes = Make.objects.order_by('name')
#     models = Model.objects.order_by('name')
#     trims = Trim.objects.all()
#     if id:
#         cars = Auto.objects.filter(category_id=id)
#     else:
#         cars = Auto.objects.all()
#     paginator = Paginator(cars, 6)
#     page = request.GET.get('page')
#     paged_cars = paginator.get_page(page)
#     context = {
#         'requests': requests,
#         'categories': categories,
#         'searched': name,
#         'makes': makes,
#         'models': models,
#         'trims': trims,
#         'cars': paged_cars,
#         'cnt': cars.count()
#     }
#     return render(request, "autos/pages/autos.html", context)


# def srch_autos_view(request):
#     if request.method == "POST":
#         searched = request.POST['searched']
#         if searched:
#             cars = Auto.objects.filter(name__contains=searched)
#         else:
#             cars = Auto.objects.all()
#     context = {'searched': searched, 'cars': cars, 'cnt': cars.count()}
#     return render(request, "autos/pages/autos.html", context)


# def srch_autos_home_view(request):
#     if request.user.is_authenticated:
#         requests = Request.objects.filter(user=request.user)

#     if request.method == "POST":
#         searched = ""
#         searched = request.POST['searched']
#         if searched:
#             cars = Auto.objects.filter(name__contains=searched)
#         else:

#             cars = Auto.objects.all()
#             make = request.POST.get("srch-make")
#             model = request.POST.get("srch-model")
#             year = request.POST.get("srch-year")
#             location = request.POST.get("srch-location")
#             category = request.POST.get("srch-category")
#             # minprice = request.POST["data-min-price")
#             # maxprice = request.POST["data-max-price")
#             if not category:
#                 if year:
#                     cars = cars.filter(year=year)
#                     searched += year + " "

#                 if make:
#                     cars = cars.filter(make__name=make)
#                     searched += make + " "
#                 if model:
#                     cars = cars.filter(model__name=model)
#                     searched += model + " "
#                 if location:
#                     cars = cars.filter(location__contains=location)
#                     searched += "in " + location + " "
#             else:
#                 cars = Auto.objects.filter(category__name=category)
#                 searched = category

#     print("searched", searched)
#     context = {
#         'requests': requests,
#         'searched': searched,
#         'cars': cars,
#         'cnt': cars.count()
#     }
#     return render(request, "autos/pages/autos.html", context)


# def auto_detail_view(request, id):

#     car = Auto.objects.get(id=id)
#     requests = []
#     if request.user.is_authenticated:
#         requests = Request.objects.filter(user=request.user, auto=car)

#     if request.method == 'POST':
#         Request.objects.create(user=request.user, auto=car)

#     context = {'car': car, 'requests': requests}
#     return render(request, "autos/pages/detail.html", context)


# def save_auto_inquiry(request):

#     firstname = request.POST['first_name']
#     lastname = request.POST['last_name']
#     customerneed = request.POST['customer_need']
#     cartitle = request.POST['car_title']
#     city = request.POST['city']
#     state = request.POST['state']
#     email = request.POST['email']
#     phone = request.POST['phone']
#     text = request.POST['phone']
#     message = request.POST['message']
#     carid = request.POST['car_id']
#     userid = request.user.id
#     print('userid ', userid)
#     print('carid ', carid)
#     #Send email to owner
#     send_mail(
#         customerneed,
#         message,
#         email,
#         ['gmeyer49s@gmail.com'],
#         fail_silently=False,
#     )

#     #Save request inf User request File
#     car = Auto.objects.get(id=carid)
#     #request, created = Request.objects.get_or_create(user=request.user,
#     #                                               auto=car)
#     #Request.objects.create(user=request.user, auto=car)
#     request = Request(auto_id=carid, user_id=userid)
#     request.save()
#     messages.success(
#         request,
#         "Requst email sent successfully. One of our sales represresetatvie will contact you shortly"
#     )
#     return redirect('/autos/' + carid)
#     #  return JsonResponse("Car saved in you inquires")


# def about_view(request):
#     if request.user.is_authenticated:
#         requests = Request.objects.filter(user=request.user)

#     context = {'requests': requests}
#     return render(request, "autos/pages/about.html", context)


# def services_view(request):
#     if request.user.is_authenticated:
#         requests = Request.objects.filter(user=request.user)

#     context = {'requests': requests}
#     return render(request, "autos/pages/services.html", context)


# def contacts_view(request):
#     if request.user.is_authenticated:
#         requests = Request.objects.filter(user=request.user)

#     context = {'requests': requests}
#     return render(request, "autos/pages/contact.html", context)


class UserViewSetREST(viewsets.ModelViewSet):
    UserModel = get_user_model()
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    @action(detail=False, methods=['GET'])
    def current_user(self, request):
                print('user',request.user.id)
                curuser = User.objects.get(id=request.user.id)
                serializer = UserSerializer(curuser, many=False)
                response =  serializer.data
                print(response)
                return Response(response, status=status.HTTP_200_OK)

class AutoViewSetREST(viewsets.ModelViewSet):
    serializer_class = AutoSerializer
    queryset = Auto.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['name']
     
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    @action(detail=True, methods=['POST'])
    def order_auto(self, request, pk=None):
        if 'qty' in request.data:
            auto = Auto.objects.get(id=pk)
            user = request.user
            qty = request.data['qty']
            print('auto ', auto)
            print('user ', user)
            print('qty', qty)
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

    @action(detail=True, methods=['POST'])
    def rate_auto(self, request, pk=None):
        print(request.data)
        print(request.POST.get('stars'))
        if 'stars' in request.data:
            auto = Auto.objects.get(id=pk)
            user = request.user
            rating = request.data['stars']
            print('autoid ', pk)
            print('user ', user)
            print('rating', rating)
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
            print('auto ', auto)
            print('user ', user)
            print('content', content)
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
        if 'like' in request.data:
            auto = Auto.objects.get(id=pk)
            user = request.user
            like = request.data['like']
            print('auto ', auto)
            print('user ', user)
            print('like', like)
            if (like) :
                #send email
                customerneed= auto.name
                message = "Auto inquiry"
                email = user.email
                send_mail(
                    customerneed,
                    message,
                    email,
                    ['gmeyer49s@gmail.com'],
                    fail_silently=False,
                )
                #save to favorites
                favorite = Favorite.objects.create(
                    user=user,auto=auto)
                serializer = FavoriteSerializer(favorite, many=False)
                response = {
                    'message': "Favorite created",
                    'result': serializer.data}

                return Response(response, status=status.HTTP_200_OK)
                # return redirect("/")
                
            else:
               favorite = Favorite.objects.get(user=user, auto=auto)
               favorite.delete()
               serializer = OrderSerializer(favorite, many=False)
               response = {
                    'message': "Favorite deleted",
                    'result': serializer.data}
               return Response(response, status=status.HTTP_200_OK)
               # return redirect("/")
        else:
            response = {'message': "Error you need to provide like"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

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
    queryset = Auto.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

class CategoryViewSetREST(viewsets.ModelViewSet):
    
    #serializer_class = MovieMiniSerializer
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

class OrderViewSetREST(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    @action(detail=False, methods=['GET'])
    def view_cart(self, request):
                print('user',request.user)
                cart_items = Order.objects.filter(user=request.user, complete=False)
                serializer = OrderSerializer(cart_items, many=True)
                response =  serializer.data
                print(response)
                return Response(response, status=status.HTTP_200_OK)

    # @action(detail=True, methods=['DELETE'])
    # def delete_cart_item(self, request):
    #             print('order id:',request.id)
    #             cart_item = Order.objects.delete(id=request.id)
    #             serializer = OrderSerializer(cart_item, many=True)
    #             response =  serializer.data
    #             print(response)
    #             return Response(response, status=status.HTTP_200_OK)

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

    @action(detail=False, methods=['GET'])
    def view_item(self, request):
                print('user',request.user)
                list_item = Favorite.objects.filter(user=request.user,auto=request.autoId)
                serializer = FavoriteSerializer(list_item, many=False)
                response =  serializer.data
                print(response)
                return Response(response, status=status.HTTP_200_OK)
