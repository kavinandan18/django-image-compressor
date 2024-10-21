from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ImageUploadForm, FileUploadForm
from PIL import Image
import os
import zipfile

def custom_404(request, exception):
    return render(request, 'compressor/404.html', status=404)


class HomeView(View):
    def get(self, request):
        return render(request, 'compressor/home.html')

class LoginView(View):
    def get(self, request):
        form = CustomAuthenticationForm()
        return render(request, 'compressor/login.html', {'form': form})

    def post(self, request):
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        messages.error(request, 'Invalid username or password.')
        return render(request, 'compressor/login.html', {'form': form})

class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'compressor/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
        return render(request, 'compressor/register.html', {'form': form})

class LogoutView(View):
    def get(self, request):
        auth_logout(request)
        messages.success(request, 'You have been logged out.')
        return redirect('login')

def compress_image(image_path, size_kb, quality):
    try:
        with default_storage.open(image_path, 'rb') as img_file:
            img = Image.open(img_file)
            img_format = img.format
            output_path = os.path.splitext(image_path)[0] + '_compressed.' + img_format.lower()

            with default_storage.open(output_path, 'wb') as output_file:
                img.save(output_file, format=img_format, quality=quality, optimize=True)

            while os.path.getsize(default_storage.path(output_path)) > size_kb * 1024 and quality > 5:
                quality -= 5
                with default_storage.open(output_path, 'wb') as output_file:
                    img.save(output_file, format=img_format, quality=quality, optimize=True)

            if os.path.getsize(default_storage.path(output_path)) > size_kb * 1024:
                raise Exception("Unable to compress image to the desired size.")

            return output_path
    except Exception as e:
        raise e

def compress_file(file_path, size_kb):
    try:
        zip_path = os.path.splitext(file_path)[0] + '_compressed.zip'
        with zipfile.ZipFile(default_storage.path(zip_path), 'w') as zipf:
            zipf.write(default_storage.path(file_path), os.path.basename(file_path))
        
        while os.path.getsize(default_storage.path(zip_path)) > size_kb * 1024:
            raise Exception("Unable to compress file to the desired size.")

        return zip_path
    except Exception as e:
        raise e

class ImageUploadView(LoginRequiredMixin, View):
    form_class = ImageUploadForm
    template_name = 'compressor/upload_image.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            size_kb = form.cleaned_data['size_kb']
            quality = form.cleaned_data['quality']
            
            try:
                image_path = default_storage.save(image.name, ContentFile(image.read()))
                compressed_image_path = compress_image(image_path, size_kb, quality)
                compressed_image_url = default_storage.url(compressed_image_path)
                print(compressed_image_url)

                messages.success(request, 'Image compressed successfully!')
                return render(request, self.template_name, {
                    'form': form,
                    'compressed_image_url': compressed_image_url,
                })
            except Exception as e:
                messages.error(request, f"Error: {e}")
                return render(request, self.template_name, {'form': form})
        else:
            return render(request, self.template_name, {'form': form})

class FileUploadView(LoginRequiredMixin, View):
    form_class = FileUploadForm
    template_name = 'compressor/upload_file.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            size_kb = form.cleaned_data['size_kb']

            try:
                file_path = default_storage.save(file.name, ContentFile(file.read()))
                compressed_file_path = compress_file(file_path, size_kb)
                compressed_file_url = default_storage.url(compressed_file_path)
                
                messages.success(request, 'File compressed successfully!')
                return render(request, self.template_name, {
                    'form': form,
                    'compressed_file_url': compressed_file_url,
                })
            except Exception as e:
                messages.error(request, f"Error: {e}")
                return render(request, self.template_name, {'form': form})
        else:
            return render(request, self.template_name, {'form': form})
