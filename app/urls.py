
from django.urls import path

from app import views

urlpatterns = [
    path('book/',views.BookAPIView.as_view() ),
    path('book/<str:id>/',views.BookAPIView.as_view() ),
    path('book2/',views.BookAPIView2.as_view() ),
    path('book2/<str:id>/',views.BookAPIView2.as_view() ),
    path('book_logic/',views.BookLoginRegister.as_view({"put":"user_login","post":"user_register"}) ),
    path('book_logic/<str:username>/',views.BookLoginRegister.as_view({"put":"user_login","post":"user_register"}) ),

]