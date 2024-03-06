# from django.http import HttpResponse
from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, logout
from django.contrib.auth import logout
from .forms import UserRegistrationForm, \
  UserEditForm, ProfileEditForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def dashboard(request):
    return render(request,
                'account/dashboard.html',
                {'section': 'dashboard'})


def logout_view(request):
    logout(request)
    return redirect('/')

# def user_login(request):
#   if request.method == 'POST':
#     form = LoginForm
#     if form.is_valid():
#       cd = form.cleaned_data
#       user = authenticate(request,
#                           username=cd['username'],
#                           password=cd['password'])
#       if user is not None:
#         if user.is_activate:
#           login(request, user)
#           return HttpResponse('Аутентификация прошла успешно') 
#         else:
#           return HttpResponse('Аккаунт не существует')
#       else:
#         return HttpResponse('Неверный логин')
#   else:
#     form = LoginForm()
#   return render(request, 'account/login.html', {'form': form})  


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
          # Создать новый объект пользователя,
          # но пока не сохранять его
          new_user = user_form.save(commit=False)
          # Установить выбранный пароль
          new_user.set_password(
            user_form.cleaned_data['password'])
          # Сохранить объект User
          new_user.save()
          Profile.objects.create(user=new_user)
          return render(request,
                        'account/register_done.html',
                        {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})

@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user,
                                data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                      data=request.POST,
                                      files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated' \
                            'successfully')
        else:
            messages.error(request, 'Error updating your profile')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    
    return render(request,
                 'account/edit.html',
                 {'user_form': user_form,
                  'profile_form': profile_form} )




