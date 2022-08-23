
from django.shortcuts import render
from .models import *
from chatApp.forms import *


# CVB

from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView

# Django authentication

from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

class MessagesList(LoginRequiredMixin, ListView):

    model = Message
    template_name = "chatApp/message_list.html"

class MessageDetail(LoginRequiredMixin, DetailView):

    model = Message
    template_name = "chatApp/message_detail.html"



def crear_mensaje(request):
    print(request.user)
    if request.method == 'POST':
        form= MessagesForm(request.POST)
       
        if form.is_valid():
            data= form.cleaned_data
            
           
            destinatario = User.objects.filter(username=data['reciever'])
            print(destinatario)
            mensaje= Message()
            mensaje.title=data['title']
            mensaje.sender=request.user
            mensaje.reciever=destinatario.get()
            mensaje.content=data['content']
            mensaje.date=datetime.now()
            mensaje.save()
            nuevo_form =MessagesForm()


            return render(request, 'chatApp/message_form.html', {'form':nuevo_form})  
            
    else:
        form =  MessagesForm()
        return render(request, 'chatApp/message_form.html', {'form':form})


class MessageDelete(LoginRequiredMixin, DeleteView):

    model = Message
    success_url = "/chatApp/app/list"
    
    