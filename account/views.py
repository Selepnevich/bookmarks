from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm
# Create your views here.

def user_login(request):
  if request.method == 'POST':
    form = LoginForm
    if form.is_valid():
      cd = form.cleaned_data
      user = authenticate(request,
                          username=cd['username'],
                          password=cd['password'])
      if user is not None:
        if user.is_activate:
          login(request, user)
          return HttpResponse('Аутентификация прошла успешно') 
        else:
          return HttpResponse('Аккаунт не существует')
      else:
        return HttpResponse('Неверный логин')
  else:
    form = LoginForm()
  return render(request, 'account/login.html', {'form': form})  
        