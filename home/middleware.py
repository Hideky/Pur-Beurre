from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

class LoginFormMiddleware(MiddlewareMixin):
    def process_request(self, request):
        from django.contrib.auth.forms import AuthenticationForm
        if request.method == 'POST' and 'login-modal' in request.POST:
            form = AuthenticationForm(data=request.POST, prefix="login")
            if form.is_valid():
                from django.contrib.auth import login
                login(request, form.get_user())
            request.method = 'GET'
        else:
            form = AuthenticationForm(request, prefix="login")
        request.login_form = form