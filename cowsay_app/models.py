from django.db import models
from django.utils import timezone

# Cowsay Model - A model that we can save the text line to
"""
Text Model:
-----------
text_line (TextField)
date (DateTimeField)
"""


# Create your models here.
class CowSayModel(models.Model):
    text_line = models.TextField(max_length=100, null=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.text_line}"
