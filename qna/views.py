from django.shortcuts import render,redirect
import os
from content.tasks import send_test_email,get_new_questions

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        send_test_email(email)
        
        request.session['user_email'] = email
        redirect_uri = "http://127.0.0.1:8000/homepage/api/stackexchange/callback/"
        client_id = os.getenv('CLIENT_ID')
        oauth_url = (
            f"https://stackoverflow.com/oauth?client_id={client_id}&scope=write_access&redirect_uri={redirect_uri}"
        )
        get_new_questions()
        return redirect(oauth_url)

    
    if 'se_access_token' in request.session:
        return redirect('homepage')

    return render(request, 'home.html')

def feedback(request):
    return render(request,'feedback.html')







