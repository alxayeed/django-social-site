from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'
urlpatterns = [
    # path('login/', views.user_login, name='login')
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # Changing Password
    path('change-password/', auth_views.PasswordChangeView.as_view(success_url='done'),  # append 'done' twith current (change-password/) url, and, will be redirected to resulting url if password change is success
         name='change-password'),
    path('change-password/done/', auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
    # Resetting Password
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             success_url=reverse_lazy('account:password_reset_done')),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             success_url=reverse_lazy('account:password_reset_complete')),
         name='password_reset_confirm'),
    path('password-reset/success/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_success.html'),
         name='password_reset_complete'),
    # Register user
    path('register/', views.register, name='register'),
    path('update-profile/', views.update_profile, name='update-profile'),
    path('users/', views.user_list, name='user_list'),
    path('users/follow/', views.user_follow, name='user_follow'),
    path('users/<username>/', views.user_details, name='user_detail'),

]
