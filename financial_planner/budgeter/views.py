from django.shortcuts import render

def home(request):
    return render(request, 'budgeter/home.html')

def about(request):
    return render(request, 'budgeter/about.html', {'title': 'About'})

def contact(request):
    return render(request, 'budgeter/contact.html', {'title': 'Contact'})
