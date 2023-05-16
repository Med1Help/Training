from django.shortcuts import render , redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from .models import Room, Topic, Message
from .forms import RoomForm, MessageForm ,UserForm
from .RoomCrud import RoomCrud
from  django.contrib.auth.forms import UserCreationForm

def loginView(request):
    context = {}
    if(request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'User Doesn''t exist')
            return render(request,'myapp/login_form.html',context)
        user = authenticate(request,username=username,password=password)  
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Password Doesn''t matche') 

    
    return render(request,'myapp/login_form.html',context)

def logoutUser(req):
    logout(req)
    return redirect('home')

def signupView(req):
    form = UserCreationForm()
    if req.method == 'POST':
        form = UserCreationForm(req.POST)
        if form.is_valid():
            user            = form.save(commit=False)
            user.username   = user.username.lower()
            user.save()
            login(req,user)
            return redirect('home')
        else:
            print(form)
            messages.error(req,'An error occurred during registration')
    context = {'form': form}
    return render(req,'myapp/signup_form.html',context)

@login_required(login_url='login_view')
def update_user(req):
    user = req.user
    form = UserForm(instance=user)
    if req.method == 'POST':
        form = UserForm(req.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile',user.id)  

    context = {'form':form}
    return render(req,'myapp/update_user.html',context)

def home(request):
    rooms   = None
    q = request.GET.get('q')
    if request.GET.get('q') != None:
        rooms   = Room.objects.filter(
            Q(topic__name__contains=q) |
            Q(name__contains = q) |
            Q(description__contains = q)
                                      )
        recent_messages = Message.objects.filter(
        Q(room__topic__name__contains=q)
        )
    else:
        rooms   = Room.objects.all()
        recent_messages = Message.objects.all()
    topics          = Topic.objects.all() 
    
    return render(request,'myapp/home.html',{'rooms':rooms , 'topics' : topics , 'recent_messages':recent_messages})

def room(request,id):
    rooms = Room.objects.all()
    form = MessageForm()
    for i in rooms:
        if i.id == int(id) :
            room = i   
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',room.id)
    participants  = room.participants.all()
    room_messages = room.message_set.all()          
    context = {'room':room,'room_messages':room_messages,'participants':participants}
    return render(request,'myapp/room.html',context)

@login_required(login_url='login_view')
def createRoom(request):
    form    = RoomForm()
    if(request.method == 'POST'):
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit = False)
            room.host = request.user
            room.save()
            return redirect('home')

    context = {'form':form}
    return render(request,'myapp/room_form.html',context=context)

@login_required(login_url='login_view')
def updateRoom(request,roomId):
    room  = Room.objects.get(id=roomId)
    form  = RoomForm(instance=room)
    check =  False
    if request.user != room.host:
        return HttpResponse('You are not allowed to update this room !! ')
    if request.method == 'POST':
        form = RoomForm(request.POST,instance=room)
        check = RoomCrud.saveRoom(form)
    if check:
        return redirect('home')
    context = {'form':form}
    return render(request,'myapp/room_form.html',context)

@login_required(login_url='login_view')
def deleteRoom(request,roomId):
    room = Room.objects.get(id=roomId)
    if request.user != room.host:
        return HttpResponse('You are not allowed to update this room !! ')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj' : room}
    return render(request,'myapp/delete.html',context)

@login_required(login_url='login_view')
def deleteMessage(request,messageId):
    message = Message.objects.get(id=messageId)
    if request.user != message.user:
        return HttpResponse('You are not allowed to update this room !! ')
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    context = {'obj' : message}
    return render(request,'myapp/delete.html',context)

def profileView(req,profileId):
    user          =  User.objects.get(id=profileId)
    user_rooms    =  Room.objects.filter(Q(host=profileId))
    topics        =  Topic.objects.all()
    room_messages =  user.message_set.all()
    context       = {
        'profile_user':user ,
        'rooms' : user_rooms,
        'topics' : topics,
        'room_messages' : room_messages
        }
    return render(req,'myapp/profile.html',context)

def topics(req):
    topics = Topic.objects.all()
    context = {'topics':topics}
    return render(req,'myapp/topics.html',context)
def activities(req):
    activities = Message.objects.all()
    context = {'recent_messages':activities}
    return render(req,'myapp/activity.html',context)
