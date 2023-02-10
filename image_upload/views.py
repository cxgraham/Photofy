from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
from .models import *
from .forms import *

import bcrypt


# USER LOGIN & REGISTRATION  
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        errors = User.objects.user_validator(request.POST)
        if len(errors) > 0:
            print(errors)
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/register')
        else:
            email = request.POST['email'].lower()
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            print(pw_hash)
            created_user = User.objects.create(username = request.POST['username'], email = email, password = pw_hash)
            request.session['user_id'] = created_user.id
            created_user.save()
            print(created_user)
            return redirect('/homepage')

def login(request):
    user = User.objects.filter(username=request.POST['username'])
    if user:
        logged_user = user[0]
        print(logged_user)
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
        return redirect('/homepage')
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')


# PAGE / TEMPLATE VIEWS
def index(request):
    return render(request, 'initial_login.html')

def nav(request):
    this_user = User.objects.get(id = request.session['user_id'])
    context = {
        'username': this_user.username,
    }
    return render(request, 'navbar.html', context)

def homepage(request):
    this_user = User.objects.get(id = request.session['user_id'])
    context = {
        'username':  this_user.username,
        'form': PhotoForm(),
        'photos': this_user.photos.all(),
    }
    return render(request, 'homepage.html', context)

def user_profile(request, id):
    this_user = User.objects.get(id = request.session['user_id'])
    user_profile = User.objects.get(id=id)
    context = {
        'username': this_user.username,
        'user_profile': user_profile,
    }
    return render(request, 'user_profile.html', context)



# PHOTO VIEWS 
def add_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            this_user = User.objects.get(id = request.session['user_id'])
            form.instance.user = this_user
            form.save()
            print(request.FILES)
            print(request.session['user_id'])
            return redirect('/homepage')
    return redirect('/homepage')

def edit_photo(request, id):
    this_photo = Photo.objects.get(id=id)
    this_user = User.objects.get(id=request.session['user_id'])
    form = PhotoForm(instance=this_photo)
    if request.method == 'POST':
        form = PhotoForm(request.POST, instance = this_photo)
        if form.is_valid():
            form.save()
            return redirect('/homepage')
    context = {
        'photo': this_photo,
        'username': this_user.username,
        'form': form,
    }
    return render(request, 'view_photo.html', context)

def view_all_photos(request):
    all_photos = Photo.objects.all()
    this_user = User.objects.get(id=request.session['user_id'])
    context = {
        'photos': all_photos,
        'username': this_user.username,
    }
    return render(request, 'all_photos.html', context)

def delete_photo(request, id):
    this_photo = Photo.objects.get(id=id)
    this_photo.delete()
    return redirect('/homepage')