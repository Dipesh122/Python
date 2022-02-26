from multiprocessing import context
from shutil import move
from urllib import request
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from .forms import MovieForm,ReviewForm
from .models import Movie, Review
from django.contrib.auth import authenticate, login
import math
# Create your views here.
def home(request):
    return HttpResponse("Home Page")

def number(reuqest, id):
    return HttpResponse("Number: "+str(id))

def template_test(request):
    return render(request, 'index.html')

def get_movie_info(request, id):
    try:
        review_form = ReviewForm()
        if request.method == 'POST':
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review=review_form.save(commit=False)
                review.movie_id = id            
                review.user_id = request.user.id
                review.save()
                
        movie = Movie.objects.get(id=id)

        context = {
            'is_favorite': False
        }

        if movie.favorite.filter(pk=request.user.pk).exists():
            context['is_favorite'] = True

        return render(request, 'movie.html', {'review_form': review_form, 'movie':movie, 'context': context,})
    except Movie.DoesNotExist:
        return render(request, '404.html')
        
def get_movies(request, page_number):
    page_size = 1

    if page_number < 1:
        page_number = 1

    movie_count = Movie.objects.count()

    last_page = math.ceil(movie_count / page_size)

    pagination = {
        'previous_page': page_number -1,
        'current_page': page_number,
        'next_page': page_number + 1,
        'last_page': last_page
    }
    movies = Movie.objects.all()[(page_number-1)* page_size:page_number * page_size]

    return render(request, 'movies.html', {'movies': movies, 'pagination':pagination})

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
