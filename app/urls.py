from django.urls import path
from . import views

# namespace for views
app_name = "app"

# (sub)urls of app
urlpatterns = [
    path("", views.index, name="index"),
    path("msg/<int:msgID>/", views.msg_detail_view, name="msg_detail"),
    path("new_msg/", views.new_message_view, name="new_msg"),
    path("msg/<int:msgID>/edit/", views.edit_message_view, name="edit_msg")
]
