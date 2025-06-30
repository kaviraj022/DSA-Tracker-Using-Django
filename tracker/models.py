from django.db import models

class User(models.Model):
    ROLE_CHOICES = [
        ('superadmin', 'Super Admin'),
        ('admin', 'Admin'),
        ('user', 'User')
    ]
    
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password_hash = models.CharField(max_length=255)
    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES,
        default='user'
    )
    
    class Meta:
        db_table = 'users'

class Problem(models.Model):
    topic = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    youtube_link = models.URLField(blank=True, null=True)
    practice_link = models.URLField(blank=True, null=True, max_length=1000)
    class Meta:
        db_table = 'problems' 
class UserNote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    note = models.TextField()
    class Meta:
        db_table = 'usernotes' 
class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    class Meta:
        db_table = 'userprogress' 