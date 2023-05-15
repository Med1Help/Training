from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('signup/',views.signupView,name="signup_view"),
    path('login/',views.loginView,name="login_view"),
    path('logout/',views.logoutUser,name="logout_view"),
    path('room/<str:id>/',views.room,name="room"),
    path('create-room/',views.createRoom,name="create_room"),
    path('update-room/<str:roomId>',views.updateRoom,name="update-room"),
    path('delete-room/<str:roomId>',views.deleteRoom,name="delete-room"),
    path('delete-message/<str:messageId>',views.deleteMessage,name="delete-message"),
    path('user-profile/<str:profileId>',views.profileView,name="user-profile")
]