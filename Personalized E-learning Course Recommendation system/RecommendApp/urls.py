from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
	             path("UserLogin.html", views.UserLogin, name="UserLogin"),
		     path("Register.html", views.Register, name="Register"),
		     path("RegisterAction", views.RegisterAction, name="RegisterAction"),
		     path("UserLoginAction", views.UserLoginAction, name="UserLoginAction"),
		     path("GetRecommend.html", views.GetRecommend, name="GetRecommend"),
		     path("GetRecommendAction", views.GetRecommendAction, name="GetRecommendAction"),		    
		    ]