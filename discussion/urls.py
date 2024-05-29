from django.urls import path
from . import views

urlpatterns = [
    # ... your existing URL patterns ...

    path('send_message/', views.send_message, name='send_message'),
    path('import_messages/', views.import_messages, name='import_messages'),
    path('load_messages/', views.load_messages, name='load_messages'),
    path('get_discussion/<int:discussion_id>/', views.get_discussion, name='get_discussion'),
    path('create_conversation/', views.create_conversation, name='create_conversation'),


]