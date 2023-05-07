from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import Room
from .forms import RoomForm 
from .RoomCrud import RoomCrud

def home(request):
    rooms = Room.objects.all()
    return render(request,'myapp/home.html',{'rooms':rooms})

def room(request,id):
    rooms = Room.objects.all()
    for i in rooms:
        if i.id == int(id) :
            room = i

    return render(request,'myapp/room.html',{'room':room})

def createRoom(request):
    form    = RoomForm()
    if(request.method == 'POST'):
        form = RoomForm(request.POST)
        check = RoomCrud.saveRoom(form)
        if(check):
           return redirect('home')

    context = {'form':form}
    return render(request,'myapp/room_form.html',context=context)

def updateRoom(request,roomId):
    room  = Room.objects.get(id=roomId)
    form  = RoomForm(instance=room)
    check =  False
    if request.method == 'POST':
        form = RoomForm(request.POST,instance=room)
        check = RoomCrud.saveRoom(form)
    if check:
        return redirect('home')
    context = {'form':form}
    return render(request,'myapp/room_form.html',context)

def deleteRoom(request,roomId):
    room = Room.objects.get(id=roomId)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'room' : room}
    return render(request,'myapp/delete.html',context)
