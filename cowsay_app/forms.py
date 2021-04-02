from django import forms
from cowsay_app.models import CowSayModel

# Cowsay Form - a form that just takes in a text line
"""
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
        max_length=8,
        choices=DISPLAY_CHOICES,
        default=DEFAULT
    )

    text_line = models.TextField(max_length=100)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.text_line}"
"""
# On submission of the form, it uses python's subprocess module to pass the
# submitted text to the cowsay utility and retrieves the output

# Create your forms here.
class CowSayForm(forms.Form):
    cowsay_type = forms.CharField()
    text_line = forms.CharField(widget=forms.TextInput)
    # date = forms.DateTimeField(widget=forms.TimeField)
