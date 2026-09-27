from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from .models import (
    Category,
    MenuItem,
    GalleryImage,
    RestaurantTable,
    Reservation,
    ContactMessage,
    Offer,
    Order,
    OrderItem,
    Review,
)


# ============================================================
# HOME
# ============================================================

def home(request):

    if request.method == "POST":

        form_type = request.POST.get("form_type")

        # ---------------- RESERVATION ----------------

        if form_type == "reservation":

            name = request.POST.get("name", "").strip()
            phone = request.POST.get("phone", "").strip()
            email = request.POST.get("email", "").strip()
            date = request.POST.get("date")
            time = request.POST.get("time")
            guests = request.POST.get("guests")
            message = request.POST.get("message", "").strip()

            if not name or not phone or not date or not time or not guests:

                messages.error(
                    request,
                    "Please fill all required reservation fields."
                )

            else:

                Reservation.objects.create(
                    name=name,
                    phone=phone,
                    email=email,
                    date=date,
                    time=time,
                    guests=guests,
                    message=message,
                )

                messages.success(
                    request,
                    "Your table reservation request has been submitted."
                )

                return redirect("home")

        # ---------------- CONTACT ----------------

        elif form_type == "contact":

            name = request.POST.get("name", "").strip()
            phone = request.POST.get("phone", "").strip()
            email = request.POST.get("email", "").strip()
            subject = request.POST.get("subject", "").strip()
            message = request.POST.get("message", "").strip()

            if not name or not message:

                messages.error(
                    request,
                    "Please enter your name and message."
                )

            else:

                ContactMessage.objects.create(
                    name=name,
                    phone=phone,
                    email=email,
                    subject=subject,
                    message=message,
                )

                messages.success(
                    request,
                    "Your message has been sent successfully."
                )

                return redirect("home")

    featured_items = MenuItem.objects.filter(
        is_available=True,
        is_featured=True
    ).select_related("category")

    if not featured_items.exists():

        featured_items = MenuItem.objects.filter(
            is_available=True
        ).select_related("category")[:6]

    gallery_images = GalleryImage.objects.filter(
        is_active=True
    )[:8]

    offers = Offer.objects.filter(
        is_active=True
    )[:4]

    reviews = Review.objects.filter(
        is_approved=True
    ).select_related(
        "user",
        "menu_item"
    )[:6]

    categories = Category.objects.filter(
        is_active=True
    )

    return render(
        request,
        "restaurant/home.html",
        {
            "featured_items": featured_items,
            "gallery_images": gallery_images,
            "offers": offers,
            "reviews": reviews,
            "categories": categories,
        }
    )


# ============================================================
# MENU
# ============================================================

def menu(request):

    items = MenuItem.objects.filter(
        is_available=True
    ).select_related("category")

    categories = Category.objects.filter(
        is_active=True
    )

    search = request.GET.get(
        "search",
        ""
    ).strip()

    category_id = request.GET.get(
        "category",
        ""
    )

    food_type = request.GET.get(
        "food_type",
        ""
    )

    sort = request.GET.get(
        "sort",
        ""
    )

    if search:

        items = items.filter(
            name__icontains=search
        )

    if category_id:

        items = items.filter(
            category_id=category_id
        )

    if food_type in [
        "veg",
        "non_veg"
    ]:

        items = items.filter(
            food_type=food_type
        )

    if sort == "price_low":

        items = items.order_by(
            "price"
        )

    elif sort == "price_high":

        items = items.order_by(
            "-price"
        )

    elif sort == "name":

        items = items.order_by(
            "name"
        )

    else:

        items = items.order_by(
            "-is_featured",
            "name"
        )

    return render(
        request,
        "restaurant/menu.html",
        {
            "items": items,
            "categories": categories,
            "selected_category": category_id,
            "selected_food_type": food_type,
            "selected_sort": sort,
            "search": search,
        }
    )


# ============================================================
# MENU DETAIL
# ============================================================

def menu_detail(request, item_id):

    item = get_object_or_404(
        MenuItem.objects.select_related("category"),
        id=item_id,
        is_available=True
    )

    reviews = Review.objects.filter(
        menu_item=item,
        is_approved=True
    ).select_related(
        "user"
    )

    if request.method == "POST":

        if not request.user.is_authenticated:

            messages.warning(
                request,
                "Please login to submit a review."
            )

            return redirect("login")

        rating = request.POST.get(
            "rating",
            "5"
        )

        comment = request.POST.get(
            "comment",
            ""
        ).strip()

        try:

            rating = int(rating)

        except ValueError:

            rating = 5

        if rating < 1:

            rating = 1

        if rating > 5:

            rating = 5

        if not comment:

            messages.error(
                request,
                "Please write a review."
            )

        else:

            Review.objects.create(
                user=request.user,
                menu_item=item,
                rating=rating,
                comment=comment,
            )

            messages.success(
                request,
                "Your review has been submitted."
            )

            return redirect(
                "menu_detail",
                item_id=item.id
            )

    return render(
        request,
        "restaurant/menu_detail.html",
        {
            "item": item,
            "reviews": reviews,
        }
    )


