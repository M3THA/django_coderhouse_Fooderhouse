
from nntplib import ArticleInfo
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from requests import post

from blogApp.forms import User_register_form, Crear_form, EditProfileForm
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import PasswordChangeView
from .forms import *



from .models import *

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.urls import reverse_lazy




def inicio(request):
    return render(request, "blogApp/inicio.html")

#ORIANA
#Vista de login

def login_usuario(request):

    if request.method == 'POST':

        form = AuthenticationForm(request, data= request.POST)

        if form.is_valid:

            usuario= request.POST['username']
            contrasena= request.POST['password']

            user= authenticate(username=usuario, password=contrasena) 

            if user is not None:

                login(request, user)
                

                return render(request, "blogApp/inicio_exito.html", {'mensaje':f"te has logueado {usuario}"} )
            else: 
                
                return render(request, "blogApp/login.html", {'form': form,  'mensaje': f"Error, datos incorrectos"} )
                
            
        else:
            
            return render(request, "blogApp/inicio.html", {'mensaje': "Error, formulario erroneo"} )

    else:

        form = AuthenticationForm()

        return render(request, "blogApp/login.html", {'form': form})

# Vista de registro

def registro(request):

    if request.method == 'POST':

        form= User_register_form(request.POST)

        if form.is_valid():

            username= form.cleaned_data['username']

            form.save()
            return render(request, "blogApp/inicio.html", {'form':form, 'mensaje':f"Usuario creado: {username}"} )

    else:
        form= User_register_form()

    return render(request,'blogApp/registro.html', {'form': form} )

# Vista de editar perfil

@login_required
def update_user(request):
    
    usuario= request.user

    if request.method == 'POST':
        form= EditProfileForm(request.POST, instance=usuario)
       
        if form.is_valid():
            data= form.cleaned_data
            
            usuario.username= data['username']
            usuario.email= data['email']
            usuario.first_name= data['first_name']
            usuario.last_name= data['last_name']
           
            usuario.save()

            return render(request, 'blogApp/inicio.html', {'usuario':usuario, 'mensaje': 'Perfil editado con exito'})

    else:
        print(usuario)
        form = EditProfileForm(instance=usuario)
            
   
    return render (request, 'blogApp/edit_profile.html', {'form':form, 'user':usuario.username})

@login_required()
def perfil(request):

    avatar = Avatar.objects.filter(user=request.user)

    if len(avatar) > 0:
        imagen = avatar[0].imagen.url
        return render(request, 'blogApp/perfil.html', {"image_url": imagen})

    return render (request, 'blogApp/perfil.html')


@login_required()
def upload_avatar(request):   
    
    
    if request.method == "POST":

        formulario = AvatarForm(request.POST,request.FILES)

        if formulario.is_valid():

            usuario = request.user

            avatar = Avatar.objects.filter(user=usuario)

            if len(avatar) > 0:
                avatar = avatar[0]
                avatar.imagen = formulario.cleaned_data["imagen"]
                avatar.save()

            else:
                avatar = Avatar(user=usuario, imagen=formulario.cleaned_data["imagen"])
                avatar.save()
            
        return redirect("perfil")
    else:

        formulario = AvatarForm()
        return render(request, "blogApp/upload_avatar.html", {"form": formulario})


# Vista de about

def about(request):

    return render(request, 'blogApp/about.html')


class PasswordsChangeView(PasswordChangeView):
    form_class= PasswordChangingForm
    success_url= reverse_lazy('password_success')

def password_success(request):
	return render(request, 'blogApp/password_success.html', {})

#NICOLAS
#Función para pages, con paginador 
def pages(request):
    posteos= Blog_post.objects.all()
    page= request.GET.get("page")
    paginator=Paginator(posteos, 2)
    try:
        posteos= paginator.page(page)
    except PageNotAnInteger:
        posteos= paginator.page(1)
    except EmptyPage:
        posteos= paginator.page(paginator.num_pages)

    return render(request, "blogApp/pages.html", {'posteos':posteos}, )


 
class Post_detalle(DetailView):
    model= Blog_post
    template_name= "blogApp/post.html"
    slug_field= "slug"


def Like_view(request, pk):
    post= get_object_or_404(Blog_post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    titulo= post.slug
    return HttpResponseRedirect(reverse('post', args=[titulo]))


class Crear_post(CreateView):
    model= Blog_post
    form_class= Crear_form
    template_name= 'blogApp/crear_post.html'

class Editar_post(UpdateView):
    model= Blog_post
    template_name= 'blogApp/editar_post.html'
    form_class= Crear_form
    
class Eliminar_post(DeleteView):
    model= Blog_post
    template_name= 'blogApp/borrar_post.html'
    success_url= reverse_lazy('pages')



