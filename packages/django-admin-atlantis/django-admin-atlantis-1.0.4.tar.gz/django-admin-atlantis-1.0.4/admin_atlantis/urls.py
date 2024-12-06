from django.contrib import admin
from django.urls import path
from admin_atlantis import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('accounts/register/', views.signup, name='signup'),
    path('accounts/login/', views.AuthSignin.as_view(), name='login'),
    path('accounts/logout/', views.user_logout_view, name='logout'),
    path('accounts/change-password/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('accounts/change-password/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('accounts/password_change_done/', views.password_change_done, name='password_change_done'),
    path('accounts/recover-password/', views.recover_password, name='recover_password'),
    path('starter-template/', views.starter_template, name='starter_template'),
    path('components/avatars/', views.avatars, name='avatars'),
    path('components/buttons/', views.buttons, name='buttons'),
    path('components/flaticons/', views.flaticons, name='flaticons'),
    path('components/font-awesome-icons/', views.fontawesome, name='fontawesome'),
    path('components/simple-line-icons/', views.simple_line_icons, name='simple_line_icons'),
    path('components/gridsystem/', views.gridsystem, name='gridsystem'),
    path('components/panels', views.panels, name='panels'),
    path('components/notifications/', views.notifications, name='notifications'),
    path('components/sweetalert/', views.sweetalert, name='sweetalert'),
    path('components/typography/', views.typography, name='typography'),
    path('sidebar-style-1/', views.sidebarone, name='sidebarone'),
    path('sidebar-overlay/', views.sidebar_overlay, name='sidebar_overlay'),
    path('compact-sidebar/', views.sidebar_compact, name='sidebar_compact'),
    path('static-sidebar/', views.sidebar_static, name='sidebar_static'),
    path('icon-menu/', views.icon_menu, name='icon_menu'),
    path('forms/', views.forms, name='forms'),
    path('tables/data-tables/', views.datatables, name='datatables'),
    path('tables/tables/', views.tables, name='tables'),
    path('charts/charts/', views.charts, name='charts'),
    path('charts/sparkline/', views.sparkline, name='sparkline'),
    path('maps/jqvmap/', views.maps, name='maps'),
    path('widgets/', views.widgets, name='widgets'),    
]