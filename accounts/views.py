from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.views.generic import CreateView, FormView, View
from django.contrib.auth import authenticate, login, get_user_model, logout

# Create your views here.


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/account/login/'


class LoginView(FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        # next_post = request.POST.get('next')
        # redirect_path = next_ or next_post or None
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        return super(LoginView, self).form_invalid(form)


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('/')