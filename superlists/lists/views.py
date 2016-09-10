from django.shortcuts import render

from .models import Item


def home_page(request):
    if request.method == 'POST':
        item = Item()
        item.text = request.POST.get('item_text', '')
        item.save()
        return render(request,
                      'lists/home.html',
                      {
                          'new_item_text' : item.text,
                      })
    else:
        return render(request, 'lists/home.html')
