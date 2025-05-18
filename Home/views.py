from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import *;

# Create your views here.
def Pet_Home(request):
    pet_type = request.POST.get('pet_type')
    pet_age_type = request.POST.get('pet_age_type')
    pet_size = request.POST.get('pet_size')

    if pet_type or pet_age_type or pet_size:
        queryset = Pet_Adoption.objects.all()
        if pet_type:
            queryset = queryset.filter(pet_type=pet_type)
        if pet_age_type:
            queryset = queryset.filter(pet_age_type=pet_age_type)
        if pet_size:
            queryset = queryset.filter(pet_size=pet_size)
    else:
        queryset = Pet_Adoption.objects.all()[:4]

    contact = Contact_Form.objects.all()[:3]
    return render(request,"index.html",{"Pets" : queryset,"Contacts": contact})

def Pet_Detail(request,id):
    queryset = Pet_Adoption.objects.get(id=id)
    return render(request,"pet-detail.html",{"Pet":queryset})

def Pet_List(request):
    queryset = Pet_Adoption.objects.all().order_by('-timestamp')

    if request.POST.get('All'):
        return render(request,"pets.html",{"Pets":queryset})

    if request.method == "POST":
        pet_type = request.POST.get('pet_type')
        pet_age_type = request.POST.get('pet_age_type')
        pet_size = request.POST.get('pet_size')
        pet_gender = request.POST.get('pet_gender')

        if pet_type or pet_age_type or pet_size or pet_gender:
            queryset = Pet_Adoption.objects.all()
            if pet_type:
                queryset = queryset.filter(pet_type=pet_type)
            if pet_age_type:
                queryset = queryset.filter(pet_age_type=pet_age_type)
            if pet_size:
                queryset = queryset.filter(pet_size=pet_size)
            if pet_gender:
                queryset = queryset.filter(pet_gender=pet_gender)

        if not queryset.exists():
            print("No data Found")
            return render(request,"pets.html",{"message":"No Data Found"})

        return render(request,"pets.html",{"Pets":queryset})

    return render(request,"pets.html",{"Pets":queryset})

@login_required(login_url="/login")
def Pet_Meet(request):
    user = request.user
    if user.is_authenticated:
        subject = "Your Pet Adoption Meeting is Confirmed!"
        message = f"""
        Dear {user.username},
        We’re happy to let you know that your meeting for the pet adoption process has been successfully scheduled!
        This meeting will help us guide you through the final steps of the adoption, 
        share important information about your chosen pet, and answer any questions you might have.
        Thank you for taking a beautiful step toward giving a pet a loving forever home. 
        Our team will reach out to you soon with further updates.
        Warm regards,  
        The Pet Adoption Team
        """
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        messages.success(request, "Your pet adoption meeting has been scheduled successfully!")
    return redirect('/list')

@login_required(login_url="/login")
def Pet_Adopt(request):
    return redirect('/list')

def Pet_Adoption_Form(request):
    if request.method == "POST":
        pet_name = request.POST.get('pet_name')
        pet_type = request.POST.get('pet_type')
        pet_breed = request.POST.get('pet_breed')
        pet_age = request.POST.get('pet_age')
        pet_months = request.POST.get('pet_months')
        pet_age_type = request.POST.get('pet_age_type')
        pet_color = request.POST.get('pet_color')
        pet_background = request.POST.get('pet_background')
        pet_gender = request.POST.get('pet_gender')
        pet_size = request.POST.get('pet_size')
        pet_desc = request.POST.get('pet_desc')
        pet_photo = request.FILES.get('pet_photo')
        contact_name = request.POST.get('contact_name')
        contact_phoneno =  request.POST.get('contact_phoneno')
        contact_email =  request.POST.get('contact_email')
        contact_city =  request.POST.get('contact_city')

        print("Pet Data Received : ",pet_name,pet_type)
        if not pet_name or not pet_photo:
            return render(request, "pet-adoption-form.html", {"error": "Please fill all required fields."})

        queryset = Pet_Adoption.objects.create(
            pet_name = pet_name,
            pet_type = pet_type,
            pet_breed = pet_breed,
            pet_age = pet_age,
            pet_months = pet_months,
            pet_gender = pet_gender,
            pet_age_type = pet_age_type,
            pet_color = pet_color,
            pet_background = pet_background,
            pet_size = pet_size,
            pet_desc = pet_desc,
            pet_photo = pet_photo,
            contact_name = contact_name,
            contact_phoneno = contact_phoneno,
            contact_email = contact_email,
            contact_city = contact_city
        )

        queryset.save()
        queryset = Pet_Adoption.objects.all()
        
        return redirect("/list",{'alert' : "🐾 Woof! Your pet's profile is live and ready for adoption adventure! 🎉","Pets":queryset})
    return render(request,"pet-adoption-form.html")

