from django.shortcuts import render, redirect
from newsapi import NewsApiClient
from myapp import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)

from .forms import UserLoginForm, UserRegisterForm


def home(request):
    API_KEY = "0c6d46cd105a4eec899d842768e0a84e"
    newsApi = NewsApiClient(API_KEY)
    headLines = newsApi.get_top_headlines(sources='bbc-news')

    desc = []
    news = []
    img = []
    articles = headLines['articles']
    for i in range(len(articles)):
        article = articles[i]

        desc.append(article['description'])
        news.append(article['title'])
        img.append(article['urlToImage'])

        mylist = zip(desc, news, img)
    return render(request, 'home.html', context={"mylist": mylist})


def index(request):
    API_KEY = "0c6d46cd105a4eec899d842768e0a84e"
    newsApi = NewsApiClient(API_KEY)
    headLines = newsApi.get_top_headlines(sources='ign, cnn')

    desc = []
    news = []
    img = []
    articles = headLines['articles']
    for i in range(len(articles)):
        article = articles[i]

        desc.append(article['description'])
        news.append(article['title'])
        img.append(article['urlToImage'])

        mylist = zip(desc, news, img)
    return render(request, 'index.html', context={"mylist": mylist})


# setting up Autheer
@login_required
def layout(request):
    return render(request, 'layout.html', {})


def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')

    context = {
        'form': form,
    }
    return render(request, "login.html", context)


def register_view(request):
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect('/')

    context = {
        'form': form,
    }
    return render(request, "register.html", context)


def logout_view(request):
    logout(request)
    return redirect('/')
