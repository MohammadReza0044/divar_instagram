from django.urls import path

from user import views

urlpatterns = [
    path("register/", views.RegisterApi.as_view(), name="register"),
    # path('profile/', ProfileApi.as_view(),name="profile"),
]
