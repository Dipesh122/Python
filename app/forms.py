from dataclasses import fields
import imp
from django import forms
from .models import Movie, Review

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'budget', 'genres']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review']