# signals.py
import requests
import json
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def send_user_data(sender, instance, created, **kwargs):
    if created:
        user_data = {'user_type': instance.user_type, 'username': instance.username, 'Uni_ID': instance.Uni_ID, 'email': instance.email}
        response = requests.post('http://localhost:3000/new_user', data=json.dumps(user_data), headers={'Content-Type': 'application/json'})