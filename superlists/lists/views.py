from django.shortcuts import redirect
from django.shortcuts import render

from .models import Item


def home_page(request):
    return render(request, 'lists/home.html',)


def view_list(request):
    items = Item.objects.all()
    return render(request,
                  'lists/list.html',
                  {
                      'items': items,
                  })


def new_list(request):
    item = Item()
    item.text = request.POST['item_text']
    item.save()
    return redirect('/lists/the-only-list-in-the-world/')
