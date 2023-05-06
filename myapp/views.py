from django.shortcuts import render
from django.http import HttpResponse

rooms = [
    {'id':1,'name':'java dev'},
    {'id':2,'name':'php dev'},
    {'id':3,'name':'spring boot framework'},
]

def home(request):
    return render(request,'myapp/home.html',{'rooms':rooms})
def room(request,id):
    room = None
    for i in rooms:
        if i['id'] == int(id) :
            room = i

    return render(request,'myapp/room.html',{'room':room})
