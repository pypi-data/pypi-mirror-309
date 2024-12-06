from django.shortcuts import render, redirect
from admin_atlantis.forms import RegistrationForm,LoginForm,UserPasswordChangeForm,UserPasswordResetForm,UserSetPasswordForm
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

def signup(request):
  if request.method == 'POST':
      form = RegistrationForm(request.POST)
      if form.is_valid():
        form.save()
        print('Account created successfully!')
        return redirect('/accounts/login/')
      else:
        print("Registration failed!")
  else:
    form = RegistrationForm()
  context = {'form': form}
  return render(request, 'accounts/register.html', context)

class AuthSignin(auth_views.LoginView):
  template_name = 'accounts/login.html'
  form_class = LoginForm
  success_url = '/'

class UserPasswordChangeView(auth_views.PasswordChangeView):
  template_name = 'accounts/change-password.html'
  form_class = UserPasswordChangeForm 

class UserPasswordResetView(auth_views.PasswordResetView):
  template_name = 'accounts/recover-password.html'
  form_class = UserPasswordResetForm

class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
  template_name = 'accounts/reset-password.html'
  form_class = UserSetPasswordForm

@login_required(login_url='/accounts/login/')
def user_logout_view(request):
  logout(request)
  return redirect('/accounts/login')

@login_required(login_url='/accounts/login/')
def password_change_done(request):
    return render(request, 'accounts/password-reset-done.html') 

@login_required(login_url='/accounts/login/')
def recover_password(request):
    return render(request,'accounts/recover-password.html')        

# Pages -- Dashboard
def dashboard(request):
    context = {
        'active_page': 'dashboard' 
    }
    return render(request, 'index.html',context)

@login_required(login_url='/accounts/login/')
def starter_template(request):
    return render(request, 'starter-template.html')

# Components
@login_required(login_url='/accounts/login/')
def avatars(request):
    context = {
        'active_page': 'base' 
    }
    return render(request, 'components/avatars.html',context)

@login_required(login_url='/accounts/login/')
def buttons(request):
    context = {
        'active_page': 'base' 
    }
    return render(request, 'components/buttons.html',context)

@login_required(login_url='/accounts/login/')
def flaticons(request):
    context = {
        'active_page': 'base' 
    }
    return render(request, 'components/flaticons.html',context)    

@login_required(login_url='/accounts/login/')
def fontawesome(request):
    context = {
        'active_page': 'base' 
    }
    return render(request, 'components/font-awesome-icons.html',context)

@login_required(login_url='/accounts/login/')
def simple_line_icons(request):
    context = {
        'active_page': 'base' 
    }
    return render(request, 'components/simple-line-icons.html',context)

@login_required(login_url='/accounts/login/')
def gridsystem(request):
    context = {
        'active_page': 'base' 
    }
    return render(request, 'components/gridsystem.html',context)  

@login_required(login_url='/accounts/login/')
def panels(request):
    context = {
        'active_page': 'base' 
    }
    return render(request, 'components/panels.html',context)

@login_required(login_url='/accounts/login/')
def notifications(request):
    context = {
        'active_page': 'base' 
    }
    return render(request, 'components/notifications.html',context)

@login_required(login_url='/accounts/login/')
def sweetalert(request):
    context = {
        'active_page': 'base' 
    }
    return render(request, 'components/sweetalert.html',context)

@login_required(login_url='/accounts/login/')
def typography(request):
    context = {
        'active_page': 'base' 
    }
    return render(request, 'components/typography.html',context)


# Sidebar layouts
@login_required(login_url='/accounts/login/')
def sidebarone(request):
    context = {
        'active_page': 'sidebar' 
    }
    return render(request, 'sidebar-style-1.html',context)

@login_required(login_url='/accounts/login/')
def sidebar_overlay(request):
    context = {
        'active_page': 'sidebar' 
    }
    return render(request, 'overlay-sidebar.html',context)


@login_required(login_url='/accounts/login/')
def sidebar_compact(request):
    context = {
        'active_page': 'sidebar' 
    }
    return render(request, 'compact-sidebar.html',context)  

@login_required(login_url='/accounts/login/')
def sidebar_static(request):
    context = {
        'active_page': 'sidebar' 
    }
    return render(request, 'static-sidebar.html',context)

@login_required(login_url='/accounts/login/')
def icon_menu(request):
    context = {
        'active_page': 'sidebar' 
    }
    return render(request, 'icon-menu.html',context)


# Forms
@login_required(login_url='/accounts/login/')
def forms(request):
    context = {
        'active_page': 'forms' 
    }
    return render(request, 'forms/forms.html',context)

# Tables  
@login_required(login_url='/accounts/login/')  
def datatables(request):
    context = {
        'active_page': 'tables' 
    }
    return render(request, 'tables/datatables.html',context)

@login_required(login_url='/accounts/login/')
def tables(request):
    context = {
        'active_page': 'tables' 
    }
    return render(request, 'tables/tables.html',context)

# Charts 
@login_required(login_url='/accounts/login/') 
def charts(request):
    context = {
        'active_page': 'charts' 
    }
    return render(request, 'charts/charts.html',context)

@login_required(login_url='/accounts/login/')
def sparkline(request):
    context = {
        'active_page': 'charts' 
    }
    return render(request, 'charts/sparkline.html',context) 

# Maps
@login_required(login_url='/accounts/login/')
def maps(request):
    context = {
        'active_page': 'maps' 
    }
    return render(request, 'maps/jqvmap.html',context)

# Widgets
@login_required(login_url='/accounts/login/')
def widgets(request):
    context = {
        'active_page': 'widgets' 
    }
    return render(request, 'widgets.html',context)               