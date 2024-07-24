# Django Image & File  Compressor

Django Image & File Compressor is a web application that allows users to upload and compress images and files to their desired size and quality. The application provides a user-friendly interface to manage image and file compression needs effectively.

## Features

- **Image Compression**: Upload images, set desired size, and adjust quality.
- **File Compression**: Upload any file and set the desired size.
- **User Authentication**: Secure login and registration for users.
- **Custom 404 Page**: A well-designed custom 404 error page.

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/kavinandan18/django-image-compressor.git
    cd django-image-compressor
    ```

2. **Create and activate a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Apply migrations:**
    ```sh
    python manage.py migrate
    ```

5. **Create a superuser:**
    ```sh
    python manage.py createsuperuser
    ```

6. **Run the development server:**
    ```sh
    python manage.py runserver
    ```

7. **Visit the application:**
    Open your web browser and navigate to `http://127.0.0.1:8000`.

## Configuration

### Allowed Hosts

Ensure that `ALLOWED_HOSTS` is set in your `settings.py` file:

```python
# settings.py

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'yourdomain.com']


