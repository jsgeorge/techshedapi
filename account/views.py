from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegForm, LoginForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from autos.models import Auto, Request
from django.core.mail import send_mail
# Create your views here.


def signin_view(request, *args, **kwargs):
    form = AuthenticationForm(request, data=request.POST or None)
    #form = LoginForm()
    #if request.method == 'POST':
    #form = LoginForm(request.POST)
    if form.is_valid():
        user_ = form.get_user()
        login(request, user_)
        return redirect("/account/profile")
    else:
        messages.error(request, "Invalid entries")
    context = {'form': form, "btn_label": "Login", "title": "Signin"}
    return render(request, "account/signin.html", context)


def signup_view(request, *args, **kwargs):
    #form = UserCreationForm(request.POST or None)
    form = RegForm()
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            user = form.save()
            #user.set_password = form.cleaned_data.get("password1")
            #username = form.cleaned_data.gt("username")
            #login(request, user)
            return redirect("/account/signin")
        else:
            messages.error(request, "Invalid entries")
    context = {'form': form, "btn_label": "Register", "title": "Signup"}
    return render(request, "account/signup.html", context)


def signout_view(request, *args, **kwargs):
    if request.method == "POST":
        logout(request)
        return redirect('/')
    context = {
        'form': None,
        'description': "are you sure you want to logout?",
        "btn_label": "Signin",
        "title": "Logout"
    }
    return render(request, "account/signout.html", context)


@login_required
def profile_view(request, *args, **kwargs):
    requests = []
    if request.user.is_authenticated:
        requests = Request.objects.filter(
            user=request.user).order_by('created_at').reverse()
    context = {'requests': requests}
    return render(request, "account/profile.html", context)


@login_required
def send_contact_email(request):
    firstname = request.POST['first_name']
    lastname = request.POST['last_name']
    subject = request.POST['subject']
    email = request.user.email
    message = request.POST['message']

    #Send email to owner
    send_mail(
        subject,
        'From ' + firstname + lastname + '<br/> ' + 'Email' + email + '<br/>' +
        message,
        email,
        ['gmeyer49s@gmail.com'],
        fail_silently=False,
    )
    messages.success(request, "Contact email sent successfully")
    return redirect('/contacts')
    #  return JsonResponse("Car saved in you inquires")