# ============================================================
# ABOUT
# ============================================================

def about(request):

    return render(
        request,
        "restaurant/about.html"
    )


# ============================================================
# CONTACT
# ============================================================

def contact(request):

    if request.method == "POST":

        name = request.POST.get(
            "name",
            ""
        ).strip()

        phone = request.POST.get(
            "phone",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        subject = request.POST.get(
            "subject",
            ""
        ).strip()

        message = request.POST.get(
            "message",
            ""
        ).strip()

        if not name or not message:

            messages.error(
                request,
                "Please enter your name and message."
            )

        else:

            ContactMessage.objects.create(
                name=name,
                phone=phone,
                email=email,
                subject=subject,
                message=message,
            )

            messages.success(
                request,
                "Your message has been sent successfully."
            )

            return redirect("contact")

    return render(
        request,
        "restaurant/contact.html"
    )


# ============================================================
# RESERVATION
# ============================================================

def reservation(request):

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        email = request.POST.get("email", "").strip()
        date = request.POST.get("date")
        time = request.POST.get("time")
        guests = request.POST.get("guests")
        table_id = request.POST.get("table")
        seating_preference = request.POST.get(
            "seating_preference",
            "no_preference"
        )
        message = request.POST.get("message", "").strip()

        # ----------------------------------------------------
        # BASIC VALIDATION
        # ----------------------------------------------------

        if not name or not phone or not date or not time or not guests:
            messages.error(
                request,
                "Please fill all required fields."
            )
            return redirect("reservation")

        # ----------------------------------------------------
        # GUEST VALIDATION
        # ----------------------------------------------------

        try:
            guests = int(guests)
        except (ValueError, TypeError):
            messages.error(
                request,
                "Please enter a valid number of guests."
            )
            return redirect("reservation")

        if guests < 1:
            messages.error(
                request,
                "Number of guests must be at least 1."
            )
            return redirect("reservation")

        # ----------------------------------------------------
        # TABLE VALIDATION
        # ----------------------------------------------------

        if not table_id:
            messages.error(
                request,
                "Please select a table."
            )
            return redirect("reservation")

        table = get_object_or_404(
            RestaurantTable,
            id=table_id,
            is_active=True
        )

        # ----------------------------------------------------
        # TABLE CAPACITY CHECK
        # ----------------------------------------------------

        if table.capacity < guests:
            messages.error(
                request,
                f"Table {table.table_number} can accommodate "
                f"only {table.capacity} guests."
            )
            return redirect("reservation")

        # ----------------------------------------------------
        # SEATING PREFERENCE VALIDATION
        # ----------------------------------------------------

        if seating_preference not in [
            "no_preference",
            "indoor",
            "outdoor"
        ]:
            seating_preference = "no_preference"

        # ----------------------------------------------------
        # CHECK TABLE AVAILABILITY
        # ----------------------------------------------------

        existing_reservation = Reservation.objects.filter(
            table=table,
            date=date,
            time=time,
            status__in=[
                "pending",
                "confirmed"
            ]
        ).exists()

        if existing_reservation:
            messages.error(
                request,
                f"Table {table.table_number} is already booked "
                f"for the selected date and time."
            )
            return redirect("reservation")

        # ----------------------------------------------------
        # CREATE RESERVATION
        # ----------------------------------------------------

        Reservation.objects.create(
            user=request.user if request.user.is_authenticated else None,
            name=name,
            phone=phone,
            email=email,
            date=date,
            time=time,
            guests=guests,
            table=table,
            seating_preference=seating_preference,
            message=message,
            status="pending"
        )

        messages.success(
            request,
            f"Your reservation request has been submitted. "
            f"Table {table.table_number} is requested for your booking."
        )

        return redirect("reservation")

    # ========================================================
    # GET REQUEST
    # ========================================================

    tables = RestaurantTable.objects.filter(
        is_active=True
    ).order_by(
        "table_number"
    )

    return render(
        request,
        "restaurant/reservation.html",
        {
            "tables": tables,
        }
    )


# ============================================================
# REGISTER
# ============================================================

def register_view(request):

    if request.user.is_authenticated:

        return redirect("home")

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        first_name = request.POST.get(
            "first_name",
            ""
        ).strip()

        last_name = request.POST.get(
            "last_name",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        confirm_password = request.POST.get(
            "confirm_password",
            ""
        )

        if not username or not password:

            messages.error(
                request,
                "Username and password are required."
            )

            return redirect("register")

        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

            return redirect("register")

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                "Username already exists."
            )

            return redirect("register")

        if email and User.objects.filter(
            email=email
        ).exists():

            messages.error(
                request,
                "Email is already registered."
            )

            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        login(
            request,
            user
        )

        messages.success(
            request,
            "Account created successfully."
        )

        return redirect("home")

    return render(
        request,
        "restaurant/register.html"
    )


# ============================================================
# LOGIN
# ============================================================

def login_view(request):

    if request.user.is_authenticated:

        return redirect("home")

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(
                request,
                user
            )

            messages.success(
                request,
                "Welcome back!"
            )

            return redirect("home")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "restaurant/login.html"
    )


