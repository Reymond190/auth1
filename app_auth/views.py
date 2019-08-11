from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegisterForm, ProfileAddForm, AddDeviceform
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def start(request):
    return render(request, 'file1.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username= username, password = password)
            messages.success(request,f'Your account has been created {username}! Login to continue!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'registration/register.html', context)

@login_required
def profile(request):
    form = ProfileAddForm
    if request.method == 'POST':
        form = ProfileAddForm(request.POST)
        if form.is_valid():
            return start(request)
    return render(request,'registration/profile.html',{'form':form})

@login_required
def AddDevice(request):
    form = AddDeviceform
    if request.method == 'POST':
        form = AddDeviceform(request.POST)
        if form.is_valid():
            return start(request)
    return render(request,'registration/Add.html',{'form':form})

