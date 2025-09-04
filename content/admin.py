from django.contrib import admin
from .models import Question, Answer,User_Question, User_Answer

# Register your models here.
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(User_Question)
admin.site.register(User_Answer)