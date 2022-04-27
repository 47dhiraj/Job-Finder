from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from validate_email import validate_email
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from .utils import EmailThread
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from .models import User


class RegistrationView(View):
    def get(self, request):
        return render(request, 'auth_app/register.html')
    
    def post(self, request):
        context = {
            'data': request.POST,
            'has_error': False
        }

        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if len(password) < 6:
            messages.add_message(request, messages.ERROR, 'passwords must be minimum of 6 characters')
            context['has_error'] = True
        
        if password != password2:
            messages.add_message(request, messages.ERROR, 'passwords doesn\'t match')
            context['has_error'] = True

        if not validate_email(email):
            messages.add_message(request, messages.ERROR, 'provide a valid & real email address')
            context['has_error'] = True

        try:
            if User.objects.get(email=email):
                messages.add_message(request, messages.ERROR, 'user with that email already exists')
                context['has_error'] = True

        except Exception as e:
            pass


        try:
            if User.objects.get(username=username):
                messages.add_message(request, messages.ERROR, 'user with that username already exists')
                context['has_error'] = True

        except Exception as e:
            pass


        if context['has_error']:
            return render(request, 'auth_app/register.html', context, status=400)


        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.set_password(password)
            user.save()

            current_site = get_current_site(request)
            email_subject = 'Account Activation'
            message = render_to_string('auth_app/activate.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(smart_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })

            email_message = EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                [email]
            )
            EmailThread(email_message).start()

            messages.add_message(request, messages.SUCCESS, 'Account created succesfully! Please, check  your email for account Verification.')
            return redirect('login')

        except:
            messages.add_message(request, messages.ERROR, 'Something went wrong!')
        
        return redirect('login')


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_verified = True
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Account activated successfully !')
            return redirect('login')

        return render(request, 'auth_app/activate_failed.html', status=401)



class LoginView(View):
    def get(self, request):
        return render(request, 'auth_app/login.html')
    
    def post(self, request):
        context = {
            'data': request.POST,
            'has_error': False
        }

        email = request.POST.get('email')
        password = request.POST.get('password')

        if email == '':
            messages.add_message(request, messages.ERROR, 'Email address is required')
            context['has_error'] = True

        if password == '':
            messages.add_message(request, messages.ERROR, 'Password is required')
            context['has_error'] = True

        user = authenticate(request, email=email, password=password)
        print('User instance : ',user)

        if not user and not context['has_error']:
            messages.add_message(request, messages.ERROR, 'Invalid login credentials or account not verified yet.')
            context['has_error'] = True

        if not user.is_verified:
            messages.add_message(request, messages.ERROR, 'Account is not verified. Check email to verify your account.')
            context['has_error'] = True

        if context['has_error']:
            return render(request, 'auth_app/login.html', status=401, context=context)


        login(request, user)
        return redirect('home')


class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')


class RequestResetEmailView(View):
    def get(self, request):
        return render(request, 'auth_app/request_reset_email.html')

    def post(self, request):
        email = request.POST['email']

        if not validate_email(email):
            messages.error(request, 'enter a valid email address')
            return render(request, 'auth_app/request_reset_email.html')

        try:
            user = User.objects.filter(email=email).first()

            if user:
                current_site = get_current_site(request)
                email_subject = '[Reset the password]'
                message = render_to_string('auth_app/reset_password_link.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(smart_bytes(user.pk)),
                    'token': account_activation_token.make_token(user)
                })

                email_message = EmailMessage(
                    email_subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [email]
                )

                EmailThread(email_message).start()

            messages.success(request, 'Sent email with instructions to reset your password')
            return render(request, 'auth_app/request_reset_email.html')
       
        except:
            messages.add_message(request, messages.ERROR, 'Something went wrong!')
        
        return render(request, 'auth_app/request_reset_email.html')


class SetNewPasswordView(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)

            if not account_activation_token.check_token(user, token):
                messages.info(request, 'Invalid reset link, please request new reset link.')
                return render(request, 'auth_app/request_reset_email.html')

        except DjangoUnicodeDecodeError as e:
            messages.success(request, 'Something went wrong. Request new reset link.')
            return render(request, 'auth_app/request_reset_email.html')


        return render(request, 'auth_app/set_new_password.html', context)


    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token,
            'has_error': False
        }

        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if len(password) < 6:
            messages.add_message(request, messages.ERROR, 'passwords must be minimum of 6 characters')
            context['has_error'] = True

        if password != password2:
            messages.add_message(request, messages.ERROR, 'passwords doesn\'t match')
            context['has_error'] = True

        if context['has_error'] == True:
            return render(request, 'auth_app/set_new_password.html', context)

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()

            messages.success(request, 'Password reset successfull !')
            return redirect('login')

        except DjangoUnicodeDecodeError as e:
            messages.error(request, 'Something went wrong! Please, try again after some time.')

        return render(request, 'auth_app/set_new_password.html', context)


class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Successfully logged out')
        return redirect('login')
