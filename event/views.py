from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import EventForm, CreateUserForm
from .filters import EventFilter


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form= CreateUserForm()
        if request.method=='POST':
            form= CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user= form.cleaned_data.get('username')
                messages.success(request, 'Account was created for '+ user)
                return redirect('login')
        context={'form':form}
        return render(request, 'event/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method =='POST':
            username= request.POST.get('username')
            password= request.POST.get('password')

            user =authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or Password is incorrect')
            
        context={}
        return render(request, 'event/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    events =Event.objects.all()
    participants= Participant.objects.all()

    total_participants =participants.count()
    total_events= events.count()
    completed= events.filter(status='Completed').count()
    incomplete= events.filter(status='Incomplete').count()
    pending= events.filter(status='Pending').count()


    context={'events':events, 'participants': participants,'total_participants':total_participants,'total_events':total_events,'completed':completed,'incomplete':incomplete,'pending':pending}

    return render(request, 'event/dashboard.html', context)
@login_required(login_url='login')
def products(request):
    products= Product.objects.all()

    return render(request, 'event/products.html',{'products': products})

@login_required(login_url='login')
def participant(request,pk_test):
    participant= Participant.objects.get(id=pk_test)
    events= participant.event_set.all()
    event_count=events.count()

    myFilter=EventFilter(request.GET, queryset=events)
    events= myFilter.qs
    context={'participant': participant, 'events': events,'event_count':event_count, 'myFilter':myFilter}
    return render(request, 'event/participant.html', context)

@login_required(login_url='login')
def createEvent(request,pk):
    EventFormSet= inlineformset_factory(Participant, Event, fields=('event', 'status'), extra=5)
    participant=Participant.objects.get(id=pk)
    formset=EventFormSet(queryset=Event.objects.none(), instance=participant)
    #form=EventForm(initial={'participant':participant})
    if request.method=='POST':
        #print('Printing post:', request.POST)
        #form= EventForm(request.POST)
        formset=EventFormSet(request.POST, instance=participant)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context={'formset':formset}
    return render(request, 'event/event_form.html', context)

@login_required(login_url='login')
def updateEvent(request, pk):
    event= Event.objects.get(id=pk)
    form= EventForm(instance=event)

    if request.method=='POST':
        form= EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('/')
        
    context={'form': form}
    return render(request, 'event/event_form.html', context)

@login_required(login_url='login')
def deleteEvent(request,pk):
    event= Event.objects.get(id=pk)
    if request.method =="POST":
        event.delete()
        return redirect('/')
    
    context={'item':event}
    return render(request, 'event/delete.html', context)

