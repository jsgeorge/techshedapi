from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

User = settings.AUTH_USER_MODEL


# Create your models here.
class Make(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Model(models.Model):
    make = models.ForeignKey(Make, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Trim(models.Model):
    make = models.ForeignKey(Make, null=True, on_delete=models.SET_NULL)
    model = models.ForeignKey(Model, null=True, on_delete=models.SET_NULL)

    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=250)
    image = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.name

    def imageURL(self):
            try:
                url = self.image.url
            except:
                url = ''
            return url

class Feature(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Auto(models.Model):
    COLORS = (('White', 'White'), ('Red', 'Red'), ('Blue', 'Blue'),
              ('Silver', 'Silver'), ('Green', 'Green'), ('Black', 'Black'))
    name = models.CharField(max_length=250)
    price = models.FloatField()
    discountpct = models.FloatField(default=0.00)
    make = models.ForeignKey(Make, null=True, on_delete=models.SET_NULL)
    model = models.ForeignKey(Model, null=True, on_delete=models.SET_NULL)
    trim = models.ForeignKey(Trim, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category,
                                 null=True,
                                 on_delete=models.SET_NULL)
    stock = models.IntegerField()
    description = models.CharField(max_length=1000, null=True, blank=True)
    color = models.CharField(max_length=200,
                             choices=COLORS,
                             null=True,
                             blank=True)
    features = models.ManyToManyField(Feature)
    location = models.CharField(max_length=200, blank=True, null=True)
    # image_url = models.CharField(max_length=2083)
    image = models.ImageField(null=True, blank=True)
    image2 = models.ImageField(null=True, blank=True)
    image3 = models.ImageField(null=True, blank=True)
    image4 = models.ImageField(null=True, blank=True)
    image5 = models.ImageField(null=True, blank=True)
    image6 = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def discount_price(self):
        discount= self.price - (self.price * self.discountpct)
        return(discount)
        
    def rating_cnt(self):
        ratings = AutoRating.objects.filter(auto=self)
        return len(ratings)

    def ave_rating(self):
        sum = 0
        ratings = AutoRating.objects.filter(auto=self)
        if len(ratings) > 0:
            for r in ratings:
                sum += r.rating
            return sum / len(ratings)
        else:
            return 0

    def review_cnt(self):
        reviews = AutoReview.objects.filter(auto=self)
        return len(reviews)

class AutoRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auto= models.ForeignKey(Auto, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'auto'),)
        index_together = (('user', 'auto'),)

    def __str__(self):
        return self.auto

class AutoReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auto= models.ForeignKey(Auto, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'auto'),)
        index_together = (('user', 'auto'),)

    def __str__(self):
        return self.auto

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auto= models.ForeignKey(Auto, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'auto'),)
        index_together = (('user', 'auto'),)

    def __str__(self):
        return self.auto

class Staff(models.Model):
    firstname = models.CharField(max_length=250)
    lastname = models.CharField(max_length=250)
    dept = models.CharField(max_length=250)
    image = models.ImageField(null=True, blank=True)

    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def __str__(self):
        return self.firstname


class Order(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    auto = models.ForeignKey(Auto, null=True, on_delete=models.SET_NULL)
    qty = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)

    class Meta:
        unique_together = (('user', 'auto'),)
        index_together = (('user', 'auto'),)


    def __str__(self):
        return self.auto

