from django.shortcuts import render,redirect
import requests
from django.http import HttpResponse, HttpResponseRedirect
from api.tasks import save_question_async, save_answer_async
from dotenv import load_dotenv
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os
load_dotenv()

@api_view(['GET','POST'])
def create_question(request):
    if(request.session.get('user_email',0)==0):
        return redirect('login')
    user_data = request.session.get('user_data')
    context={
        'user': user_data['items'][0],
        'email': request.session.get('user_email'),
    }
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        user_id = request.POST.get('user_id')
        question_title = request.POST.get('question_title')
        question_body = request.POST.get('question_body')
        question_remarks = request.POST.get('question_remarks', '')

        save_question_async.delay(name, email,user_id, question_title, question_body, question_remarks)
        return redirect('/')

    return render(request, 'create_question.html',context)

@api_view(['GET','POST'])
def create_answer(request, question_id):
    if(request.session.get('user_email',0)==0):
        return redirect('login')
    user_data = request.session.get('user_data')
    context={
        'user': user_data['items'][0],
        'email':request.session.get('user_email'),
        'question_id':question_id,
    }

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        user_id = request.POST.get('user_id')
        question = request.POST.get('question')
        answer_body = request.POST.get('answer_body')
        answer_tags = request.POST.get('answer_tags')
        answer_remarks = request.POST.get('answer_remarks','')

        save_answer_async.delay(name, email,user_id, question, answer_body, answer_tags, answer_remarks)
        return redirect('/')

    return render(request, 'create_answer.html',context)

@api_view(['GET'])
def stackexchange_callback(request):
    code = request.GET.get('code')
    if not code:
        return Response({'detail': 'Missing code parameter'}, status=status.HTTP_400_BAD_REQUEST)

    token_url = "https://stackoverflow.com/oauth/access_token/json"
    data = {
        'client_id': os.getenv('CLIENT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET'),
        'code': code,
        'redirect_uri': 'https://stackconnect-r3qa.onrender.com/homepage/api/stackexchange/callback/'
    }

    response = requests.post(token_url, data=data)
    if response.status_code != 200:
        return Response({'detail': 'Failed to get access token'}, status=response.status_code)

    token_data = response.json()
    access_token = token_data.get('access_token')

    if access_token:
        request.session['se_access_token'] = access_token

    return HttpResponseRedirect('/')

def exchange_code_for_token(code):
    url = "https://stackoverflow.com/oauth/access_token/json"
    data = {
        'client_id': os.getenv('CLIENT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET'),
        'code': code,
        'redirect_uri': "https://stackconnect-r3qa.onrender.com/stackexchange/callback/"
    }
    response = requests.post(url, data=data)
    return response.json()

def upvote_view(request, answer_id):
    access_token = request.session.get('se_access_token')

    result = upvote_answer(answer_id, access_token, os.getenv('API_KEY'))
    
    return HttpResponseRedirect('/feedback')

def upvote_question(request, question_id):
    access_token = request.session.get('se_access_token')

    result = upvote_question_id(question_id, access_token, os.getenv('API_KEY'))

    return HttpResponseRedirect('/feedback')

def upvote_answer(answer_id, access_token, api_key):
    url = f"https://api.stackexchange.com/2.3/answers/{answer_id}/upvote"
    data = {
        'key': api_key,
        'access_token': access_token,
        'site': 'stackoverflow'
    }
    response = requests.post(url, data=data)
    return response.json()

def upvote_question_id(question_id, access_token, api_key):
    url = f"https://api.stackexchange.com/2.3/questions/{question_id}/upvote"
    data = {
        'key': api_key,
        'access_token': access_token,
        'site': 'stackoverflow'
    }
    response = requests.post(url, data=data)
    return response.json()

def logout_view(request):
    request.session.flush()
    return redirect('login')
