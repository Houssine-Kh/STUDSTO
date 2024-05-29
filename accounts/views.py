from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.shortcuts import HttpResponseRedirect
from .Forms import VotreUserCreationForm
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth.models import User



def signup(request):
    if request.method == 'POST':
        # Extract user-related data from the form
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Create a new user in the default authentication user table
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = request.POST.get('firstname')
        user.last_name = request.POST.get('lastname')
        user.save()

        # Create a UserProfile linked to the new user
        user_profile = UserProfile.objects.create(
            user=user,
            firstName=request.POST.get('firstname'),
            lastName=request.POST.get('lastname'),
            address=request.POST.get('address'),
            city=request.POST.get('City'),
            phoneNumber=request.POST.get('phoneNumber'),  # Add this line
            ProfilePic=request.FILES.get('Pprofile'),  # Add this line
        )

        messages.success(request, f'Le compte de {username} a été bien créé')
        return redirect('/')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})



def signup2(request):
    if request.method == 'POST':
        form = VotreUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            
            messages.success(request, f'Le compte de {username} a été bien créé')
            return redirect('/')
    else:
        form = VotreUserCreationForm()

    return render(request, 'signup.html', {'form': form})

   
def home(request): 
    return render(request, 'home/home.html')
   
  
def signin(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/') #profile
        else:
            msg = 'Error Login'
            form = AuthenticationForm(request.POST)
            return render(request, 'login.html', {'form': form, 'msg': msg})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})
  
def profile(request): 
    return render(request, 'profile.html')

   
def signout(request):
    logout(request)
    return redirect('/home')