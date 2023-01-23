
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout




# Create your views here.
def home(request):
    return render(request, "account/index.html")

def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
    
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username")
            return redirect('home')
        
        if User.objects.filter(email=email):
            messages.error(request, "Email already registered! ")
            return redirect('home')
        
        if len(username)>10:
            messages.error(request, "Username must be under 10 character")
            
        if pass1 != pass2:
            messages.error(request, "Password didn't match!")
            
        if not username.isalnum():
            messages.error(request, "Usernaem must be Alpha-Numeric!")
            return redirect('home')
                
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()
        
        messages.success(request, "Your Account has been successfully created.")
        
        
        
        return redirect('/login')
    return render(request, "account/signup.html")

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "account/index.html", {'fname':fname})
        else:
            messages.success(request, "LogIn successfully!")
            return redirect('home')
    return render(request, "account/login.html")

def logout_view(request):
    logout(request)
    messages.success(request, "Logged Out successfully!")
    return redirect('home')


        
        