from django.urls import path

from . import views

app_name = 'newsletter'
urlpatterns = [
    path('', views.newsletter_signup, name='newsletter_signup'),
    path('unsubscribe/', views.newsletter_unsubscribe, name='newsletter_unsubscribe')
]
