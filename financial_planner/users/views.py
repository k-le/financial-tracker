from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm

def register(request):
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
            username = form.cleaned_data.get('username')
            messages.success(request, 'Thanks for signing up! '
                                      'You should receive a verification email within the next 30 minutes.')

            return redirect('budgeter-home')
    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form': form})
