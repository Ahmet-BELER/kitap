from django.urls import path 
from kitaplar.api import views as api_views 
from knox import views as knox_views

urlpatterns = [
    
    path('kitaplar/',api_views.KitapListCreateApıWiews.as_view(),name="kitaplar"),
    path('kitaplar/<int:pk>' ,api_views.KitapDetailWiew.as_view(),name="kitaplap-detay"),
    path('kitaplar/<int:kitap_pk>/yorum_yap',api_views.YorumCreateAPIView.as_view(),name="yorum-yap"),
    path('yorumlar/<int:pk>',api_views.YorumDetailWiew.as_view(),name="yorum-detay"),
    path('register/', api_views.RegisterAPI.as_view(), name='register'),
    path('login/',api_views.LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),


] 

 
 
 