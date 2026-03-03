from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout

# Create your views here.

@login_required
def notes_list(request):
    return render(request, "notes/notes_list.html")