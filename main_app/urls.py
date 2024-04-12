from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('furniture/', views.furniture_index, name="index"),
    
    path('accounts/signup/', views.signup, name='signup'),
    
    path('furniture/create/', views.Furniture_Item_Create.as_view(), name='furniture_create'),

    path('furniture/<int:furniture_item_id>/',views.furniture_detail, name='detail'),

    path('furniture/<int:furniture_item_id>/create/', views.add_photo, name='add_photo'),
    
    path('furniture/<int:pk>/delete/', views.Furniture_Item_Delete.as_view(), name='furniture_delete'),
]