from django.shortcuts import render,redirect
from django.http import Http404,HttpResponse
from django.core.paginator import Paginator
import requests
from .models import Question, Answer, Tag
from datetime import datetime
from dotenv import load_dotenv
import pytz, os
load_dotenv()

def fetch_stackoverflow_questions():
    url = "https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow&filter=!u.*0Ven9AME1G2jH2G-WWtShW1E9kpi"  # filter to get body and answers
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['items']
    else:
        return Http404

def save_questions_to_db(questions_json):
    for q in questions_json:
        creation_dt = datetime.fromtimestamp(q['creation_date'], tz=pytz.UTC)
        last_activity_dt = datetime.fromtimestamp(q['last_activity_date'], tz=pytz.UTC)

        owner = q.get('owner', {})
        profile_image = owner.get('profile_image', '')
        profile_link = owner.get('link','.. ')

        tags_list = q.get('tags',[])

        question, created = Question.objects.update_or_create(
            question_id=q['question_id'],
            defaults={
                'title': q['title'],
                'body': q['body_markdown'],
                'score': q['score'],
                'author':q['owner']['display_name'],
                'answer_count': q['answer_count'],
                'view_count': q['view_count'],
                'created_at': creation_dt,
                'last_activity_date': last_activity_dt,
                'question_link': q['link'],
                'profile_image': profile_image,
                'profile_link': profile_link,
            }
        )

        tag_objs = []
        for tag_name in tags_list:
            tag_obj, _ = Tag.objects.get_or_create(name=tag_name)
            tag_objs.append(tag_obj)

        question.tags.set(tag_objs)

        answers_data = q.get('answers', [])
        save_answers_to_db(answers_data, question)

    total = Question.objects.count()
    Question.objects.filter(score__lte=0).delete()
    if total > 1024:
        latest_ids = (
            Question.objects.order_by('-last_activity_date').values_list('id', flat=True)[:1024]
        )
        Question.objects.exclude(id__in=latest_ids).delete()
    

def save_answers_to_db(answers_json, question):
    for answer_data in answers_json:
        creation_dt = datetime.fromtimestamp(answer_data['creation_date'], tz=pytz.UTC)
        last_activity_dt = datetime.fromtimestamp(answer_data['last_activity_date'], tz=pytz.UTC)
        owner = answer_data.get('owner', {})
        profile_image = owner.get('profile_image', '')
        reputation = owner.get('reputation', 0)
        display_name = owner.get('display_name', 'Anonymous')
        profile_link = owner.get('link','')

        Answer.objects.update_or_create(
            answer_id=answer_data['answer_id'],
            defaults={
                'question': question,
                'body': answer_data.get('body', ''),
                'score': answer_data['score'],
                'is_accepted': answer_data.get('is_accepted', False),
                'created_at': creation_dt,
                'last_activity_date': last_activity_dt,
                'owner_display_name': display_name,
                'owner_profile_image': profile_image,
                'owner_reputation': reputation,
                'owner_profile_link': profile_link,
            }
        )

def homepage(request):
    if(request.session.get('user_email',0)==0):
        return redirect('login')
    questions_qs = Question.objects.prefetch_related('answers').all().order_by('-view_count')
    paginator = Paginator(questions_qs, 5)
    page_number = request.GET.get('page')
    questions = paginator.get_page(page_number)

    access_token = request.session.get('se_access_token')
    
    if request.session.get('get_user_data', 0) == 0:
        user_data = get_stackexchange_user_profile(request, access_token, os.getenv('API_KEY'))
        request.session['user_data'] = user_data
    else:
        user_data = request.session.get('user_data', {'items': []})

    try:
        user = user_data['items'][0]
    except (KeyError, IndexError, TypeError):
        user = None

    context = {
        'questions': questions,
        'user': user,
    }

    return render(request, "base.html", context)

def get_stackexchange_user_profile(request, access_token, api_key):
    request.session['get_user_data'] = 1
    url = "https://api.stackexchange.com/2.3/me"
    params = {
        'access_token': access_token,
        'key': api_key,
        'site': 'stackoverflow'
    }
    response = requests.get(url, params=params)
    user_data = response.json()
    return user_data
