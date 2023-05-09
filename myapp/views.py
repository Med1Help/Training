from django.shortcuts import render , redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from .models import Room ,Topic
from .forms import RoomForm 
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
            messages.error(req,'An error occurred during registration')
    context = {'form': form}
    return render(req,'myapp/signup_form.html',context)

def home(request):
    rooms   = None
    q = request.GET.get('q')
    if request.GET.get('q') != None:
        rooms   = Room.objects.filter(
            Q(topic__name__contains=q) |
            Q(name__contains = q) |
            Q(description__contains = q)
                                      )
    else:
        rooms   = Room.objects.all()
    topics  = Topic.objects.all() 
    return render(request,'myapp/home.html',{'rooms':rooms , 'topics' : topics})

def room(request,id):
    rooms = Room.objects.all()
    for i in rooms:
        if i.id == int(id) :
            room = i

    return render(request,'myapp/room.html',{'room':room})

@login_required(login_url='login_view')
def createRoom(request):
    form    = RoomForm()
    if(request.method == 'POST'):
        form = RoomForm(request.POST)
        check = RoomCrud.saveRoom(form)
        if(check):
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
    context = {'room' : room}
    return render(request,'myapp/delete.html',context)
