from django.urls import path
from organisation.views import UserDetailView,Orglistview,OrgDetailView

urlpatterns = [
    path('users/<userId>',UserDetailView.as_view()),
    path('organisations',Orglistview.as_view()),
    path('organisations/<orgid>',OrgDetailView.as_view()),
    path('organisations/<orgId>/users',Orglistview.as_view()),


]
