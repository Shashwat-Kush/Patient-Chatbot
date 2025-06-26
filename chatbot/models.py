from django.db import models

class Patient(models.Model):
    # The patient’s name
    name = models.CharField(max_length=100)

    # When their next appointment is scheduled
    next_appointment = models.DateTimeField(null=True, blank=True)

    # A simple comma-separated list of medications
    medications = models.TextField(
        help_text="Comma-separated list, e.g. 'aspirin,metformin'"
    )

    def __str__(self):
        # What shows up when Django needs a string (in admin, shell, etc.)
        return f"{self.name}"
    
from django.db import models
from django.conf import settings

class ChatMessage(models.Model):
    room = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chat_messages'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        # Useful for admin or debugging
        return f"[{self.timestamp:%Y-%m-%d %H:%M}] {self.user.username}: {self.content}"  