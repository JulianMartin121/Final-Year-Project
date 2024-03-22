from django.db import models
from django.utils import timezone
from accounts.models import CustomUser

# Create your models here.
class Lecture(models.Model):
    title = models.CharField(max_length=200)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)


