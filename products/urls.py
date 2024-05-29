from django.urls import path
from . import views

urlpatterns=[
    path('',views.retrievePosts , name="home"),
    path('save_product/',views.save_product,name="save_product"),
    path('add_like/',views.add_like,name="add_like")


]