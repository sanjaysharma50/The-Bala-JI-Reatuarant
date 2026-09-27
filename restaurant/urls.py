from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "menu/",
        views.menu,
        name="menu"
    ),

    path(
        "menu/<int:item_id>/",
        views.menu_detail,
        name="menu_detail"
    ),

    path(
        "about/",
        views.about,
        name="about"
    ),

    path(
        "contact/",
        views.contact,
        name="contact"
    ),

    path(
        "reservation/",
        views.reservation,
        name="reservation"
    ),

    path(
        "register/",
        views.register_view,
        name="register"
    ),

    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    path(
        "cart/",
        views.cart_view,
        name="cart"
    ),

    path(
        "cart/add/<int:item_id>/",
        views.add_to_cart,
        name="add_to_cart"
    ),

    path(
        "cart/update/<int:item_id>/",
        views.update_cart,
        name="update_cart"
    ),

    path(
        "cart/remove/<int:item_id>/",
        views.remove_from_cart,
        name="remove_from_cart"
    ),

    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),

    path(
        "orders/",
        views.orders,
        name="orders"
    ),

    path(
        "orders/<int:order_id>/",
        views.order_detail,
        name="order_detail"
    ),

    path(
        "profile/",
        views.profile,
        name="profile"
    ),

    path(
        "gallery/",
        views.gallery,
        name="gallery"
    ),

    path(
        "offers/",
        views.offers,
        name="offers"
    ),
]