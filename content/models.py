from django.db import models
from django.urls import reverse
from django.utils import timezone

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('deleted', 'Deleted'),
    ]

    question_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=200)
    body = models.TextField()
    author = models.CharField(default='User',max_length=200)
    
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    score = models.IntegerField(default=0)

    question_link = models.URLField(null=True, blank=True)  
    
    view_count = models.PositiveIntegerField(default=0)
    answer_count = models.PositiveIntegerField(default=0)
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_activity_date = models.DateTimeField(default=timezone.now)
    profile_image = models.ImageField(default='https://share.google/images/sZNPcYSLjis7n9HqX')
    profile_link = models.URLField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='questions')

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['-score']),
            models.Index(fields=['-last_activity_date']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('question_detail', kwargs={'pk': self.pk})

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer_id = models.IntegerField(unique=True)
    body = models.TextField(blank=True)
    score = models.IntegerField()
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField()
    last_activity_date = models.DateTimeField()
    owner_display_name = models.CharField(max_length=100)
    owner_profile_image = models.URLField(default='https://share.google/images/sZNPcYSLjis7n9HqX')
    owner_reputation = models.IntegerField(default=0)
    owner_profile_link = models.URLField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='answers')

    class Meta:
        ordering = ['-score', '-is_accepted']  # Show accepted and high-scored answers first

    def __str__(self):
        return f"Answer to: {self.question.title}"
    
class User_Question(models.Model):
    name = models.CharField(max_length=100)
    email = models.URLField(null=True, blank=True)
    user_id = models.IntegerField(default=0)
    question_title = models.CharField(max_length=200)
    question_body = models.TextField(blank=True)
    question_remarks = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class User_Answer(models.Model):
    name = models.CharField(max_length=100)
    email = models.URLField(null=True, blank=True)
    user_id = models.IntegerField(default=0)
    question_id = models.IntegerField(default=0)
    question_link = models.URLField(null=True, blank=True)
    answer_title = models.CharField(max_length=200)
    answer_body = models.TextField(blank=True)
    answer_remarks = models.TextField(blank=True)

    def __str__(self):
        return self.name


