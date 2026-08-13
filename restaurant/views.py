from django.shortcuts import render, redirect
from django.contrib import messages

from .models import (
    MenuItem,
    GalleryImage,
    Reservation,
    ContactMessage,
)


def home(request):

    # =========================
    # POST REQUESTS
    # =========================

    if request.method == "POST":

        form_type = request.POST.get("form_type")

        # =========================
        # RESERVATION
        # =========================

        if form_type == "reservation":

            name = request.POST.get("name")
            phone = request.POST.get("phone")
            email = request.POST.get("email")
            date = request.POST.get("date")
            time = request.POST.get("time")
            guests = request.POST.get("guests")
            message = request.POST.get("message")

            if name and phone and date and time and guests:

                Reservation.objects.create(
                    name=name,
                    phone=phone,
                    email=email,
                    date=date,
                    time=time,
                    guests=guests,
                    message=message,
                    status="pending",
                )

                messages.success(
                    request,
                    "Your table reservation has been submitted successfully!"
                )

            else:

                messages.error(
                    request,
                    "Please fill all required reservation fields."
                )

            return redirect("home")


        # =========================
        # CONTACT MESSAGE
        # =========================

        elif form_type == "contact":

            name = request.POST.get("contact_name")
            phone = request.POST.get("contact_phone")
            email = request.POST.get("contact_email")
            subject = request.POST.get("contact_subject")
            message_text = request.POST.get("contact_message")

            if name and message_text:

                ContactMessage.objects.create(
                    name=name,
                    phone=phone,
                    email=email,
                    subject=subject,
                    message=message_text,
                )

                messages.success(
                    request,
                    "Thank you! Your message has been sent successfully."
                )

            else:

                messages.error(
                    request,
                    "Please enter your name and message."
                )

            return redirect("home")


    # =========================
    # MENU
    # =========================

    menu_items = (
        MenuItem.objects
        .filter(
            category__is_active=True,
            is_available=True
        )
        .select_related("category")
        .order_by(
            "category__created_at",
            "name"
        )
    )


    # =========================
    # GALLERY
    # =========================

    gallery_images = (
        GalleryImage.objects
        .filter(is_active=True)
        .order_by("-created_at")
    )


    context = {
        "menu_items": menu_items,
        "gallery_images": gallery_images,
    }


    return render(
        request,
        "restaurant/home.html",
        context
    )