from django.db import models


# =========================================================
# MENU CATEGORY
# =========================================================

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

    def __str__(self):
        return self.name


# =========================================================
# MENU ITEM
# =========================================================

class MenuItem(models.Model):

    VEG_CHOICES = [
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
        choices=VEG_CHOICES,
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


# =========================================================
# RESTAURANT GALLERY
# =========================================================

class GalleryImage(models.Model):

    title = models.CharField(
        max_length=150,
        blank=True
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

    def __str__(self):
        return self.title or "Restaurant Image"


# =========================================================
# TABLE RESERVATION
# =========================================================

class Reservation(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    ]

    name = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=20
    )

    email = models.EmailField(
        blank=True
    )

    date = models.DateField()

    time = models.TimeField()

    guests = models.PositiveIntegerField(
        default=1
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

    def __str__(self):
        return f"{self.name} - {self.date} - {self.time}"


# =========================================================
# CONTACT MESSAGE
# =========================================================

class ContactMessage(models.Model):

    name = models.CharField(
        max_length=100
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
        return f"{self.name} - {self.subject}"