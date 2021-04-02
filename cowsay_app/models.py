from django.db import models
from django.utils import timezone

# Cowsay Model - A model that we can save the text line to
"""
Text Model:
-----------
cowsay_type (CharField)
text_line (TextField)
date (DateTimeField)
"""

# Create your models here.
class CowSayModel(models.Model):
    DEFAULT = 'Default'
    TUX = 'Tux'
    DRAGON = 'Dragon'
    HELLO_KITTY = 'Hello_Kitty'
    SKELETON = 'Skeleton'

    DISPLAY_CHOICES = [
        (DEFAULT, 'Default'),
        (TUX, 'Tux'),
        (DRAGON, 'Dragon'),
        (HELLO_KITTY, 'Hello_Kitty'),
        (SKELETON, 'Skeleton'),
        ]
    cowsay_type = models.CharField(
        max_length=15,
        choices=DISPLAY_CHOICES,
        default=DEFAULT
    )

    text_line = models.TextField(max_length=100)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.text_line}"
