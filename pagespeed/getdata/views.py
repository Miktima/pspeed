from django.shortcuts import render
from .models import Sputnik
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .PageSpeed import PageSpeed

def index(request):
    # Выбираем список порталов
    portal_list = Sputnik.objects.all()
    # Заполняем списки для выбора даты
    context = {
        'portal_list': portal_list,
    }
    return render(request, "getdata/index.html", context=context)

def results(request):
    portal_id = request.POST['portal']
    try:
        portal_obj = Sputnik.objects.get(id=portal_id)
    except Sputnik.DoesNotExist:
        # Если портал не выбран или не найден, повторяем вывод формы
        messages.error(request, 'Необходимо выбрать портал')
        return HttpResponseRedirect(reverse('index'))
    else:
        ps = PageSpeed(portal_obj.url)
        ps.get_result()
        context = {
            "lE_metrics": ps.lE_metrics,
            "olE_metrics": ps.olE_metrics,
        }
        return render(request, 'getdata/results.html', context)    
    return render(request)
