from django.urls import path
from blogApp import views
from blogApp.views import *
from django.contrib.auth.views import LogoutView


urlpatterns = [
   
   path('', views.inicio, name='inicio'),

    #Vistas inicio de sesion, registo, logout

   path('login/', views.login_usuario, name= 'login'),
   path('registro/', views.registro, name= 'registro'),
   path('logout/', LogoutView.as_view(template_name= 'blogApp/logout.html'), name= 'logout'),
   path('edit_profile/',update_user, name='edit_profile'),
   path('perfil/', views.perfil, name="perfil"),
   path('upload_avatar/', upload_avatar, name="upload_avatar"),

   # Vista para cambiar contraseña
   path('password/', PasswordsChangeView.as_view(template_name= 'blogApp/change-password.html'), name= 'password'),
   path('password_success', views.password_success, name="password_success"),

   
   path('pages/', views.pages, name= 'pages'),
   path('about/', views.about, name= 'about'),
   

   #url para CRUD posteos
   path('<slug>', Post_detalle.as_view(), name='post'), 
   path('crear_post/', Crear_post.as_view(), name='crear_post'),
   path('editar_post/<slug>', Editar_post.as_view(), name='editar_post'),
   path('<slug>/eliminar', Eliminar_post.as_view(), name='eliminar_post'),

   #Like para posts
   path('like/<int:pk>', views.Like_view, name="like_post")

]