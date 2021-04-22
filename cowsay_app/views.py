from django.shortcuts import redirect, render
from django.http import HttpResponse
import subprocess

from cowsay_app.forms import CowSayForm
from cowsay_app.models import CowSayModel

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
              'Successful post submission - return <a href="/">home</a>!'
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
              ['cowsay', '-f', f'{cow_post}', f'{cowsay_type}'], capture_output=True
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
    cow_posts = CowSayModel.objects.all()
    posts_num = len(cow_posts)
    
    first_post = CowSayModel.objects.all().order_by('-id')

    if posts_num >= 10:
      first_post = posts_num - 10
    
    cow_post = CowSayModel.objects.get(id=first_post)

    cowsay_type = cow_post.cowsay_type
    # print('Post_Type:', post_type)
    message = cow_post.text_line
    # print('Message:', reload_message)
    process = subprocess.run(['cowsay', '-f', f'{cowsay_type}',
                          f'{message}'], capture_output=True).stdout.decode("utf-8")
    # print('Subprocess:', process)

    history = CowSayModel.objects.all().order_by('-id')[:10]

    return render(request, "history.html", {
      "history_page": "Cowsay History",
      "history": history,
      "process": process
    })


# server_error
def error_500(request, exception=None):
    return render(request, "500.html", {}, status=500)


# page_not_found
def error_404(request, exception):
    return render(request, "404.html", {}, status=404)


# permission_denied
def error_403(request, exception=None):
    return render(request, "403.html", {}, status=403)


# bad_request
def error_400(request, exception=None):
    return render(request, "400.html", {}, status=400)