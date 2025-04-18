from django.shortcuts import render
from .models import UserProfile , Log_Usage
from django.contrib.auth.models import User
from django.contrib.auth import login , authenticate , logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect as hrr 
from django.urls import reverse
from datetime import datetime , timedelta


def custom_404(req , exception):
  return render(req , "404.html")


def detect_device_brand(req):
    user_agent = req.META.get("HTTP_USER_AGENT", "").lower()
   

    # Expanded list of laptop brands
    laptop_brands = [
        "mac", "hp", "dell", "lenovo", "acer", "asus", "msi", "samsung", 
        "sony", "toshiba", "razer", "gigabyte", "huawei", "lg", "alienware", "microsoft"
    ]
    
    # Mobile brands remain the same
    mobile_brands = ["android", "iphone"]

    # Check if the device is a laptop
    for brand in laptop_brands:
        if brand in user_agent:
            return brand.capitalize()  # Returns "Mac", "HP", "Dell", etc.

    # Check if the device is a mobile phone
    for brand in mobile_brands:
        if brand in user_agent:
            return brand.capitalize()  # Returns "Android" or "iPhone"

    return "Unknown Device"  # If none of the brands match




@login_required
def homepage(req):
  user = UserProfile.objects.get(user = req.user)
  context= {"userprofile": user  }
  ip = ""
  x_forwarded_for = req.META.get('HTTP_X_FORWARDED_FOR')
  if x_forwarded_for:
     ip = x_forwarded_for.split(',')[0]  # Get first IP in case of proxies
  else:
      ip = req.META.get('REMOTE_ADDR') 
  
  
  print(ip)

  print("Device : => " , detect_device_brand(req))
  
  return render(req , "homepage.html" , context=context)

@login_required
def edit_profile(req):
  
  userprofile =  UserProfile.objects.get(user = req.user)
  context = {"userprofile" : userprofile , "form_action" : reverse("portal:edit_profile")}

  print(req.POST)
  username_already_exist = None
  email_already_exist = None
  RegNo_already_exist = None

  if req.POST.get("username") != req.user.username:
    try:
      username_already_exist = User.objects.get(username = req.POST.get("username"))
    except:
       ... # pass
  if req.POST.get("email") != req.user.email:
    try:
      email_already_exist = User.objects.get(email = req.POST.get("email"))

    except:
      ... # pass

  if req.POST.get("registration_number") != userprofile.RegNo:
    try:
      RegNo_already_exist = UserProfile.objects.get(RegNo = req.POST.get("registration_number"))
  
    except:
      ...  # pass


  if username_already_exist:
     return render(req , "signup.html" ,context= {"form_action" : reverse("portal:edit_profile") ,"Username" : "In Use"})
  
  elif email_already_exist:
     return render(req , "signup.html" ,context= {"form_action" : reverse("portal:edit_profile") ,"Email" : "In Use"})
     
  elif RegNo_already_exist:
     return render(req , "signup.html" ,context= {"form_action" : reverse("portal:edit_profile") ,"RegistrationNumber" : "In Use"})
     
  else:
     
     if authenticate(username = "apple" , password = req.POST.get("adminpassword")):
        # before creating a new user confirm that that person a is admin
        # or has access to admin dashboard
        get_user = User.objects.get(username = req.user.username)
        get_user.username = req.POST.get("username")
        get_user.first_name = req.POST.get("firstname")
        get_user.last_name = req.POST.get("lastname")
        get_user.email = req.POST.get("email")
        print("i got here " , get_user)

        if req.POST.get("personal_password"):
          get_user.set_password(req.POST.get("personal_password"))
          login(req,authenticate(username = get_user.username , password = req.POST.get("personal_paswword")))
        
        get_user.save()
        
        profile = UserProfile.objects.get(user = get_user ) 
        profile.RegNo = req.POST.get("registration_number")
        if "image" in req.FILES:
          profile.display_pic = req.FILES["image"]

        profile.save()
        return hrr(reverse("portal:homepage"))
   

  return render(req , "editprofile.html"  , context=context)

