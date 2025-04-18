from django.urls import path, re_path
from .views import login_ , homepage , logout_ , createuser , edit_profile ,checkuseractivites
app_name = "portal"

urlpatterns = [
    path("login" , view=login_ , name= "login"),
    path("homepage" , view = homepage , name="homepage"),
    path("logout" , view = logout_ , name = "logout"),
    path("createuser" , view= createuser , name = "createuser"),
    path("edit_profile" , view=edit_profile , name ="edit_profile"),
    path("userlog" , view= checkuseractivites , name ="checkuseractivities")
    
]