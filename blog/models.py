from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User  # Importamos el modelo de usuario predeterminado
from django.db import models  # Importamos las herramientas para crear modelos

# Modelo para Categorías
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


# Modelo para Etiquetas
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# Modelo para Post (Entrada del Blog)
class TravelPost(models.Model):
    title = models.CharField(max_length=200, default='Título por defecto')
    content = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    destination = models.CharField(max_length=100, blank=True, null=True)  # Destino opcional
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)  # Para controlar si el post está publicado o no
    meta_title = models.CharField(max_length=60, blank=True, null=True)
    meta_description = models.CharField(max_length=160, blank=True, null=True)
    views = models.PositiveIntegerField(default=0)  # Para contar las vistas del post

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        # Automáticamente genera un slug si no se proporciona
        if not self.slug:
            self.slug = slugify(self.title)
            # Verificar que el slug sea único
            while TravelPost.objects.filter(slug=self.slug).exists():  # Verificar si el slug ya existe
                self.slug = f"{self.slug}-{self.id}"
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']


# Modelo para Comentarios
class Comment(models.Model):
    post = models.ForeignKey(TravelPost, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Relacionar con el usuario
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'



from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"
