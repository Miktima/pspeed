from django.shortcuts import render
from .models import Sputnik, Data
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .PageSpeed import PageSpeed

from io import BytesIO
import base64

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import matplotlib.dates as mdates

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
        # Вызываем утилиту PageSpeed
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

def saved_results(request, portal_id):
    data = Data.objects.filter(sputnik__id=portal_id)
    portal = Sputnik.objects.get(id=portal_id)
    timestamps = data.values_list('time', flat=True)
    # Заполняем листы значениями (пока только тремя из шести)
    data_le_desktop_FCP = []
    data_le_desktop_FID = []
    data_le_desktop_LCP = []
    for d in data.values_list('dataLEDesktop', flat=True):
        data_le_desktop_FCP.append(d["FIRST_CONTENTFUL_PAINT_MS"]["percentile"])
        data_le_desktop_FID.append(d["FIRST_INPUT_DELAY_MS"]["percentile"])
        data_le_desktop_LCP.append(d["LARGEST_CONTENTFUL_PAINT_MS"]["percentile"])
    data_ole_desktop_FCP = []
    data_ole_desktop_FID = []
    data_ole_desktop_LCP = []
    for d in data.values_list('dataLEDesktop', flat=True):
        data_ole_desktop_FCP.append(d["FIRST_CONTENTFUL_PAINT_MS"]["percentile"])
        data_ole_desktop_FID.append(d["FIRST_INPUT_DELAY_MS"]["percentile"])
        data_ole_desktop_LCP.append(d["LARGEST_CONTENTFUL_PAINT_MS"]["percentile"])
    data_le_mobile_FCP = []
    data_le_mobile_FID = []
    data_le_mobile_LCP = []
    for d in data.values_list('dataLEMobile', flat=True):
        data_le_mobile_FCP.append(d["FIRST_CONTENTFUL_PAINT_MS"]["percentile"])
        data_le_mobile_FID.append(d["FIRST_INPUT_DELAY_MS"]["percentile"])
        data_le_mobile_LCP.append(d["LARGEST_CONTENTFUL_PAINT_MS"]["percentile"])
    data_ole_mobile_FCP = []
    data_ole_mobile_FID = []
    data_ole_mobile_LCP = []
    for d in data.values_list('dataLEMobile', flat=True):
        data_ole_mobile_FCP.append(d["FIRST_CONTENTFUL_PAINT_MS"]["percentile"])
        data_ole_mobile_FID.append(d["FIRST_INPUT_DELAY_MS"]["percentile"])
        data_ole_mobile_LCP.append(d["LARGEST_CONTENTFUL_PAINT_MS"]["percentile"])
    # Определение тиков для оси ординат (дат)
    locator = mdates.AutoDateLocator(minticks=5, maxticks=9)
    formatter = mdates.ConciseDateFormatter(locator)
    # График FIRST_CONTENTFUL_PAINT_MS
    fig, ax = plt.subplots(figsize=(7, 7), layout='constrained')
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    ax.plot(timestamps, data_le_desktop_FCP, label="Desktop - конечные пользователи")
    ax.plot(timestamps, data_ole_desktop_FCP, label="Desktop - источник")
    ax.plot(timestamps, data_le_mobile_FCP, label="Mobile - конечные пользователи")
    ax.plot(timestamps, data_ole_mobile_FCP, label="Mobile - источник")
    ax.set_title("FIRST_CONTENTFUL_PAINT_MS")
    ax.set_ylabel("мс") 
    ax.legend()
    imgFCP_in_memory = BytesIO()
    plt.savefig(imgFCP_in_memory, format="png")
    FCPimage = base64.b64encode(imgFCP_in_memory.getvalue()).decode()
    plt.clf()
    # График FIRST_INPUT_DELAY_MS
    fig, ax = plt.subplots(figsize=(7, 7), layout='constrained')
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    ax.plot(timestamps, data_le_desktop_FID, label="Desktop - конечные пользователи")
    ax.plot(timestamps, data_ole_desktop_FID, label="Desktop - источник")
    ax.plot(timestamps, data_le_mobile_FID, label="Mobile - конечные пользователи")
    ax.plot(timestamps, data_ole_mobile_FID, label="Mobile - источник")
    ax.set_title("FIRST_INPUT_DELAY_MS")
    ax.set_ylabel("мс") 
    ax.legend()
    imgFID_in_memory = BytesIO()
    plt.savefig(imgFID_in_memory, format="png")
    FIDimage = base64.b64encode(imgFID_in_memory.getvalue()).decode()
    plt.clf()
    # График LARGEST_CONTENTFUL_PAINT_MS
    fig, ax = plt.subplots(figsize=(7, 7), layout='constrained')
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    ax.plot(timestamps, data_le_desktop_LCP, label="Desktop - конечные пользователи")
    ax.plot(timestamps, data_ole_desktop_LCP, label="Desktop - источник")
    ax.plot(timestamps, data_le_mobile_LCP, label="Mobile - конечные пользователи")
    ax.plot(timestamps, data_ole_mobile_LCP, label="Mobile - источник")
    ax.set_title("LARGEST_CONTENTFUL_PAINT_MS")
    ax.set_ylabel("мс") 
    ax.legend()
    imgLCP_in_memory = BytesIO()
    plt.savefig(imgLCP_in_memory, format="png")
    LCPimage = base64.b64encode(imgLCP_in_memory.getvalue()).decode()
    plt.clf()
    context = {
        "FCPimage": FCPimage,
        "FIDimage": FIDimage,
        "LCPimage": LCPimage,
        "portal": portal
    }
    return render(request, 'getdata/saved_results.html', context)

def save_data(request):
    if request.method == 'POST':
        portal_id = request.POST["portal"]
        portal_row = Sputnik.objects.get(id=portal_id)
        data = Data(
            dataLEDesktop=request.POST["le_metrics_desktop"],
            dataOLEDesktop=request.POST["ole_metrics_desktop"],
            dataLEMobile=request.POST["le_metrics_mobile"],
            dataOLEMobile=request.POST["ole_metrics_mobile"],
            site=portal_row
        )
        data.save()
        return render(request, 'getdata/results.html')