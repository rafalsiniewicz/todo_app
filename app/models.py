from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=200, default=None)


class TODO(models.Model):
    STATUS = [
        ('To do', 'TO DO'),
        ('In progress', 'IN PROGRESS'),
        ('Done', 'DONE')
    ]
    PRIORITY = [
        ('1', '1️⃣'),
        ('2', '2️⃣'),
        ('3', '3️⃣'),
        ('4', '4️⃣'),
        ('5', '5️⃣'),
        ('6', '6️⃣'),
        ('7', '7️⃣'),
        ('8', '8️⃣'),
        ('9', '9️⃣'),
        ('10', '🔟')
    ]
    title = models.CharField(max_length=50)
    status = models.CharField(max_length=30, choices=STATUS)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateField(auto_now_add=True, null=True)
    expiration_date = models.DateField('Expiration date', null=True)
    priority = models.CharField(max_length=2, choices=PRIORITY)
    comments = models.ManyToManyField(Comment, default=None)

class Team(models.Model):
    title = models.CharField(max_length=50, default=None)
    users = models.ManyToManyField(User, default=None)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_requests_created', default=[], blank=True)
    todos = models.ManyToManyField(TODO, default=None)
