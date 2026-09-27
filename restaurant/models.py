from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User


# ============================================================
# CATEGORY
# ============================================================

class Category(models.Model):

    name = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True
    )

    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


# ============================================================
# MENU ITEM
# ============================================================

class MenuItem(models.Model):

    FOOD_TYPE_CHOICES = [
        ("veg", "Vegetarian"),
        ("non_veg", "Non-Vegetarian"),
    ]

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="menu_items"
    )

    name = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    food_type = models.CharField(
        max_length=20,
        choices=FOOD_TYPE_CHOICES,
        default="veg"
    )

    image = models.ImageField(
        upload_to="menu/",
        blank=True,
        null=True
    )

    is_available = models.BooleanField(
        default=True
    )

    is_featured = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


# ============================================================
# GALLERY IMAGE
# ============================================================

class GalleryImage(models.Model):

    title = models.CharField(
        max_length=150
    )

    image = models.ImageField(
        upload_to="gallery/"
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


# ============================================================
# RESTAURANT TABLE
# ============================================================

class RestaurantTable(models.Model):

    LOCATION_CHOICES = [
        ("indoor", "Indoor"),
        ("outdoor", "Outdoor"),
    ]

    table_number = models.PositiveIntegerField(
        unique=True
    )

    capacity = models.PositiveIntegerField(
        help_text="Maximum number of guests this table can accommodate."
    )

    location = models.CharField(
        max_length=20,
        choices=LOCATION_CHOICES,
        default="indoor"
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["table_number"]

    def __str__(self):
        return (
            f"Table {self.table_number} "
            f"({self.capacity} seats)"
        )


# ============================================================
# RESERVATION
# ============================================================

class Reservation(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    ]

    SEATING_PREFERENCE_CHOICES = [
        ("no_preference", "No Preference"),
        ("indoor", "Indoor"),
        ("outdoor", "Outdoor"),
    ]

    # Logged-in customer
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="restaurant_reservations",
        null=True,
        blank=True
    )

    name = models.CharField(
        max_length=150
    )

    phone = models.CharField(
        max_length=20
    )

    email = models.EmailField(
        blank=True
    )

    date = models.DateField()

    time = models.TimeField()

    guests = models.PositiveIntegerField()

    table = models.ForeignKey(
        RestaurantTable,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reservations"
    )

    seating_preference = models.CharField(
        max_length=20,
        choices=SEATING_PREFERENCE_CHOICES,
        default="no_preference"
    )

    message = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.name} - "
            f"{self.date} - "
            f"Table {self.table.table_number if self.table else 'N/A'}"
        )


# ============================================================
# CONTACT MESSAGE
# ============================================================

class ContactMessage(models.Model):

    name = models.CharField(
        max_length=150
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    subject = models.CharField(
        max_length=200,
        blank=True
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


# ============================================================
# OFFER
# ============================================================

class Offer(models.Model):

    title = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True
    )

    discount_percentage = models.PositiveIntegerField()

    image = models.ImageField(
        upload_to="offers/",
        blank=True,
        null=True
    )

    valid_until = models.DateField(
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


# ============================================================
# ORDER
# ============================================================

class Order(models.Model):

    ORDER_TYPE_CHOICES = [
        ("pickup", "Pickup"),
        ("delivery", "Delivery"),
    ]

    STATUS_CHOICES = [
        ("placed", "Placed"),
        ("confirmed", "Confirmed"),
        ("preparing", "Preparing"),
        ("ready", "Ready"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    PAYMENT_METHOD_CHOICES = [
        ("cod", "Cash on Delivery"),
        ("restaurant", "Pay at Restaurant"),
        ("online", "Online Payment"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="restaurant_orders"
    )

    customer_name = models.CharField(
        max_length=150
    )

    phone = models.CharField(
        max_length=20
    )

    address = models.TextField(
        blank=True
    )

    order_type = models.CharField(
        max_length=20,
        choices=ORDER_TYPE_CHOICES,
        default="pickup"
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="placed"
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default="cod"
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="pending"
    )

    payment_id = models.CharField(
        max_length=200,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"Order #{self.id} - "
            f"{self.customer_name}"
        )


# ============================================================
# ORDER ITEM
# ============================================================

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    item_name = models.CharField(
        max_length=150
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    def subtotal(self):

        price = self.price or Decimal("0.00")

        quantity = self.quantity or 0

        return price * quantity

    def __str__(self):
        return (
            f"{self.item_name} x "
            f"{self.quantity}"
        )


# ============================================================
# REVIEW
# ============================================================

class Review(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    rating = models.PositiveIntegerField(
        default=5
    )

    comment = models.TextField()

    is_approved = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.menu_item.name} - "
            f"{self.rating}"
        )