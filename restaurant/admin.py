from django.contrib import admin
from django.utils.html import format_html

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


# =========================================================
# CATEGORY ADMIN
# =========================================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
    )

    list_editable = (
        "is_active",
    )

    ordering = (
        "name",
    )


# =========================================================
# MENU ITEM ADMIN
# =========================================================

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "image_preview",
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
        "created_at",
    )

    search_fields = (
        "name",
        "description",
        "category__name",
    )

    list_editable = (
        "price",
        "is_available",
        "is_featured",
    )

    list_per_page = 20

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "image_preview",
        "created_at",
    )

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "category",
                    "name",
                    "description",
                    "price",
                    "food_type",
                )
            },
        ),
        (
            "Product Image",
            {
                "fields": (
                    "image",
                    "image_preview",
                )
            },
        ),
        (
            "Availability",
            {
                "fields": (
                    "is_available",
                    "is_featured",
                )
            },
        ),
        (
            "Information",
            {
                "fields": (
                    "created_at",
                )
            },
        ),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="70" height="70" '
                'style="object-fit:cover;border-radius:8px;" />',
                obj.image.url
            )

        return "No Image"

    image_preview.short_description = "Image"


# =========================================================
# GALLERY ADMIN
# =========================================================

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "image_preview",
        "title",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    search_fields = (
        "title",
    )

    list_editable = (
        "is_active",
    )

    readonly_fields = (
        "image_preview",
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    fieldsets = (
        (
            "Gallery Information",
            {
                "fields": (
                    "title",
                    "image",
                    "image_preview",
                    "is_active",
                )
            },
        ),
        (
            "Information",
            {
                "fields": (
                    "created_at",
                )
            },
        ),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="70" '
                'style="object-fit:cover;border-radius:8px;" />',
                obj.image.url
            )

        return "No Image"

    image_preview.short_description = "Preview"


# =========================================================
# RESERVATION ADMIN
# =========================================================

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "phone",
        "email",
        "date",
        "time",
        "guests",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "date",
        "created_at",
    )

    search_fields = (
        "name",
        "phone",
        "email",
    )

    list_editable = (
        "status",
    )

    date_hierarchy = "date"

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
    )

    fieldsets = (
        (
            "Customer Information",
            {
                "fields": (
                    "name",
                    "phone",
                    "email",
                )
            },
        ),
        (
            "Reservation Details",
            {
                "fields": (
                    "date",
                    "time",
                    "guests",
                    "message",
                    "status",
                )
            },
        ),
        (
            "Information",
            {
                "fields": (
                    "created_at",
                )
            },
        ),
    )


# =========================================================
# CONTACT MESSAGE ADMIN
# =========================================================

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "phone",
        "email",
        "subject",
        "created_at",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "name",
        "phone",
        "email",
        "subject",
        "message",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    fieldsets = (
        (
            "Customer Information",
            {
                "fields": (
                    "name",
                    "phone",
                    "email",
                )
            },
        ),
        (
            "Message",
            {
                "fields": (
                    "subject",
                    "message",
                )
            },
        ),
        (
            "Information",
            {
                "fields": (
                    "created_at",
                )
            },
        ),
    )


# =========================================================
# OFFER ADMIN
# =========================================================

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "image_preview",
        "title",
        "discount_percentage",
        "valid_until",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
        "valid_until",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
    )

    list_editable = (
        "discount_percentage",
        "is_active",
    )

    readonly_fields = (
        "image_preview",
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    fieldsets = (
        (
            "Offer Information",
            {
                "fields": (
                    "title",
                    "description",
                    "discount_percentage",
                )
            },
        ),
        (
            "Offer Image",
            {
                "fields": (
                    "image",
                    "image_preview",
                )
            },
        ),
        (
            "Validity",
            {
                "fields": (
                    "valid_until",
                    "is_active",
                )
            },
        ),
        (
            "Information",
            {
                "fields": (
                    "created_at",
                )
            },
        ),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="70" '
                'style="object-fit:cover;border-radius:8px;" />',
                obj.image.url
            )

        return "No Image"

    image_preview.short_description = "Preview"


# =========================================================
# ORDER ITEM INLINE
# =========================================================

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

    readonly_fields = (
        "item_name",
        "price",
        "subtotal_display",
    )

    fields = (
        "menu_item",
        "item_name",
        "price",
        "quantity",
        "subtotal_display",
    )

    def subtotal_display(self, obj):
        return f"₹{obj.subtotal():.2f}"

    subtotal_display.short_description = "Subtotal"


# =========================================================
# ORDER ADMIN
# =========================================================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer_name",
        "phone",
        "order_type",
        "total_amount",
        "status",
        "payment_method",
        "payment_status",
        "created_at",
    )

    list_filter = (
        "status",
        "order_type",
        "payment_method",
        "payment_status",
        "created_at",
    )

    search_fields = (
        "customer_name",
        "phone",
        "address",
        "user__username",
        "user__email",
        "payment_id",
    )

    list_editable = (
        "status",
        "payment_status",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 20

    inlines = (
        OrderItemInline,
    )

    fieldsets = (
        (
            "Customer Information",
            {
                "fields": (
                    "user",
                    "customer_name",
                    "phone",
                    "address",
                )
            },
        ),
        (
            "Order Information",
            {
                "fields": (
                    "order_type",
                    "total_amount",
                    "status",
                )
            },
        ),
        (
            "Payment Information",
            {
                "fields": (
                    "payment_method",
                    "payment_status",
                    "payment_id",
                )
            },
        ),
        (
            "Information",
            {
                "fields": (
                    "created_at",
                )
            },
        ),
    )


# =========================================================
# REVIEW ADMIN
# =========================================================

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "menu_item",
        "rating",
        "is_approved",
        "created_at",
    )

    list_filter = (
        "rating",
        "is_approved",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "menu_item__name",
        "comment",
    )

    list_editable = (
        "is_approved",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    fieldsets = (
        (
            "Review Information",
            {
                "fields": (
                    "user",
                    "menu_item",
                    "rating",
                    "comment",
                    "is_approved",
                )
            },
        ),
        (
            "Information",
            {
                "fields": (
                    "created_at",
                )
            },
        ),
    )


# =========================================================
# ADMIN SITE SETTINGS
# =========================================================

admin.site.site_header = "The-Bala-JI Restaurant Administration"
admin.site.site_title = "The-Bala-JI Restaurant Admin"
admin.site.index_title = "Restaurant Management Dashboard"


@admin.register(RestaurantTable)
class RestaurantTableAdmin(admin.ModelAdmin):

    list_display = (
        "table_number",
        "capacity",
        "location",
        "is_active",
        "created_at",
    )

    list_filter = (
        "location",
        "is_active",
    )

    search_fields = (
        "table_number",
    )

    list_editable = (
        "capacity",
        "location",
        "is_active",
    )

    ordering = (
        "table_number",
    )