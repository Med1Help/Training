from .models import Room
from .forms import RoomForm

class RoomCrud:
    def saveRoom(room):
        if room.is_valid():
            room.save()
            return True
        return False