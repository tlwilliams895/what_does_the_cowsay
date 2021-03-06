from django.shortcuts import render
from cowsay_app.forms import CowSayForm
from cowsay_app.models import CowSayModel
import subprocess

# Assistance from Cesar Ramos, Deidre Boddie, Corey Shafer Tutorial
# on Subprocess, Real Python Tutorial, and Python docs
# Convert bytes to string python 3:
# https://www.askpython.com/python/string/python-string-bytes-conversion


# Create your views here - Cowsay View
# - if there is output, render it to the browser
# - always renders a fresh version of our form
def index(request):
    if request.method == "POST":
        new_form = CowSayForm()
        form = CowSayForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            CowSayModel.objects.create(
              text_line=data.get('text_line')
            )
            # utf-8 is used here because it is a very common encoding practice,
            # but you need to use the encoding in the proper location where
            # the data resides.
            process = subprocess.check_output(
                ['cowsay', data['text_line']]).decode("utf-8")
            # ...Or try this option - both works!!
            # process = subprocess.run(
            #     ['cowsay', data['text_line']], capture_output=True
            # ).stdout.decode("utf-8")

            return render(request, "index.html", {
                "output": process,
                "form": new_form
            })
            # cow_says = cowsay.dragon('Hello TL')
    form = CowSayForm()
    return render(request, "index.html", {
      "homepage": "Cowsay Home",
      "form": form,
    })


# Displays the 10 most recent strings submitted
# Use negative indexes in QuerySet, inverted order of the id, then slice it
# Resource StackOverFlow: https://stackoverflow.com/questions/47428403/how-to-get-the-last-10-item-data-in-django
def history(request):
    cow_says = CowSayModel.objects.all().order_by('-id')[:10]
    # cow_says = CowSayModel.objects.all()[::-1][:10]
    return render(request, "history.html", {
      "history_page": "Cowsay History",
      "history": cow_says
    })
