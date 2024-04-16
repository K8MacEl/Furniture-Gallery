import os
import django


# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'furniture_gallery.settings')

print(os.environ['DJANGO_SETTINGS_MODULE'])
django.setup()
from django.contrib.auth.models import User

import environ
environ.Env()
environ.Env.read_env()

username = os.environ['ADMIN_USERNAME']
email = os.environ['ADMIN_EMAIL']
pw = os.environ['ADMIN_PW']



def create_super_user():
    # Check if superuser already exists
    if not User.objects.filter(username=username).exists():
        # Create superuser
        User.objects.create_superuser(username, email, pw)
        print("Superuser created successfully.")
    else:
        print("Superuser already exists.")

if __name__ == "__main__":
    create_super_user()