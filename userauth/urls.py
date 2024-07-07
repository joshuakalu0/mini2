from django.urls import path
from userauth.views import RegisterView,MyTokenObtainPairView

urlpatterns = [
    path('register',RegisterView.as_view()),
    path('login',MyTokenObtainPairView.as_view()),

]
