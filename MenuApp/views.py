from django.shortcuts import render

def menu_view(request, *args, **kwargs):
    return render(request, 'MenuApp/test1.html')
