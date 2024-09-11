from django.shortcuts import render, redirect,HttpResponse
from django.urls import reverse
from . import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def custom404(request, exception):
    return render(request, '404.html')

def index(request):
    if request.user.is_superuser:
        todos = models.Todo.objects.all()
        return render(request, 'index.html', {'todos': todos, 'ID': request.user, 'admin' : True})
    elif request.user.is_authenticated:
        todos = models.Todo.objects.filter(user = request.user)
        return render(request, 'index.html', {'todos': todos, 'ID': request.user})
    else:
        return render( request, "index.html", { 'login': True ,'ID': None } )
def list(request):
     if request.user.is_superuser:
        todos = models.Todo.objects.all()
        return render(request, 'list.html', {'todos': todos, 'ID': request.user, 'admin' : True})
     elif request.user.is_authenticated:
        todos = models.Todo.objects.filter(user = request.user)
        return render(request, 'list.html', {'todos': todos, 'ID': request.user})
     else:
        return render( request, "list.html", { 'login': True ,'ID': None } )
def about(request):
     if request.user.is_authenticated:
         return render(request, 'about.html', { 'ID': request.user})
     else:
        return render( request, "about.html"  )
         
def submit(request):
    if request.user.is_authenticated:
        todos = models.Todo.objects.filter(user = request.user)
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            if models.Todo.objects.filter(title=title, content= content, user = request.user):
                return render( request, "index.html" , {'todoavailable' : True , 'todos' : todos,'ID': request.user})
            else:
                models.Todo.objects.create(title=title, content=content, user = request.user)
                return redirect('/')
        else:
            return render( request, "index.html" , {'falsemesg' : True , 'todos' : todos,'ID': request.user})
    else:
        return render( request, "index.html", { 'login': True ,'ID': None } )
     
def delete(request, title,content):
    deletetodo = models.Todo.objects.get(title = title, content=content, user = request.user)
    deletetodo.delete()
    return redirect('/')


def search(request):
    if request.user.is_superuser:
        title = request.POST.get('searchinput')
        todo = models.Todo.objects.filter(title = title)
        return render(request, 'search.html', {'todo': todo, 'ID': request.user, 'admin' : True})
    elif request.user.is_authenticated:
        title = request.POST.get('searchinput')
        todo = models.Todo.objects.filter(title = title, user = request.user)
        return render( request, "search.html" , {'todo' : todo, 'ID': request.user})
    else:
        return render( request, "index.html", { 'login': True ,'ID': None } )
def loginuser(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        # Check if the user already exists
        if User.objects.filter(username=username).exists():
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('index'))
            else:
                return render(request, "login.html", {'wrongpas': True})
        elif email:
            # Create a new user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            user.save()
            user = authenticate(username=username, password=password)
            login(request, user )
            return redirect(reverse('index'))
        else:
            return render(request, "login.html", {'wrongpas': True})
    else:
        return render(request, "login.html", {'wrongpas': False})

def logoutuser(request):
    logout(request)
    return redirect('/')

def account(request):
    if request.user.is_authenticated:
        todos = models.Todo.objects.filter(user = request.user)
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('new_password')
            oldpassword = request.POST.get('old_password')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            deleteaccount = request.POST.get('deleteaccount')
            old_title = request.POST.get('old_title')
            old_content = request.POST.get('old_content')
            new_title = request.POST.get('title')
            new_content = request.POST.get('content')
            if password:
                 if request.user.check_password(oldpassword):
                    request.user.set_password(password)
                    request.user.save()
                    return render(request, "index.html", {'todos': todos, 'ID': request.user, 'alert' : 'Password changed Successfully.'})
                 else:
                    
                    return render(request, "index.html", {'todos': todos, 'ID': request.user, 'wrongpas' : True})
                     
            if username:
                request.user.first_name = first_name
                request.user.last_name = last_name
                request.user.save()
                return render(request, "index.html", {'todos': todos, 'ID': request.user, 'alert' : 'Username changed Successfully.'})
            if deleteaccount:
                request.user.delete()
                return redirect('/') 
            if old_content and new_content:
                todo = models.Todo.objects.get(user=request.user, title = old_title, content=old_content)
                todo.title = new_title
                todo.content = new_content
                todo.save()
                return redirect('/')
   
    return redirect('/')
