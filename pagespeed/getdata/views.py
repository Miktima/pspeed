from django.shortcuts import render
from .models import Sputnik, Data
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
        res = ps.get_result()
        if res == False:
            messages.error(request, ps.error)
            return HttpResponseRedirect(reverse('index'))
        saved_data = Data.objects.filter(site=portal_obj).count()
        context = {
            "lE_metrics_desktop": ps.lE_metrics_desktop,
            "olE_metrics_desktop": ps.olE_metrics_desktop,
            "lE_metrics_mobile": ps.lE_metrics_mobile,
            "olE_metrics_mobile": ps.olE_metrics_mobile,
            "portal": portal_obj,
            "saved_data": saved_data
        }
        return render(request, 'getdata/results.html', context)    
