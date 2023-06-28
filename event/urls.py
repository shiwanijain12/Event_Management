from django.urls import path
from . import views

urlpatterns =[
    path('', views.home, name="home"),
    path('products/', views.products, name="products"),
    path('participant/<str:pk_test>/', views.participant, name="participant"),
    path('create_event/<str:pk>/', views.createEvent, name="create_event"),
    path('update_event/<str:pk>/', views.updateEvent, name="update_event"),
    path('delete_event/<str:pk>/', views.deleteEvent, name="delete_event"),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
]