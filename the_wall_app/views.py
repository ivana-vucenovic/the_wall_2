from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, UserManager, Wall_Message, Comment
import bcrypt

def index(request):
    request.session.flush()
    return render(request, 'index.html')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'wall_messages': Wall_Message.objects.all()
    }
    return render(request, 'success.html', context)

def register_user(request):
    if request.method == 'POST':
        errors=User.objects.registration_validator(request.POST)
        if len(errors) >0:
            for key,value in errors.items():
                messages.error(request, value)
            return redirect('/')
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt(rounds = 10)).decode()
        new_user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=pw_hash,
        )
        request.session['user_id'] = new_user.id
        return redirect('/detales')
    return redirect('/')

def login_user(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request, value)
            return redirect('/')
        this_user = User.objects.filter(email=request.POST['email'])
        request.session['user_id'] = this_user[0].id
        return redirect('/success')
    return redirect('/')

def detales(request):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.filter(id=request.session['user_id'])
    context = {
        'user': this_user[0]
    }
    return render(request, 'detales.html', context)

def post_mess(request):
    Wall_Message.objects.create(
        message=request.POST['mess'], 
        poster=User.objects.get(id=request.session['user_id']))
    return redirect('/success')

def post_comment(request, id):
    poster = User.objects.get(id=request.session['user_id'])
    message = Wall_Message.objects.get(id=id)
    Comment.objects.create(
        comment=request.POST['comment'], 
        poster=poster, 
        wall_message=message)
    return redirect('/success')

def profile(request, id):
    context = {
        'user': User.objects.get(id=id)
    }
    return render(request, 'detales.html', context)

def add_like(request, id):
    liked_message = Wall_Message.objects.get(id=id)
    user_liking = User.objects.get(id=request.session['user_id'])
    liked_message.user_likes.add(user_liking)
    return redirect('/success')

def delete_comment(request, id):
    destroyed = Comment.objects.get(id=id)
    destroyed.delete()
    return redirect('/success')

def edit(request, id):
    edit_user = User.objects.get(id=id)
    edit_user.first_name = request.POST['first_name']
    edit_user.last_name = request.POST['last_name']
    edit_user.email = request.POST['email']
    edit_user.save()
    return redirect('/success')

def logout(request):
    request.session.flush()
    return redirect('/')