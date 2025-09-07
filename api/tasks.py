from celery import shared_task
from content.models import User_Question, User_Answer

@shared_task
def save_question_async(name, email, user_id, question_title, question_body, question_remarks):
    
    user_question = User_Question.objects.create(
        name=name,
        email=email,
        user_id=user_id,
        question_title=question_title,
        question_body=question_body,
        question_remarks=question_remarks
    )
    return user_question.id

@shared_task
def save_answer_async(name, email, user_id, question_id, answer_body, answer_tags, answer_remarks):
    user_answer = User_Answer.objects.create(
        name=name,
        email=email,
        user_id=user_id,
        question_id=question_id,
        answer_body=answer_body,
        answer_tags=answer_tags,
        answer_remarks=answer_remarks
    )
    return user_answer.id