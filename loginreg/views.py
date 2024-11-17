from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import CustomUser
from Society.models import Society

def SignUpPage(request):
    if request.method=='POST':
        uname=request.POST['username']
        email=request.POST['email']
        pword1=request.POST['password1']
        pword2=request.POST['password2']
        isadmin = request.POST.get('isadmin') == 'on'
        if pword1!=pword2:
            return HttpResponse("Passwords must match !")
        else:
            my_user=CustomUser.objects.create_user(uname,email,pword1)
            my_user.isadmin=isadmin
            my_user.save()
            return redirect('login')
        
    return render(request,'signup.html')


def HomePage(request):
    admin_panel_accessible = False
    societies = None  
    if request.user.is_authenticated:
        societies = Society.objects.filter(admins=request.user)

        admin_panel_accessible = societies.exists()
    return render(request, 'home.html', {
        'admin_panel_accessible': admin_panel_accessible,
        'societies': societies,  
    })


def loginpage(request):
    if request.method == 'POST':
        uname = request.POST['username']
        pword = request.POST['pass']
        user = authenticate(request, username=uname, password=pword)
        if user is not None:
            login(request, user)
            if Society.objects.filter(admins=user).exists():
                return redirect('apanel')
            else:
                return redirect('home')
        else:
            return HttpResponse("Your Username or Password is incorrect.")
    return render(request, 'login.html')


def logoutpage(request):
    logout(request)
    return redirect('login')

    

