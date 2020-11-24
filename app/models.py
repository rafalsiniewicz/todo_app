from django.db import models
from django.contrib.auth.models import User
# Create your models here.


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
