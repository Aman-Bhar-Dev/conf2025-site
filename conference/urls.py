from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('', views.index, name='home'),
    path('submit/', views.abstract_submit, name='submit'),
    path('thankyou/', views.thank_you, name='thankyou'),
    path('thankyouab/', views.thank_you_abstract, name='thankyouab'),


    # Auth views
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Password reset
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='conference/password_reset.html'), name='password_reset'),
    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(template_name='conference/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='conference/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='conference/index.html'), name='password_reset_complete'),

    # Profile and Pages
    path('profile/', views.profile_view, name='profile'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('itinerary/', views.itinerary, name='itinerary'),
    path('pricing/', views.pricing_view, name='pricing'),

    #payment
    path('checkout/<str:paper_id>/', views.checkout_view, name='checkout'),
    path('payment-summary/<str:paper_id>/', views.payment_summary_view, name='payment_summary'),
    path('payment/thank-you/', views.payment_confirmation_view, name='thank_you'),
    path('visitor/register/', views.visitor_registration_view, name='visitor_registration'),
    path('super-edit/<str:paper_id>/', views.super_edit_abstract, name='super_edit_abstract'),

]



