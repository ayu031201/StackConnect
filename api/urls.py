from django.urls import path
from . import views

urlpatterns =[
    path('upvote/answer/<int:answer_id>/', views.upvote_view, name='upvote_answer'),
    path('upvote/question/<int:question_id>/', views.upvote_question, name='upvote_question'),
    path('logout/',views.logout_view, name='logout'),
    path('create_question/', views.create_question, name='create_question'),
    path('stackexchange/callback/', views.stackexchange_callback, name='stackexchange_callback'),
    path('create_answer/<int:question_id>', views.create_answer, name='create_answer'),
]