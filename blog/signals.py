from django.db.models.signals import post_save  # Señal que se dispara después de guardar un modelo
from django.dispatch import receiver  # Decorador para conectar la señal
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)  # Esta señal se ejecuta después de guardar un usuario
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Si el usuario se acaba de crear, creamos un perfil vinculado
        Profile.objects.create(user=instance)
    else:
        # Si el usuario ya existe, actualizamos el perfil
        instance.profile.save()
