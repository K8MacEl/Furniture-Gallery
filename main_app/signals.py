from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Cart

@receiver(user_logged_in)
def create_cart(sender, request, user, **kwargs):
    # Your logic here
    cart = Cart.objects.filter(user=user)
    if cart.exists():
        print(cart, 'users cart')
    else:

        Cart.objects.create(user=user, quantity=0)
        print("User logged in:", user.username)

user_logged_in.connect(create_cart, sender=get_user_model())