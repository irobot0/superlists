from django.shortcuts import redirect
from django.shortcuts import render

from .models import Item
from .models import List


def home_page(request):
    return render(request, 'lists/home.html',)


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)
    return render(request,
                  'lists/list.html',
                  {
                      'items': items,
                  })


def new_list(request):
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/{0:d}/'.format(list_.id))
