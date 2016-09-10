from django.shortcuts import redirect
from django.shortcuts import render

from .models import Item


def home_page(request):
    if request.method == 'POST':
        text = request.POST.get('item_text', '')
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/the-only-list-in-the-world/')
    else:
        return render(request, 'lists/home.html',)


def view_list(request):
    items = Item.objects.all()
    return render(request,
                  'lists/list.html',
                  {
                      'items': items,
                  })