# ============================================================
# LOGOUT
# ============================================================

@login_required
def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out."
    )

    return redirect("home")


# ============================================================
# CART
# ============================================================

def add_to_cart(request, item_id):

    item = get_object_or_404(
        MenuItem,
        id=item_id,
        is_available=True
    )

    cart = request.session.get(
        "cart",
        {}
    )

    item_id = str(item_id)

    if item_id in cart:

        cart[item_id]["quantity"] += 1

    else:

        cart[item_id] = {
            "quantity": 1
        }

    request.session["cart"] = cart

    request.session.modified = True

    messages.success(
        request,
        f"{item.name} added to cart."
    )

    return redirect("cart")


# ============================================================
# CART VIEW
# ============================================================

def cart_view(request):

    cart = request.session.get(
        "cart",
        {}
    )

    cart_items = []

    total = Decimal("0.00")

    for item_id, data in cart.items():

        try:

            item = MenuItem.objects.get(
                id=item_id,
                is_available=True
            )

        except MenuItem.DoesNotExist:

            continue

        quantity = int(
            data.get(
                "quantity",
                1
            )
        )

        subtotal = item.price * quantity

        total += subtotal

        cart_items.append(
            {
                "item": item,
                "quantity": quantity,
                "subtotal": subtotal,
            }
        )

    return render(
        request,
        "restaurant/cart.html",
        {
            "cart_items": cart_items,
            "total": total,
        }
    )


# ============================================================
# UPDATE CART
# ============================================================

def update_cart(request, item_id):

    cart = request.session.get(
        "cart",
        {}
    )

    item_id = str(item_id)

    if item_id not in cart:

        return redirect("cart")

    if request.method == "POST":

        quantity = request.POST.get(
            "quantity",
            "1"
        )

        try:

            quantity = int(quantity)

        except ValueError:

            quantity = 1

        if quantity <= 0:

            del cart[item_id]

        else:

            cart[item_id]["quantity"] = quantity

    request.session["cart"] = cart

    request.session.modified = True

    messages.success(
        request,
        "Cart updated."
    )

    return redirect("cart")


# ============================================================
# REMOVE FROM CART
# ============================================================

def remove_from_cart(request, item_id):

    cart = request.session.get(
        "cart",
        {}
    )

    item_id = str(item_id)

    if item_id in cart:

        del cart[item_id]

    request.session["cart"] = cart

    request.session.modified = True

    messages.success(
        request,
        "Item removed from cart."
    )

    return redirect("cart")


# ============================================================
# CHECKOUT
# ============================================================

