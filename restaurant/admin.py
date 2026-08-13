from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category,
    MenuItem,
    GalleryImage,
    Reservation,
    ContactMessage,
)


# =========================================================
# CATEGORY
# =========================================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
    )


# =========================================================
# MENU ITEM
# =========================================================

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "category",
        "price",
        "food_type",
        "is_available",
        "is_featured",
        "created_at",
    )

    list_filter = (
        "category",
        "food_type",
        "is_available",
        "is_featured",
    )

    search_fields = (
        "name",
        "description",
    )


# =========================================================
# GALLERY
# =========================================================

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):

    list_display = (
        "image_preview",
        "title",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "title",
    )

    readonly_fields = (
        "image_preview",
    )

    def image_preview(self, obj):

        if obj.image:

            return format_html(
                '<img src="{}" width="120" height="80" '
                'style="object-fit:cover; border-radius:6px;" />',
                obj.image.url
            )

        return "No Image"

    image_preview.short_description = "Preview"


# =========================================================
# RESERVATION
# =========================================================

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "phone",
        "date",
        "time",
        "guests",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "date",
    )

    search_fields = (
        "name",
        "phone",
        "email",
    )


# =========================================================
# CONTACT MESSAGE
# =========================================================

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "phone",
        "email",
        "subject",
        "created_at",
    )

    search_fields = (
        "name",
        "phone",
        "email",
        "subject",
        "message",
    )