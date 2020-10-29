# How to Django Two-Factor Authentication with OTP

TOTP stands for Time-based One-Time Password. It’s a fairly simple algorithm that involves combining a shared secret key with the current time to generate a verification token that’s only valid for a short amount of time.





### Setup
1. Create a folder and put all the files inside it.
2. Create a virtual environtment - `virtualenv env`
3. Activate VirtualENV - `source env/bin/activate`
4. Run requirements.txt - `pip3 install -r requirements.txt`
5. Run the Application - `python3 manage.py runserver`
6. Go to - http://localhost:8000/

### Email-Setting
`EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'yourgmail@gmail.com'
EMAIL_HOST_PASSWORD = 'yourpassword'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'`

### Attention-Important
To enable the option in Gmail: Sign in to your account in Gmail.com, then open another tab and go to the Less Safe Apps Setting and select "Open".
