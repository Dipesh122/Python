from multiprocessing import context
from shutil import move
from urllib import request
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from app.forms import MovieForm
from .models import Movie
from django.contrib.auth import authenticate, login
# Create your views here.
def home(request):
    return HttpResponse("Home Page")

def number(reuqest, id):
    return HttpResponse("Number: "+str(id))

def template_test(request):
    return render(request, 'index.html')

def get_movie_info(request, id):
    try:
        movie = Movie.objects.get(id=id)

        context = {
            'is_favorite': False
        }

        if movie.favorite.filter(pk=request.user.pk).exists():
            context['is_favorite'] = True

        return render(request, 'movie.html', {'movie':movie, 'context': context,})
    except Movie.DoesNotExist:
        return render(request, '404.html')
        
def get_movies(request):
    movies = Movie.objects.all()
    return render(request, 'movies.html', {'movies': movies})

def post_movie(request):
    form = MovieForm()

    if request.method == "POST":
        movie_form = MovieForm(request.POST)

        if movie_form.is_valid():
            movie_form.save()

        return redirect('/movies/')
    return render(request,'post_movie.html', {'form':form})

def signin(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data = request.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            login(request, user)
            return redirect('/movies/')

    return render(request, 'signin.html', {'form': form})

def add_to_favorite(request, id):
    movie = Movie.objects.get(id=id)
    movie.favorite.add(request.user)
    return redirect('/movies/{0}'.format(id))

def remove_from_favorites(request, id):
    movie= Movie.objects.get(id=id)
    movie.favorite.remove(request.user)

    return redirect('/movies/{0}'.format(id))

def get_user_favorites(request):
    movies = request.user.favorite.all()
    return render(request, 'user_favorite.html',{'movies': movies})
