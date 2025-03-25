from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from accounts.models import Account
from django.http import HttpResponseRedirect
from datetime import timedelta
from django.utils.timezone import now
from django.conf import settings
import random

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_otp(request, user):
    otp = random.randint(11111, 99999)
    request.session['user_id'] = user.id
    request.session['otp'] = otp
    request.session['otp_expiry'] = (now() + timedelta(minutes=5)).isoformat()

    # Render both HTML and text versions
    html_message = render_to_string('emails/otp_email.html', {
        'otp': otp,
        'user': user
    })
    plain_message = strip_tags(html_message)  # Creates text version automatically

    try:
        email = EmailMultiAlternatives(
            subject='OTP for Registration - PML Bank PLC',
            body=plain_message,  # This is the text version
            from_email=settings.EMAIL_HOST_USER,
            to=[user.email],
        )
        email.attach_alternative(html_message, "text/html")  # This attaches HTML version
        email.send()
        return otp
    except Exception as e:
        return None

def mask_email(email):
    user, domain = email.split('@')
    masked_user = user[:3] + '*' * (len(user) - 5) + user[-2:]
    masked_email = f"{masked_user}@{domain}"
    return masked_email



def create_accounts(request):
    if request.method == 'POST':
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        email = request.POST.get('email')
        pnumber = request.POST.get('phone_number')
        username = request.POST.get('username')
        deposit = request.POST.get('deposit')
        p1 = request.POST.get('password1')
        p2 = request.POST.get('password2')
        
        if User.objects.filter(username=username).exists():
            user =User.objects.get(username=username)
            if user.is_active:
                return render(request, 'accounts/create_account.html', {'error': 'Username already exists, try others.'})
            else:
                user.delete()
        
        if User.objects.filter(email=email).exists():
            user =User.objects.get(email=email)
            if user.is_active:
                return render(request, 'accounts/create_account.html', {'error': 'email already exists, try others.'})
            else:
                user.delete()

        if p1 != p2:
            return render(request, 'accounts/create_account.html', {'error': 'Password and Confirm Password do not match.'})

        user = User.objects.create_user(
            first_name=fname,
            last_name=lname,
            username=username,
            email=email,
            password=p1,
        )
        user.is_active=False
        user.save()
        user_count = User.objects.count()
        account_number = 1000 + user_count + 1

        account = Account.objects.create(
            user=user,
            account_number=account_number,
            balance=int(deposit) if deposit else 0
        )
        account.phone_number=pnumber,
        account.save()

        request.session.pop('user_id', None)
        request.session.pop('otp', None)
        request.session.pop('otp_expiry', None)


        send_otp(request, user)
        return redirect('verify_otp')

    return render(request, 'accounts/create_account.html')


def verify_otp(request, user_input_otp):
    stored_otp = request.session.get('otp')
    expiry_time = request.session.get('otp_expiry')

    if not stored_otp or not expiry_time:
        return False, "OTP has expired or was not found."

    if now() > now().fromisoformat(expiry_time):
        request.session.pop('otp', None)
        request.session.pop('otp_expiry', None)
        return False, "OTP has expired."

    if str(stored_otp) != str(user_input_otp):
        return False, "Invalid OTP."

    # OTP is correct, clear session
    request.session.pop('otp', None)
    request.session.pop('otp_expiry', None)
    return True,

def verify_otp_view(request):
    user_id = request.session.get('user_id')
    user= User.objects.get(id=user_id)
    if request.method == 'POST':
        otp= int(f'{request.POST.get('otp1')}{request.POST.get('otp2')}{request.POST.get('otp3')}{request.POST.get('otp4')}{request.POST.get('otp5')}')
        verify_status = verify_otp(request, otp)
        if not verify_status[0]:
            return render(request, 'accounts/otp_verification.html',{'error':verify_status[1]})
        elif verify_status[0]:
            account = Account.objects.get(user=user)
            account.is_active =True
            user.is_active=True
            user.save()
            account.save()
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/otp_verification.html',{'error':'exception error'})
    
    return render(request, 'accounts/otp_verification.html',{'email':mask_email(user.email)})


def resend_otp(request):
    user_id = request.session.get('user_id')    
    request.session.pop('user_id', None)
    request.session.pop('otp', None)
    request.session.pop('otp_expiry', None)
    user= User.objects.get(id=user_id)
    send_otp(request, user)
    return redirect('verify_otp')




def login_views(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'accounts/login_account.html', {'error': 'Account not fount on this email.'})

        user = authenticate(request, username=user.username, password=password)
        
        if user is None:
            return render(request, 'accounts/login_account.html', {'error': 'Email or Password is incorrect.'})

        login(request, user)
        return redirect('home')

    return render(request, 'accounts/login_account.html')


def change_password(request):
    if request.method=="POST":
        o_pass = request.POST.get('old_password')
        n_pass1 = request.POST.get('new_password1')
        n_pass2 = request.POST.get('new_password2')
        user = request.user
        if not user.check_password(o_pass):
            return render(request, 'accounts/change_password.html', {'error': 'Old password is incorrect.'})

        if n_pass1 != n_pass2:
            return render(request, 'accounts/change_password.html', {'error': 'New passwords do not match.'})

        user.set_password(n_pass1)
        user.save()
        login(request, user)
        return redirect('home')
    return render(request, 'accounts/change_password.html')


def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')