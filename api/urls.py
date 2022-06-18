from django.urls import path
from . import views

# namespace for views
app_name = "api"

# (sub)urls of app
urlpatterns = [
    path("", views.index, name="index"),
    path("msg/<int:msgID>", views.get_message, name="get_msg"),
    path("msg/<int:msgID>/delete", views.delete_message, name="del_msg"),
    path("msg/<int:msgID>/edit", views.edit_message, name="edit_msg"),
    path("new_msg/", views.create_msg, name="new_msg")
]
