from django.shortcuts import render

# Create your views here.


def hello_world(request):
    return render(request, 'index.html')


def walk_menu(request, item):
    context = {'header': item}
    return render(request, 'menu.html', context=context)
