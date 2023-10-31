from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Q
from .forms import DoctorUpdateForm
from django.contrib import messages
from .models import User, Doctor


def index(request):
    return render(request, "network/index.html")

def doctor_search(request):
    search_query = request.GET.get('search_query', '')

    doctors = Doctor.objects.filter(
        Q(name__icontains=search_query) |
        Q(email__icontains=search_query) |
        Q(phone_number__icontains=search_query) |
        Q(country__icontains=search_query) |
        Q(profession__icontains=search_query)
    )

    return render(request, 'network/search_results.html', {'doctors': doctors, 'search_query': search_query})

def add_doctor(request):
    if request.method == 'POST':
        name = request.POST["name"]
        age = request.POST["age"]
        email = request.POST["email"]
        phone_number = request.POST["phone_number"]
        working_status = request.POST["working_status"]
        profession = request.POST["profession"]
        country = request.POST["country"]

        doctor = Doctor(name=name, age=age, email=email, phone_number=phone_number, working_status=working_status, profession=profession, country=country)
        doctor.save()
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, 'network/add_doctor.html')

def update_doctor(request, doctor_id):
    doctor = Doctor.objects.get(pk=doctor_id)
    if request.method == 'POST':
        # Get the selected category and new value from the form
        update_category = request.POST.get('update_category')
        new_value = request.POST.get('new_value')

        # Update the doctor's category based on the selected category
        if update_category == 'name':
            doctor.name = new_value
        elif update_category == 'age':
            doctor.age = new_value
        elif update_category == 'email':
            doctor.email = new_value
        elif update_category == 'phone_number':
            doctor.phone_number = new_value
        elif update_category == 'working_status':
            doctor.working_status = new_value
        elif update_category == 'profession':
            doctor.profession = new_value
        elif update_category == 'country':
            doctor.country = new_value

        # Save the updated doctor instance
        doctor.save()

        return render(request, 'network/update_doctor.html', {'doctor': doctor})

    return render(request, 'network/update_doctor.html', {'doctor': doctor})

def delete_doctor(request, doctor_id):
    doctor = Doctor.objects.get(pk=doctor_id)
    if request.method == 'POST':
        # Get the doctor instance based on the doctor_id
        try:
            doctor = Doctor.objects.get(pk=doctor_id)
        except Doctor.DoesNotExist:
            messages.error(request, f"Doctor with ID {doctor_id} does not exist.")
            return HttpResponseRedirect(reverse("index")) # Redirect to a doctor list page

        # Check if the user entered "DELETE" to confirm the deletion
        confirmation = request.POST.get('confirmation')
        if confirmation == 'DELETE':
            # Perform the doctor deletion
            doctor.delete()
            messages.success(request, f"{doctor.name} has been successfully deleted.")
            return HttpResponseRedirect(reverse("index"))  # Redirect to a doctor list page
        else:
            messages.error(request, "Deletion not confirmed. The doctor has not been deleted.")
            return redirect(reverse('delete_doctor', args=[doctor_id]))  # Redirect back to the delete confirmation page

    return render(request, 'network/delete_doctor.html', {'doctor': doctor})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
