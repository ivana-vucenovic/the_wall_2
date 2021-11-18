from django.urls import path
from .import views

urlpatterns = [
    path('', views.index),
    path('register', views.register_user),
    path('login', views.login_user),
    path('detales', views.detales),
    path('logout', views.logout),
    path('success', views.success),
    path('process_message', views.post_mess),
    path('add_comment/<int:id>', views.post_comment),
    path('user_profile/<int:id>', views.profile),
    path('like/<int:id>', views.add_like),
    path('delete/<int:id>', views.delete_comment),
    path('edit/<int:id>', views.edit)
]
