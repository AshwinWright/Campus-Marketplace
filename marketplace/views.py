from django.shortcuts import render, redirect , get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import UserProfile
from django.contrib.auth import login, logout
from django.http import JsonResponse
from .models import Product
import logging
import json


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
    
    if request.session.get('is_authenticated'):
        return redirect('profile')
    
    if request.method == "POST":
        college_id = request.POST.get('college_id')
        password = request.POST.get('password')

        next_url = request.POST.get("next") or request.GET.get("next")
        if not next_url:
            next_url = "/home/"  # Default redirect if no 'next' parameter

        print("Login attempt with:", college_id)  # Debugging

        try:
            user = UserProfile.objects.get(college_id=college_id)  # Get user by College ID
            if check_password(password, user.password):  # Verify password
                request.session['user_id'] = user.user_id  # Store user ID in session
                request.session['user_name'] = user.name
                request.session['college_id'] = user.college_id
                request.session['email'] = user.email
                request.session['phone'] = user.phone
                request.session['department'] = user.department
                request.session['is_authenticated'] = True  # Custom flag
                messages.success(request, "Login successful!")

                print("Login successful for:", user.name)  # Debugging

               # next_url = request.GET.get('next', 'home')  # Default is 'home'
                return redirect(next_url)

            else:
                messages.error(request, "Invalid password!")
                print("Invalid password attempt.")  # Debugging
        except UserProfile.DoesNotExist:
            messages.error(request, "User with this College ID does not exist!")
            print("User does not exist.")  # Debugging

    return render(request, "login.html")


def home_view(request):
    products = Product.objects.all()

    # Render home.html and pass the product data
    return render(request, "marketplace/home.html", {"products": products})


def logout_view(request):
    request.session.flush()  # Clear session
    messages.success(request, "You have been logged out.")
    return redirect('login')



logger = logging.getLogger(__name__)  # Enable logging for debugging

def post_ad(request):
    """Handles both rendering the form (GET) and saving product data (POST)."""

    if not request.session.get("user_id"):  # Ensure user is logged in
        if request.method == "GET":
            return redirect("/login/")  # Redirect to login if accessing the page
        return JsonResponse({
            "error": "User not logged in!",
            "login_url": "/login/"
        }, status=403)  # JSON response for AJAX calls

    if request.method == "GET":
        return render(request, "create_ad.html")

    if request.method == "POST":
        try:
            title = request.POST.get("title")
            description = request.POST.get("description")
            price = request.POST.get("price")
            year = request.POST.get("year")  # ✅ Get year from form
            department = request.POST.get("department")  # ✅ Get department from form
            product_type = request.POST.get("product_type")

            logger.info(f"Received Product: {title}, {description}, {price}, {year}, {department}, {product_type}")

            # Save product to database
            Product.objects.create(
                title=title,
                description=description,
                price=price,
                year=year,  # ✅ Save year
                department=department,  # ✅ Save department
                product_type=product_type,  # ✅ Save product type
                user_id=request.session["user_id"],  # Ensure this exists
                status="available"
            )

            logger.info("Product successfully added to database.")
            return JsonResponse({"message": "Product added successfully!"})

        except Exception as e:
            logger.error(f"Error saving product: {e}")
            return JsonResponse({"error": "Something went wrong!"}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)



def profile_view(request):
    if not request.session.get('is_authenticated'):
        return redirect('/login/?next=/profile/')  # Redirect to login with return URL

    try:
        user = UserProfile.objects.get(user_id=request.session.get('user_id'))
    except UserProfile.DoesNotExist:
        request.session.flush()  # Clear invalid session
        return redirect('/login/?next=/profile/')

    return render(request, 'profile.html', {'user': user})


def update_profile(request):
    """ Allow the user to update only their name """
    if request.method == "POST" and request.session.get('is_authenticated'):
        try:
            user = UserProfile.objects.get(user_id=request.session.get('user_id'))
            data = json.loads(request.body)
            new_name = data.get("name")

            if new_name:
                user.name = new_name
                user.save()
                return JsonResponse({"success": True, "new_name": new_name})

        except UserProfile.DoesNotExist:
            return JsonResponse({"success": False, "error": "User not found"}, status=400)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)



def product_view(request, product_id):
    """Fetch and display a single product's details."""
    product = get_object_or_404(Product, id=product_id)
    seller = get_object_or_404(UserProfile, user_id=product.user_id)  # Fetch seller info
    return render(request, "product.html", {"product": product, "seller": seller})