from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import UserProfile
from django.contrib.auth import login, logout

def signup_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        college_id = request.POST.get('college_id')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        department = request.POST.get('department')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        # Check if College ID is already registered
        if UserProfile.objects.filter(college_id=college_id).exists():
            messages.error(request, "College ID already registered!")
            return redirect('signup')

        # Store user in database with a hashed password
        user = UserProfile.objects.create(
            name=name,
            college_id=college_id,
            email=email,
            phone=phone,
            department=department,
            password=make_password(password)  # Hash password for security
        )

        messages.success(request, "Signup successful! Please log in.")
       # return redirect('login')

    return render(request, "signup.html")




def login_view(request):
    if request.method == "POST":
        college_id = request.POST.get('college_id')
        password = request.POST.get('password')

        print("Login attempt with:", college_id)  # Debugging

        try:
            user = UserProfile.objects.get(college_id=college_id)  # Get user by College ID
            if check_password(password, user.password):  # Verify password
                request.session['user_id'] = user.user_id  # Store user ID in session
                messages.success(request, "Login successful!")

                print("Login successful for:", user.name)  # Debugging

              #  return redirect('home')  
            else:
                messages.error(request, "Invalid password!")
                print("Invalid password attempt.")  # Debugging
        except UserProfile.DoesNotExist:
            messages.error(request, "User with this College ID does not exist!")
            print("User does not exist.")  # Debugging

    return render(request, "login.html")


def home_view(request):
    return render(request,"marketplace/home.html")



def logout_view(request):
    request.session.flush()  # Clear session
    messages.success(request, "You have been logged out.")
    return redirect('login')
