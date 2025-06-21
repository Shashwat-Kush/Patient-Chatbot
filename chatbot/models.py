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