@login_required
def checkuseractivites(req):
    if req.method == "GET":
       all_log = Log_Usage.objects.all().order_by("-date")
       return render(req, "check_user_activities.html" , context ={"userquery":all_log})
    # i.e it is a post request
    else:
      start_date = req.POST.get("start_date", (datetime.today() - timedelta(weeks=1)).strftime("%Y-%m-%d"))
      end_date = req.POST.get("end_date", datetime.today().strftime("%Y-%m-%d"))  # Convert to string
   
      date1 = datetime.strptime(start_date, "%Y-%m-%d")  # Use None instead of an empty string
      date2 = datetime.strptime(end_date, "%Y-%m-%d")  # Now it's always a string, so no error
    
      if date1 > date2:
        return render(req, "check_user_activities.html", context={"Invalid": "Start Date should be lesser"})

      else:
        if req.POST.get("registration_number"):
          # check if reg number is in the post field
          try:
              # confirm if it is correct
              userprofile = UserProfile.objects.get(RegNo = req.POST.get("registration_number"))
      
          except UserProfile.DoesNotExist:
            #if not correct
            # return invalid registration number
            return render(req, "check_user_activities.html", context={"Invalid": "Invalid Reg Number"})
        
          else:
            # return all the query from the start date to the end date for the
            # registration number 

            query = userprofile.profile.filter(date__range = (date1 , date2)).order_by("-date")
            
            return render (req , "check_user_activities.html" , context={"userquery":query})
          
        else:
           #if registration number is not specified
           # return a query of all log from the start date to 
           # the end date for all user
           all_log = Log_Usage.objects.filter(date__range = (date1 , date2)).order_by("-date")
           
           return render(req, "check_user_activities.html", context={"userquery":all_log})
           

def createuser(req):
  context = {"form_action" : reverse("portal:createuser")}
  default_password = "123456789"
  
  username_already_exist = None
  email_already_exist = None
  RegNo_already_exist = None
  try:
    username_already_exist = User.objects.get(username = req.POST.get("username"))
  except:
     ... # pass

  try:
     email_already_exist = User.objects.get(email = req.POST.get("email"))

  except:
     ... # pass

  try:
     RegNo_already_exist = UserProfile.objects.get(RegNo = req.POST.get("registration_number"))
  
  except:
     ...  # pass


  if username_already_exist:
     return render(req , "signup.html" ,context= {"form_action" : reverse("portal:createuser") ,"Username" : "In Use"})
  
  elif email_already_exist:
     return render(req , "signup.html" ,context= {"form_action" : reverse("portal:createuser") ,"Email" : "In Use"})
     
  elif RegNo_already_exist:
     return render(req , "signup.html" ,context= {"form_action" : reverse("portal:createuser") ,"RegistrationNumber" : "In Use"})
     
  else:
     
     if authenticate(username = "apple" , password = req.POST.get("password")):
        # before creating a new user confirm that that person a is admin
        # or has access to admin dashboard
        
        new_user = User.objects.create(username = req.POST.get("username"),
                                       first_name = req.POST.get("firstname"),
                                       last_name = req.POST.get("lastname"),
                                       email = req.POST.get("email"))
        new_user.set_password(default_password)
        new_user.save()
        profile = UserProfile.objects.create(user = new_user , 
                                             RegNo = req.POST.get("registration_number"))
        profile.display_pic = req.FILES["image"]

        profile.save()
        authenticated_user = authenticate(username = new_user.username , password = default_password)

        if authenticated_user:
           login(req , authenticated_user)
           return hrr(reverse("portal:homepage"))
        
      
                              

  return render(req , "signup.html" ,context= context)


def login_(req):
    
    if req.method == "POST":
        reg_no_or_email = req.POST.get("email")
        password = req.POST.get("password")
        user = ""
        username = ""

        """ Checking if the Username Exists"""
        if "@" in reg_no_or_email:
            try:
             
              user =  User.objects.get(email = reg_no_or_email) # the user logined in with email
            except :
                return render(req ,"signin.html" , context={"Email":"Email Does Not Exists" , "form_action":reverse("portal:login")})
            else:
              username = user.username
        
        else :
            try:
              user = UserProfile.objects.get(RegNo = reg_no_or_email)
            
            except:
              return render(req ,"signin.html" , context={"Email":"Invalid Registration Number", "form_action":reverse("portal:login")})
            
            else:
              username = user.user.username
         
        authenticated_user = authenticate(username = username , password = password)
       

        if authenticated_user:
            login(req , authenticated_user)
           
            return hrr(reverse("portal:homepage"))
          
        else :
           # if authenticated_user returns None this implies that the password is wrong
           # the reason for concluded that password is incorrect not username
           # is because the Username has being verified before in the try block

           return render(req ,"signin.html" , context={"Password":"Incorrect Password", "form_action":reverse("portal:login")})
                  
        # Handles POST request
    # Initial GET Request
    return render(req, "signin.html", context={"form_action":reverse("portal:login")})  # Handles GET request too
 
@login_required
def logout_(req):
   
  logout(req)
  
  return hrr(reverse("portal:login"))