from django.shortcuts import redirect, render
from django.http import HttpResponse

from cowsay_app.forms import CowSayForm
from cowsay_app.models import CowSayModel

import subprocess

# Convert bytes to string python 3:
# https://www.askpython.com/python/string/python-string-bytes-conversion


# Create your views here - Cowsay View
def index(request):
    if request.method == "POST":
        new_form = CowSayForm()
        form = CowSayForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            CowSayModel.objects.create(
              text_line=data['text_line'],
              cowsay_type=data['cowsay_type'],
            )
            text_line = data['text_line']
            cowsay_type = data['cowsay_type']
            form = CowSayForm()
            response = HttpResponse(
              'Successful post submission - return <a href={% url "homepage" %}>home</a>!'
            )
            # response = redirect(homepage) <-- Must set homepage to an url
            response.set_cookie('cow_post', text_line)
            response.set_cookie('cowsay', cowsay_type)
            return response

        cow_cookies = request.COOKIES.get('cow_post')
        if cow_cookies:
          form = CowSayForm()
          cow_post = request.COOKIES.get('cow_post')
          cowsay_type = request.COOKIES.get('cowsay')
            # utf-8 is used here because it is a very common encoding practice,
            # but you need to use the encoding in the proper location where
            # the data resides.
          process = subprocess.run(
              ['cowsay', '-f', f'{cowsay_type}', f'{cow_post}'], capture_output=True
          ).stdout.decode("utf-8")

          reload_message = 'Welcome back to Cow_Say!'
          return render(request, "index.html", {
              "output": process,
              "form": new_form,
              "reload_message": reload_message,
          })
          # cow_says = cowsay.dragon('Hello TL')
    process = subprocess.run(
      ['cowsay', 'Welcome!'], capture_output=True
    ).stdout.decode("utf-8")
    form = CowSayForm()
    return render(request, "index.html", {
      "homepage": "Cowsay Home",
      "form": form,
      "process": process,
    })


# Displays the 10 most recent strings submitted
# Use negative indexes in QuerySet, inverted order of the id, then slice it
# Resource StackOverFlow: https://stackoverflow.com/questions/47428403/how-to-get-the-last-10-item-data-in-django
def history(request):
    cow_says = CowSayModel.objects.all().order_by('-id')[:10]
    cowsay_type = cow_says.cowsay_type
    reload_message = cow_says.text_line
    
    return render(request, "history.html", {
      "history_page": "Cowsay History",
      "history": cow_says
    })
