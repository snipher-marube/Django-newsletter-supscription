from django.contrib import admin

from .models import Newsletter, NewsletterUser

admin.site.register(Newsletter)
admin.site.register(NewsletterUser)
