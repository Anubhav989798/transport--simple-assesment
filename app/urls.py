from django.urls import path
from .views import LoginView,SignUpView,logoutView,homeView,PostingQuestion,AnswerView,postAnswerView

urlpatterns = [
    path('login/',LoginView,name='login'),
    path('signUp/',SignUpView,name='signUp'),
    path('logout/',logoutView,name='logout'),
    path('home/',homeView.as_view(),name='home'),
    path('questionpost/',PostingQuestion.as_view(),name='questionpost'),
    path('answerview/<int:pk>/',AnswerView.as_view(),name='answerview'),
    path('answerpost/<int:pk>/',postAnswerView.as_view(),name='answerpost'),
]