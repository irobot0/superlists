from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.shortcuts import render

from .models import Item
from .models import List


def home_page(request):
    return render(request, 'lists/home.html',)


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)

    if request.method == 'POST':
        try:
            item = Item(text=request.POST['item_text'], list=list_)
            item.full_clean()
            item.save()
            return redirect('/lists/{0:d}/'.format(list_.id))
        except ValidationError:
            error = "You can't have an empty list item"
            return render(request, 'lists/list.html', {'list': list_, 'error': error})
    else:
        return render(request, 'lists/list.html', {'list': list_, 'error': None})


def new_list(request):
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST.get('item_text', ''), list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, 'lists/home.html', {'error': error})
    else:
        return redirect('/lists/{0:d}/'.format(list_.id))
