from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt
from .models import User

# Create your views here.
def index(request):
    request.session.flush()
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        errors = User.objects.reg_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hashed_pw)
        request.session['user_id'] = new_user.id
        return redirect('/weddings')
    return redirect('/')

def login(request):
    if request.method == 'POST':
        errors = User.objects.log_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        this_user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = this_user.id
        return redirect('/weddings')
    return redirect('/')

def weddings(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'all_weddings': Wedding.objects.all(),
        'user': user,
        
    }
    return render(request, 'weddings.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

def new_wedding(request):
    if 'user_id' not in request.session:
        return redirect('/')
    return render(request, 'new_wedding.html')

def create_wedding(request):
    if request.method == 'POST':
        errors = Wedding.objects.validate(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/weddings/new')
        new_wedding = Wedding.objects.create(
            wedder_one=request.POST['wedder_one'],
            wedder_two=request.POST['wedder_two'],
            wedding_date=request.POST['wedding_date'],
            address=request.POST['address'],
            planner=User.objects.get(id=request.session['user_id'])
        )
        return redirect(f'/weddings')
    return redirect('/weddings/new')

def one_wedding(request, wed_id):
    if 'user_id' not in request.session:
        return redirect('/')
    this_wedding = Wedding.objects.filter(id=wed_id)
    if len(this_wedding) != 1:
        return redirect('/weddings')
    context = {
        'wedding': this_wedding[0]
    }
    return render(request, 'one_wedding.html', context)

def delete_wedding(request, wed_id):
    if request.method == 'POST':
        this_wedding = Wedding.objects.filter(id=wed_id)
        if len(this_wedding) != 1:
            return redirect('/weddings')
        elif this_wedding[0].planner.id != request.session['user_id']:
            return redirect('/weddings')
        this_wedding[0].delete()
    return redirect('/weddings')

def add_guest(request, wed_id):
    if request.method == 'POST':
        this_user = User.objects.get(id=request.session['user_id'])
        this_wedding = Wedding.objects.filter(id=wed_id)
        if len(this_wedding) != 1:
            return redirect('/weddings')
        elif this_wedding[0].planner.id == this_user:
            return redirect('/weddings')
        this_wedding[0].guests.add(this_user)
    return redirect('/weddings')

def remove_guest(request, wed_id):
    if request.method == 'POST':
        this_user = User.objects.get(id=request.session['user_id'])
        this_wedding = Wedding.objects.filter(id=wed_id)
        if len(this_wedding) != 1:
            return redirect('/weddings')
        elif this_wedding[0].planner.id == this_user:
            return redirect('/weddings')
        this_wedding[0].guests.remove(this_user)
    return redirect('/weddings')
    