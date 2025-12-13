from django.shortcuts import render, redirect
from .models import Comment

# Create your views here.

def index(request):
    return render(request, 'products_store/index.html')

def tools(request):
    comments = {
        'comments': Comment.objects.all(),
    }
    return render(request, 'products_store/tools.html', comments)

def contact(request):
    return render(request, 'products_store/contact.html')