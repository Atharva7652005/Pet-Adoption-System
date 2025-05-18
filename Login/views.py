from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def Pet_Login(request):
    if(request.method == "POST"):
        #Login Form Data Request
        user_login_username = request.POST.get("user_login_username")
        user_login_password = request.POST.get("user_login_password")

        if not User.objects.filter(username = user_login_username).exists():
            alert_message = f'No {user_login_username} Exist'
            return render(request,'Login.html', {'alert_message': alert_message})
        
        user = authenticate(username = user_login_username, password = user_login_password)

        if user is None:
            return render(request,'Login.html', {'alert_message': 'Invalid Credentials'})
        else:
            login(request, user)
            return redirect('/')

        #Login Form Data Request Ends Here
    return render(request,"Login.html")

def Pet_Signup(request):
    if(request.method == "POST"):
        #Sign Up Form Data Request
        user_name = request.POST.get("user_name")
        user_email = request.POST.get("user_email")
        user_password = request.POST.get("user_password")
        print("Form data received:", user_name, user_email)

        user = User.objects.filter(username = user_name)
        email_verify = User.objects.filter(email = user_email)

        if user.exists():
                return render(request, 'Signup.html', {'alert_message': 'Username already exists!'})
        elif email_verify.exists():
                return render(request, 'Signup.html', {'alert_message': 'Email Already Taken!'})
        else:
            if len(user_password) < 8:
                return render(request, 'Signup.html', {'alert_message': 'Password must contain atleast 8 characters'})
            elif not any(char.isupper() for char in user_password):
                return render(request, 'Signup.html', {'alert_message': 'Password must contain atleast  1 Uppercase letter'})
            elif not any(char.islower() for char in user_password):
                return render(request, 'Signup.html', {'alert_message': 'Password must contain atleast 1 Lowercase letter '})
            elif not any(char.isdigit() for char in user_password):
                return render(request, 'Signup.html', {'alert_message': 'Password must contain atleast 1 Digit'})
            elif not any(char in "!@#$%^&*(),.?\":{}|<>" for char in user_password):
                return render(request, 'Signup.html', {'alert_message': 'Password must contain atleast 1 special case letter'})
            else:
                user = User.objects.create_user(
                    username = user_name,
                    email = user_email,
                )
                user.set_password(user_password)
                user.save()

                send_mail(
                    'Thank You for Registering Pet Adoption System',
                    f'Dear {user_name}, Thank you for registering on Pet Adoption System! We’re thrilled to have you as part of our mission to support and uplift needful Animals.',
                    'settings.EMAIL_HOST_USER',
                    [user_email],
                    fail_silently=False
                )

                return render(request, 'index.html', {'alert_message': 'Account Created Sucessfully!'})
    
    return render(request,"Signup.html")

def logout_page(request):
    logout(request)
    request.session.flush()
    print("Session Data:", request.session.items())  # Debug session
    return redirect("/login")
    