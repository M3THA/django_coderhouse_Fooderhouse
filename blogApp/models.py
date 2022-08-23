from django.db import models
from django.contrib.auth.models import User

#ckeditor para poder editar post
from ckeditor.fields import RichTextField

#slug para agregar un id rápido para los posts
from autoslug import AutoSlugField

#para asignar al usuario como autor del post
from django.contrib.auth import get_user_model

#para asignar el slug al post en pages
from django.urls import reverse

User= get_user_model()

class Autor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    imagen_perfil= models.ImageField(upload_to="media")
    def __str__(self):
        return f"Usuario: {self.user}" 
    

class Blog_post(models.Model):
    titulo= models.CharField(max_length=50, blank=True, null=True)
    slug= AutoSlugField(populate_from= 'titulo')
    subtitulo= models.TextField(max_length=50, blank=True, null=True)
    cuerpo= RichTextField(blank=True, null=True)
    autor= models.ForeignKey(User, null=True, default=None, on_delete=models.CASCADE)
    fecha= models.DateField(auto_now_add= True)
    imagen= models.ImageField(verbose_name='imagen', upload_to='media', null=True, blank=True)
    likes= models.ManyToManyField(User, related_name="post_like")

    def __str__(self):
        return f"Título: {self.titulo}  - Autor {self.autor} - Fecha {self.fecha}"
    
    def get_absolute_url(self):
        return reverse("post", kwargs={
            'slug': self.slug
        })

    @property
    def blog_post_link(self):
        return reverse("post", kwargs={
            'slug': self.slug
        })

    def total_likes(self):
        return self.likes.count()


class Avatar(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    imagen= models.ImageField(upload_to='avatares', null=True, blank= True)

    def __str__(self):
        return f"User: {self.user} - imagem: {self.imagen}"