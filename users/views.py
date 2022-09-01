from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from .forms import UserRegisterForm, AccountUpdateForm, UserUpdateForm
from .models import Account


def user_register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successful')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                messages.error(request, 'You have not logged in')
        else:
            return HttpResponse("Username or password is not correct ")
    else:
        return render(request, 'users/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


@login_required
def account(request):
    user_account = Account.objects.get(user=request.user)

    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, request.user)
        p_form = AccountUpdateForm(request.POST, request.FILES, request.user)
        if u_form.is_valid() and p_form.is_valid():
            user = u_form.save(commit=False)
            user.save()

            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(request.user)
        p_form = AccountUpdateForm(request.user)
    context = {
        'user_account': user_account,
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, "users/account.html", context)



