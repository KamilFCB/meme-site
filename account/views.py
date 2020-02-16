from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User

# Create your views here.
from django.views.decorators.http import require_http_methods


@login_required
def manage_view(request):
    """
    Display account manage view. Actually only allows to change password.
    :param request:
    :return: Account template
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('memes:index')
        else:
            return redirect('change_password')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/account.html', {
        'form': form,
        'username': request.user.get_username()
    })


def login_view(request):
    """
    Display login page
    :param request:
    :return: Login form
    """
    data = {}

    if request.user.is_authenticated:
        return HttpResponseRedirect("/")

    try:
        data['next'] = request.GET['next']
        return render(request, 'account/login.html', data)
    except KeyError:
        pass

    data['next'] = '/'
    return render(request, 'account/login.html', data)


@require_http_methods(["POST"])
def login_validate(request):
    """
    Validate login data
    :param request:
    :return: redirect to login page if error occurred or to next page from POST data
    """
    try:
        username = request.POST['username']
        password = request.POST['password']
        next_page = request.POST['redirect']
    except KeyError:
        return redirect('account:login')

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        messages.add_message(request, messages.INFO, "Zalogowano pomyślnie!")
        return HttpResponseRedirect(next_page)

    messages.add_message(request, messages.ERROR, "Błędny login i/lub hasło!")
    return redirect('account:login')


def logout_view(request):
    """
    Logout user
    :param request:
    :return: Redirect to main page
    """
    if request.user.is_authenticated:
        logout(request)
        messages.add_message(request, messages.INFO, "Wylogowano pomyślnie!")
    return redirect("memes:index")


def register_view(request):
    """
    Display register form
    :param request:
    :return: Register form
    """
    if request.user.is_authenticated:
        messages.add_message(request, messages.INFO, "Wyloguj się, aby utworzyć nowe konto.")
        return redirect("memes:index")
    return render(request, 'account/register.html', {})


@require_http_methods(["POST"])
def register_validate(request):
    """
        Validate register data and create new user
        :param request:
        :return: redirect to register page if error occurred or to main page
        """
    try:
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
    except KeyError:
        return redirect('account:register')

    try:
        User.objects.create_user(username, email, password)
        messages.add_message(request, messages.INFO, "Rejestracja powiodła się!")
        return redirect('memes:index')
    except IntegrityError:
        messages.add_message(request, messages.ERROR, "Taki użytkownik już istnieje!")
        return redirect('account:register')
