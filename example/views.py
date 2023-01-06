from django.shortcuts import render

# Create your views here.


def hello_world(request):
    context = {'header': 'Hello, World!'}
    return render(request, 'menu.html', context=context)


def walk_menu(request, item=None):
    context = {'header': f'path:item = {item}'}
    return render(request, 'menu.html', context=context)
