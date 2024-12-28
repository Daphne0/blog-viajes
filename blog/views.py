from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from .models import TravelPost, Category, Tag
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .forms import TravelPostForm  # El formulario que vamos a usar para crear y editar posts
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.utils.text import slugify
from .models import Profile
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm

# Vista basada en clase para la lista de publicaciones
class PostListView(ListView):
    model = TravelPost
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    queryset = TravelPost.objects.filter(published=True).order_by('-created_at')

    # Esto asegura que el contenido de los posts se recorte a una longitud de 200 caracteres
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for post in context['posts']:
            post.excerpt = post.content[:200]  # Recorta el contenido para mostrar un resumen
        return context

# Vista basada en clase para los detalles de un post
from django.views.generic import DetailView
from .models import TravelPost

class PostDetailView(DetailView):
    model = TravelPost
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug'

    # Sobrescribir el método de get_queryset para que solo se muestren los posts publicados
    def get_queryset(self):
        return TravelPost.objects.filter(published=True)

    # Incrementa las vistas cuando se carga la página del post
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views += 1
        obj.save()
        return obj

# Vista basada en clase para la lista de publicaciones por categoría
class PostByCategoryView(ListView):
    model = TravelPost
    template_name = 'blog/category_list.html'
    context_object_name = 'posts'

    # Método para obtener las publicaciones filtradas por categoría
    def get_queryset(self):
        category = get_object_or_404(Category, id=self.kwargs['category_id'])
        return TravelPost.objects.filter(category=category, published=True)

    # Agregar la categoría al contexto para poder mostrarla en la plantilla
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, id=self.kwargs['category_id'])
        context['category'] = category
        return context

# Vista basada en clase para la lista de publicaciones por etiqueta
class PostByTagView(ListView):
    model = TravelPost
    template_name = 'blog/tag_list.html'
    context_object_name = 'posts'

    # Método para obtener las publicaciones filtradas por etiqueta
    def get_queryset(self):
        tag = get_object_or_404(Tag, id=self.kwargs['tag_id'])
        return TravelPost.objects.filter(tags=tag, published=True)

    # Agregar la etiqueta al contexto para poder mostrarla en la plantilla
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = get_object_or_404(Tag, id=self.kwargs['tag_id'])
        context['tag'] = tag
        return context

# Vista para crear un nuevo viaje (Post)
from django.utils.text import slugify

@login_required
def create_post(request):
    if request.method == 'POST':
        form = TravelPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            base_slug = slugify(post.title)
            slug = base_slug
            counter = 1
            # Verifica si el slug ya existe y genera uno nuevo si es necesario
            while TravelPost.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            post.slug = slug
            post.save()
            return redirect('home')  # Redirige al listado de posts después de crear
    else:
        form = TravelPostForm()
    return render(request, 'blog/create_post.html', {'form': form})
# Vista para editar un viaje (Post)
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(TravelPost, id=post_id)
    if post.author != request.user:  # Verifica que el usuario sea el autor
        return redirect('home')

    if request.method == 'POST':
        form = TravelPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirige al listado de posts después de editar
    else:
        form = TravelPostForm(instance=post)  # Carga el post existente para editar
    return render(request, 'blog/edit_post.html', {'form': form})

# Vista para eliminar un viaje (Post)
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(TravelPost, id=post_id)
    if post.author != request.user:  # Verifica que el usuario sea el autor
        return redirect('home')

    post.delete()  # Elimina el post
    return redirect('home')  # Redirige al listado de posts después de eliminar


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige al login después de registrarse
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView

class PostUpdateView(UpdateView):
    model = TravelPost
    fields = ['title', 'content', 'image', 'category']  # Campos que pueden ser editados
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('home')  # Redirige al inicio después de editar

class PostDeleteView(DeleteView):
    model = TravelPost
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('home')  # Redirige al inicio después de eliminar



@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)  # Obtenemos el perfil del usuario actual
    return render(request, 'blog/profile.html', {'profile': profile})


@login_required
def profile_update_view(request):
    profile = request.user.profile  # Obtiene el perfil del usuario actual
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirige a la página de perfil
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'blog/profile_update.html', {'form': form})

# Vista para la página "Acerca de"
def about_view(request):
    return render(request, 'blog/about.html')

# Vista para la página "Contacto"
def contact_view(request):
    if request.method == 'POST':
        # Procesar el formulario de contacto
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Aquí puedes agregar lógica para enviar el mensaje por email
        # o almacenarlo en la base de datos.
        
        # Mensaje de confirmación
        return render(request, 'blog/contact.html', {'success': True})
    return render(request, 'blog/contact.html')
