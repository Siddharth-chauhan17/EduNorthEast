from django.contrib import admin
from django.urls import path, include
from home import views
urlpatterns = [
    path('',views.index, name="home"),
    path('login',views.loginUser, name="login"),
    path('logout',views.logoutUser, name="logout"),
    path('register', views.register, name="register"),
    path('joblisting', views.joblisting, name="joblisting"),
    path('personalised',views.history_display, name="personalised"),
    path('get_quiz/', views.get_quiz_view, name='get_quiz'),
    path('search/', views.search, name="search"),
    path('profile/', views.profile, name="profile"),
    path('about/', views.about, name="about"),
    path('update-profile/', views.update_profile, name="update_profile"),

    path('ai_ml/', views.ai_ml_page, name='ai_ml'),
    path('finance/', views.finance_page, name='finance'),
    path('cybersecurity/', views.cybersecurity_page, name='cybersecurity'),
    path('web_dev/', views.web_dev_page, name='web_dev'),
    path('blockchain/', views.blockchain_page, name='blockchain'),
    path('data_science/', views.data_science_page, name='data_science'),
    


]