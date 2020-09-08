from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'
urlpatterns = [
    # path('login/', views.user_login, name='login')
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('change-password/', auth_views.PasswordChangeView.as_view(success_url='done'),  # append 'done' twith current (change-password/) url, and, will be redirected to resulting url if password change is success
         name='change-password'),
    path('change-password/done/', auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
]
