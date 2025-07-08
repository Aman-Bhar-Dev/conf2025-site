from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='home'),
    path('submit/', views.abstract_submit, name='submit'),
    path('thankyou/', views.thank_you, name='thankyou'),
    path('thankyouab/', views.thank_you_abstract, name='thankyouab'),
    path('load-superuser/', views.load_superuser),
    path("create-admin-user/", views.create_admin_user),


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

    # Payment & Participation
    path('payment/<str:paper_id>/', views.payment_view, name='payment'),
    path('confirm-participation/<str:paper_id>/', views.confirm_participation_view, name='confirm_participation'),
    path('checkout/<str:paper_id>/', views.checkout_view, name='checkout'),
    path('payment-summary/<str:paper_id>/', views.payment_summary, name='payment_summary'),
]
