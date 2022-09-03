from http.client import HTTPResponse
from telnetlib import AUTHENTICATION
from tokenize import generate_tokens
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from glss import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes#,force_text
#from .tokens import generate_token
from django.core.mail import EmailMessage,send_mail
# from django.contrib.auth.views import PasswordResetView
#from django.utils.encoding import force_text
#from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode



# Create your views here.
def home(request):
    u_email = ""
    if request.method == "POST":
         email = request.POST['email']
    subject = "Welcome to Project-Stream!!"
    message = "Hello! ! \n" + "Welcome to Project Stream! \nWe're so happy you're here. We founded Project Stream because we wanted to create a trustworthy and inspiring place for you to find everything you need to stream and live well.\n\n With Best Regards,\n Team Project Stream"
    from_email = settings.EMAIL_HOST_USER
    to_list = [home.email]
    send_mail(subject, message, from_email, email, fail_silently=True)

    return render(request, "authentication/landing.html")
    #return HttpResponse("Test")

def dashboard(request):
    return render(request, "authentication/dashboard.html")

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist!")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request, "Email already registered!")
            return redirect('home')

        if len(username)>15:
            messages.error(request, "Username length long max.15!")

        if password1 != password2:
            messages.error(request, "Password doesn't Match!")

        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric!")
            return redirect('home')
        
        myuser = User.objects.create_user(username, email, password1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.password2 = password2
        myuser.is_active = True
        myuser.save()
        messages.success(request, "Your Account Has Been Created.")


        #Welcome Email

        subject = "Welcome to Project-Stream!!"
        message = "Hello " + myuser.first_name + "! ! \n" + "Welcome to Project Stream! \nWe're so happy you're here. We founded Project Stream because we wanted to create a trustworthy and inspiring place for you to find everything you need to stream and live well.\n\n With Best Regards,\n Team Project Stream"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)


        # Email Address Confirmation email ---> Error in conformation mail

        # current_site= get_current_site(request)
        # email_subject = "Confirm your email to access PJS"
        # # message2 = render_to_string('email_confirmation.html',{ dict }),{ #error may occur .html',{
        # message2 = render_to_string('email_confirmation.html',{
        #     'name' : myuser.first_name,
        #     'domain' : current_site.domain,
        #     'uid' : urlsafe_base64_encode(force_bytes(myuser.pk)),
        #     'token' : generate_token.make_token(myuser),
        # })# } may be :(
        # email = EmailMessage(
        #     email_subject,
        #     message2,
        #     settings.EMAIL_HOST_USER,
        #     [myuser.email],
        # )
        # email.fail_silently = True
        # email.send()

        return redirect('signin')   

    return render(request, "authentication/signup.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')

        user = authenticate(username=username, password=password1) #error may come

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/home.html", {'fname': fname})

        else:
            messages.error(request, "Bad Credentials")
            # return redirect('signup')  --> wrong password hanyo vane signup ma redirect gar xa


    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    #messages.success(request, "Logged Out Successfully")
    return redirect('home')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_tokens.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return redirect('home')
    else:
        return render(request, 'activation_failed.html')

# def subscribe(request):
#     if request.method == "POST":
#         u_email = request.POST['email']
#     subject = "Welcome to Project-Stream!!"
#     message = "Hello " + myuser.first_name + "! ! \n" + "Welcome to Project Stream! \nWe're so happy you're here. We founded Project Stream because we wanted to create a trustworthy and inspiring place for you to find everything you need to stream and live well.\n\n With Best Regards,\n Team Project Stream"
#     from_email = settings.EMAIL_HOST_USER
#     to_list = [u_email]
#     send_mail(subject, message, from_email, to_list, fail_silently=True)
