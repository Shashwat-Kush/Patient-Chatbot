from django.db import models
from django.conf import settings

class Patient(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patient_profile",
    )
    next_appointment = models.DateTimeField(null=True, blank=True)
    medications      = models.TextField(
        help_text="Comma-separated list, e.g. 'aspirin,metformin'"
    )
    def __str__(self):
        return self.user.username

class ChatMessage(models.Model):
    room      = models.CharField(max_length=255)
    user      = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chat_messages'
    )
    content   = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
