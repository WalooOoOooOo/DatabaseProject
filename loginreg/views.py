from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import CustomUser
from Society.models import Society
import requests
from django.conf import settings
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

def reset_password(request, uidb64, token):
    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            return HttpResponse("Passwords do not match. Please try again.")

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return HttpResponse("Invalid link.")

        if default_token_generator.check_token(user, token):
            user.set_password(password1)
            user.save()
            return redirect('login')  
        else:
            return HttpResponse("The reset link is invalid or has expired.")

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if not default_token_generator.check_token(user, token):
            return HttpResponse("The reset link is invalid or has expired.")
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return HttpResponse("Invalid link.")

    return render(request, 'reset_password.html', {'uidb64': uidb64, 'token': token})



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return HttpResponse("This email is not registered in our system.")

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = request.build_absolute_uri(f"/reset_password/{uid}/{token}/")

        send_mail(
            'Password Reset Request',
            f'Click the link below to reset your password:\n{reset_link}',
            'admin@example.com', 
            [email],
            fail_silently=False,
        )
        return HttpResponse("A password reset link has been sent to your email.")

    return render(request, 'forgot_password.html')



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
    if request.user.is_authenticated:  
        admin_panel_accessible = Society.objects.filter(admins=request.user).exists()
    
    return render(request, 'home.html', {'admin_panel_accessible': admin_panel_accessible})


import requests
from django.conf import settings

def loginpage(request):
    if request.method == 'POST':
        uname = request.POST['username']
        pword = request.POST['pass']
        recaptcha_response = request.POST.get('g-recaptcha-response')

        captcha_url = 'https://www.google.com/recaptcha/api/siteverify'
        captcha_data = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY, 
            'response': recaptcha_response
        }
        captcha_response = requests.post(captcha_url, data=captcha_data).json()
        if not captcha_response.get('success'):  
            return HttpResponse("Invalid reCAPTCHA. Please try again.")

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

    

