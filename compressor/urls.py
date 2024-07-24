from django.urls import path
from .views import HomeView, ImageUploadView, FileUploadView, LoginView, RegisterView, LogoutView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('compress-image/', ImageUploadView.as_view(), name='compress_image'),
    path('compress-file/', FileUploadView.as_view(), name='compress_file'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
