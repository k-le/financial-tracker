from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm

def register(request):
    """Register-page for the User. Renders a basic Django registration
    form with Email for the User. Redirects the User to the login-page.
    """

    if request.method == 'POST':
        '''Once the submit button has been hit, a POST HTTP request
        is sent.
        '''

        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            '''If the form is valid, then we want to save the 
            information that was provided by the user so that 
            we ensure that the account is created.
            '''

            form.save()
            messages.success(request, 'Thanks for signing up! '
                                      'You should now be able to login.')

            return redirect('login-page')
    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form': form})