@login_required
def checkout(request):

    cart_data = request.session.get(
        "cart",
        {}
    )

    if not cart_data:

        messages.warning(
            request,
            "Your cart is empty."
        )

        return redirect("menu")

    cart_items = []

    total = Decimal("0.00")

    for item_id, data in cart_data.items():

        try:

            menu_item = MenuItem.objects.get(
                id=item_id,
                is_available=True
            )

        except MenuItem.DoesNotExist:

            continue

        quantity = int(
            data.get(
                "quantity",
                1
            )
        )

        subtotal = menu_item.price * quantity

        total += subtotal

        cart_items.append(
            {
                "item": menu_item,
                "quantity": quantity,
                "subtotal": subtotal,
            }
        )

    if not cart_items:

        messages.warning(
            request,
            "Your cart is empty."
        )

        return redirect("menu")

    if request.method == "POST":

        customer_name = request.POST.get(
            "customer_name",
            ""
        ).strip()

        phone = request.POST.get(
            "phone",
            ""
        ).strip()

        address = request.POST.get(
            "address",
            ""
        ).strip()

        order_type = request.POST.get(
            "order_type",
            "pickup"
        )

        payment_method = request.POST.get(
            "payment_method",
            "cod"
        )

        # ----------------------------------------------------
        # VALIDATE ORDER TYPE
        # ----------------------------------------------------

        if order_type not in [
            "pickup",
            "delivery"
        ]:

            order_type = "pickup"

        # ----------------------------------------------------
        # VALIDATE PAYMENT METHOD
        # ----------------------------------------------------

        if payment_method not in [
            "cod",
            "restaurant",
            "online"
        ]:

            payment_method = "cod"

        # ----------------------------------------------------
        # BASIC VALIDATION
        # ----------------------------------------------------

        if not customer_name:

            messages.error(
                request,
                "Please enter your name."
            )

            return redirect("checkout")

        if not phone:

            messages.error(
                request,
                "Please enter your phone number."
            )

            return redirect("checkout")

        if order_type == "delivery" and not address:

            messages.error(
                request,
                "Please enter your delivery address."
            )

            return redirect("checkout")

        # ----------------------------------------------------
        # PAYMENT STATUS
        # ----------------------------------------------------

        payment_status = "pending"

        # ----------------------------------------------------
        # CREATE ORDER
        # ----------------------------------------------------

        order = Order.objects.create(

            user=request.user,

            customer_name=customer_name,

            phone=phone,

            address=address,

            order_type=order_type,

            total_amount=total,

            status="placed",

            payment_method=payment_method,

            payment_status=payment_status,
        )

        # ----------------------------------------------------
        # CREATE ORDER ITEMS
        # ----------------------------------------------------

        for cart_item in cart_items:

            menu_item = cart_item["item"]

            OrderItem.objects.create(

                order=order,

                menu_item=menu_item,

                item_name=menu_item.name,

                price=menu_item.price,

                quantity=cart_item["quantity"],
            )

        # ----------------------------------------------------
        # CLEAR CART
        # ----------------------------------------------------

        request.session["cart"] = {}

        request.session.modified = True

        messages.success(
            request,
            f"Order #{order.id} placed successfully."
        )

        return redirect(
            "order_detail",
            order_id=order.id
        )

    return render(
        request,
        "restaurant/checkout.html",
        {
            "cart_items": cart_items,
            "total": total,
        }
    )


# ============================================================
# ORDERS
# ============================================================

@login_required
def orders(request):

    user_orders = Order.objects.filter(
        user=request.user
    ).prefetch_related(
        "items"
    )

    return render(
        request,
        "restaurant/orders.html",
        {
            "orders": user_orders,
        }
    )


# ============================================================
# ORDER DETAIL
# ============================================================

@login_required
def order_detail(request, order_id):

    order = get_object_or_404(
        Order.objects.prefetch_related(
            "items"
        ),
        id=order_id,
        user=request.user
    )

    return render(
        request,
        "restaurant/order_detail.html",
        {
            "order": order,
        }
    )


# ============================================================
# PROFILE
# ============================================================

@login_required
def profile(request):

    user = request.user

    if request.method == "POST":

        first_name = request.POST.get(
            "first_name",
            ""
        ).strip()

        last_name = request.POST.get(
            "last_name",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        user.first_name = first_name

        user.last_name = last_name

        user.email = email

        user.save()

        messages.success(
            request,
            "Profile updated successfully."
        )

        return redirect("profile")

    user_orders = Order.objects.filter(
        user=user
    ).order_by(
        "-created_at"
    )[:5]

    reservations = Reservation.objects.filter(
        user=user
    ).select_related(
        "table"
    ).order_by(
        "-created_at"
    )[:5]

    return render(
        request,
        "restaurant/profile.html",
        {
            "user_orders": user_orders,
            "reservations": reservations,
        }
    )


# ============================================================
# GALLERY
# ============================================================

def gallery(request):

    gallery_images = GalleryImage.objects.filter(
        is_active=True
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "restaurant/gallery.html",
        {
            "gallery_images": gallery_images,
        }
    )


# ============================================================
# OFFERS
# ============================================================

def offers(request):

    active_offers = Offer.objects.filter(
        is_active=True
    )

    return render(
        request,
        "restaurant/offers.html",
        {
            "offers": active_offers,
        }
    )