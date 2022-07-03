from django.shortcuts import render
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template

from .models import NewsletterUser, Newsletter
from .forms import NewsletterUserSignupForm

def newsletter_signup(request):
    form = NewsletterUserSignupForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        if NewsletterUser.objects.filter(email=instance.email).exists():
            messages.warning(request, 'Your Email already exists in our databasee',
                             'alert alert-warning alert-dismissible'
                             )
        else:
            instance.save()
            messages.success(request, 'Your Email has been submitted successfuly',
                             'alert alert-success alert-dismissible'
                             )
            subject = 'Thank you for subscribing to our newsletter'
            from_email = settings.EMAIL_HOST_USER
            to_email = [instance.email]
            with open(settings.BASE_DIR / 'templates/newsfeed/sign_up_email.txt') as f:
                signup_message = f.read()
            message = EmailMultiAlternatives(
                subject=subject,
                body=signup_message,
                from_email=from_email,
                to=to_email
            )
            html_template = get_template('newsfeed/sign_up_email.html').render()
            message.attach_alternative(html_template, 'text/html')
            message.send()

    context = {
        'form': form,

    }
    return render(request, 'newsfeed/index.html', context)

def newsletter_unsubscribe(request):
    form = NewsletterUserSignupForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        if NewsletterUser.objects.filter(email=instance.email).exists():
            NewsletterUser.objects.filter(email=instance.email).delete()
            messages.success(request, 'Your Email has been removed from our database',
                             'alert alert-success alert-dismissible'
                             )
            subject = 'You have successfuly unsubscribed from our Newsletter'
            from_email = settings.EMAIL_HOST_USER
            to_email = [instance.email]

            with open(settings.BASE_DIR / 'templates/newsfeed/unsubscribe_email.txt') as f:
                signup_message = f.read()
            message = EmailMultiAlternatives(
                subject=subject,
                body=signup_message,
                from_email=from_email,
                to=to_email
            )
            html_template = get_template('newsfeed/unsubscribe_email.html').render()
            message.attach_alternative(html_template, 'text/html')
            message.send()

        else:
            messages.warning(request, 'Your email does not exist in our database',
                             'alert alert-warning alert-dismissible'
                             )

    context = {
        'form': form,

    }
    return render(request, 'newsfeed/unsubscribe.html', context)
