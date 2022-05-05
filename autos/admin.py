from django.contrib import admin
from .models import *
from django.utils.html import format_html


# Register your models here.
class AutoAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'model',
        'trim',
        'category',
        'stock',
        'sold',
        'location',
        'featured',
    )


class FeaturedAdmin(admin.ModelAdmin):
    list_display = ('auto', )


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'created_at',
        'user',
        'auto',
        'qty',
    )

class AutoRatingAdmin(admin.ModelAdmin):
    list_display = ('auto', 'user', 'rating',)


class AutoReviewAdmin(admin.ModelAdmin):
    list_display = ('auto', 'user', 'content',)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('auto', 'user',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image',)


class MakeAdmin(admin.ModelAdmin):
    list_display = ('name',  )


class ModelAdmin(admin.ModelAdmin):
    list_display = ('name',)


class TrimAdmin(admin.ModelAdmin):
    list_display = ('name', )


class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name', )


class StaffAdmin(admin.ModelAdmin):
    def avatar(self, object):
        return format_html(
            '<img src="{}" width="40" style="border-radius:40px"/>'.format(
                object.image.url))

    list_display = ('id', 'avatar', 'lastname', 'firstname', 'dept',)
    list_display_liks = ("id", "firstname")
    search_fields = ("firstname", "lastname")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Auto, AutoAdmin)
admin.site.register(AutoRating, AutoRatingAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(AutoReview, AutoReviewAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Make, ModelAdmin)
admin.site.register(Model, TrimAdmin)
admin.site.register(Trim, TrimAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Staff, StaffAdmin)