def Pet_Contact(request):
    if request.method == "POST":
        contact_name = request.POST.get('contact_name')
        contact_email = request.POST.get('contact_email')
        contact_phoneno = request.POST.get('contact_phoneno')
        contact_subject = request.POST.get('contact_subject')
        contact_message = request.POST.get('contact_message')

        queryset = Contact_Form.objects.create (
            contact_name = contact_name,
            contact_email = contact_email,
            contact_phoneno = contact_phoneno,
            contact_subject = contact_subject,
            contact_message = contact_message
        )
        queryset.save()
        return render(request,"contact.html",{"alert":"Thanks for your Valueable Feedback"})
    
    return render(request,"contact.html")

def Add_Favourite(request,id):
    pet = get_object_or_404(Pet_Adoption, id=id)
    # Prevent duplicates
    Add_to_Favourites.objects.get_or_create(fav_user=request.user, fav_pet=pet)
    return redirect('/myfavs')

def My_Favourites(request):
    queryset = Add_to_Favourites.objects.filter(fav_user=request.user).select_related('fav_pet')
    if not queryset.exists():
        return render(request,"Favourites.html",{"message":"No Data Found"})
    
    return render(request,"Favourites.html",{"Favourites":queryset})

def Delete_Favourite(request, id):
    queryset = get_object_or_404(Add_to_Favourites, id=id)
    queryset.delete()
    return redirect('/myfavs')

def My_Notifications(request):
    if request.user.is_staff:
        queryset = Notifications.objects.all().order_by('-timestamp')
    if not queryset.exists():
        return render(request,"Notification.html",{"message":"No Data Found"})
    
    return render(request,"Notification.html",{"Notification":queryset})

@login_required(login_url="/login")
def Notification(request,id):
    pet = get_object_or_404(Pet_Adoption, id=id)
    # Prevent duplicates
    Notifications.objects.get_or_create(notify_user=request.user, notify_pet=pet)
    return redirect(request.META.get('HTTP_REFERER', '/detail'))

@login_required(login_url="/login")
def Accept_Notification(request,id):
    queryset = get_object_or_404(Pet_Adoption, id=id)
    pet = Notifications.objects.get(notify_pet_id = id)
    print(queryset)
    # Prevent duplicates
    user = request.user
    if user.is_authenticated:
        subject = "Pet Adoption Done Successfully"
        message = f"""
        Dear {pet.notify_user.username},
        Thank you for choosing to adopt through our Pet Adoption System!
        Your compassion and kindness are helping provide a loving home to an animal in need. 
        We are thrilled to have you as part of our mission to give every pet a second chance at happiness.
        Our team will contact you shortly with the next steps in the adoption process. 
        Meanwhile, feel free to explore more pets or learn about pet care tips on our platform.
        🐾 Thank you for making a difference!
        Warm regards,  
        The Pet Adoption Team
        """
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [pet.notify_user.email],
            fail_silently=False,
        )
        messages.success(request, "Pet Adoption Request Accepted")
        pet.delete()
    return redirect('/mynotifys')

def Delete_Notify(request,id):
    queryset = get_object_or_404(Notifications, id=id)
    print(queryset)
    # Prevent duplicates
    user = request.user
    if user.is_authenticated:
        subject = "Sorry Your Pet Adoption Request Rejected"
        message = f"""
        Dear {user.username},
        Your Request for {queryset.notify_pet.pet_name} has been Rejected
        """
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        messages.success(request, "Pet Adoption Request Rejected")
        queryset.delete()
    return redirect('/mynotifys')
