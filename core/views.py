from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView
from core.forms import SignUpForm, ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django_otp.forms import OTPAuthenticationForm
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from core.tokens import account_activation_token
from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.core.mail import EmailMessage
from django_otp import match_token
# Sign Up View
class SignUpView(View):
    form_class = SignUpForm
    template_name = 'commons/signup.html'

    def get_user_totp_device(self,user, confirmed=None):
        devices = devices_for_user(user, confirmed=confirmed)
        for device in devices:
            if isinstance(device, TOTPDevice):
                return device

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = True # Deactivate account till it is confirmed
            user.save()
            device = self.get_user_totp_device(user)
            if not device:
                device = user.totpdevice_set.create(confirmed=True)
                print(device.config_url)
            current_site = get_current_site(request)
            mail_subject = 'DJANGO OTP DEMO'
            message = render_to_string('emails/account_activation_email.html', {
                'user': user,
                'qr_code': device.config_url,
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.content_subtype = "html"
            email.send()


            messages.success(request, ('Please Confirm your email to complete registration.'))

            return redirect('login')

        return render(request, self.template_name, {'form': form})



from django.contrib.auth.models import User


class AccountLoginView(FormView):

    template_name = 'commons/login.html'
    form_class = OTPAuthenticationForm
    success_url = '/'

    def form_invalid(self, form):
        return super().form_invalid(form)

    def form_valid(self, form):

        # self.request.user returns AnonymousUser
        # self.request.user.is_authenticated returns False
        # self.request.user.is_verified() returns False

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        otp_token = form.cleaned_data.get('otp_token')
        otp_device = form.cleaned_data.get('otp_device')

        user = authenticate(request=self.request, username=username, password=password)

        if user is not None:

            device_match = match_token(user=user, token=otp_token)

            # device_match returns None

            auth_login(self.request, user)

            # self.request.user returns admin@mywebsite.com
            # self.request.user.authenticated returns True
            # self.request.user.is_verified returns AttributeError 'User' object has no attribute 'is_verified'
            # user.is_verified returns AttributeError 'User' object has no attribute 'is_verified'

        return super().form_valid(form)


# Edit Profile View
class ProfileView(UpdateView):
    model = User
    form_class = ProfileForm
    success_url = reverse_lazy('home')
    template_name = 'commons/profile.html'

