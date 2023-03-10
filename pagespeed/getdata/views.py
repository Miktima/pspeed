from django.shortcuts import render
from .models import Sputnik, Data
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Count
from .PageSpeed import PageSpeed
from .forms import DataForm
import json

from io import BytesIO
import base64

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import matplotlib.dates as mdates

def index(request):
    # Выбираем список порталов
    portal_list = Sputnik.objects.all()
    p = len(Data.objects.all().annotate(Count('site_id', distinct=True)))
    # Заполняем списки для выбора даты
    context = {
        'portal_list': portal_list,
        'num_saved_portals': p,
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
    data = Data.objects.filter(site_id=portal_id)
    portal = Sputnik.objects.get(id=portal_id)
    timestamps = data.values_list('time', flat=True)
    # Заполняем листы значениями (пока только тремя из шести)
    data_le_desktop_FCP = []
    data_le_desktop_FID = []
    data_le_desktop_LCP = []                                                     
    for d in data.values_list("dataLEDesktop", flat=True):
        data_le_desktop_FCP.append(d["FIRST_CONTENTFUL_PAINT_MS"]["percentile"])
        data_le_desktop_FID.append(d["FIRST_INPUT_DELAY_MS"]["percentile"])
        data_le_desktop_LCP.append(d["LARGEST_CONTENTFUL_PAINT_MS"]["percentile"])
    data_ole_desktop_FCP = []
    data_ole_desktop_FID = []
    data_ole_desktop_LCP = []
    for d in data.values_list('dataOLEDesktop', flat=True):
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
    for d in data.values_list('dataOLEMobile', flat=True):
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
    form = DataForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            portal_id = form.cleaned_data["portal"]
            portal_row = Sputnik.objects.get(id=portal_id)
            print(form.cleaned_data["le_metrics_desktop"])
            data = Data(
                dataLEDesktop=form.cleaned_data["le_metrics_desktop"],
                dataOLEDesktop=form.cleaned_data["ole_metrics_desktop"],
                dataLEMobile=form.cleaned_data["le_metrics_mobile"],
                dataOLEMobile=form.cleaned_data["ole_metrics_mobile"],
                site=portal_row
            )
            data.save()
            return render(request, 'getdata/results.html')
        else:
            return render(request, 'getdata/results.html')
    
def sputnik_results(request):
    LCP_desktop = []
    LCP_mobile = []
    sputnik = []
    # Заполняем списки для каждого портала. Берем последнее измерение
    portal = Sputnik.objects.values("id", "url")
    for value in portal:
        data = Data.objects.filter(site_id=value.get("id")).order_by('-time').first()
        if data != None:
            sputnik_name = (value.get("url")).replace("https://", "")
            sputnik_name = sputnik_name.replace("/", "")
            sputnik.append(sputnik_name)
            LCP_desktop.append(data.dataLEDesktop["LARGEST_CONTENTFUL_PAINT_MS"]["percentile"])
            LCP_mobile.append(data.dataLEMobile["LARGEST_CONTENTFUL_PAINT_MS"]["percentile"])
    # График LARGEST_CONTENTFUL_PAINT_MS для Desktop
    fig, ax = plt.subplots(figsize=(7, 7), layout='constrained')
    ax.scatter(sputnik, LCP_desktop, facecolor='r', edgecolor='k')
    ax.set_title("LARGEST_CONTENTFUL_PAINT_MS для Desktop")
    ax.set_ylabel("мс")
    ax.hlines(2500, 0, len(sputnik), colors="g")
    ax.grid(True) 
    for label in ax.get_xticklabels():
        label.set(rotation=90, horizontalalignment='center')
    imgLCP_desktop_in_memory = BytesIO()
    plt.savefig(imgLCP_desktop_in_memory, format="png")
    LCP_desktop_image = base64.b64encode(imgLCP_desktop_in_memory.getvalue()).decode()
    plt.clf()
    # График LARGEST_CONTENTFUL_PAINT_MS для Mobile
    fig, ax = plt.subplots(figsize=(7, 7), layout='constrained')
    ax.scatter(sputnik, LCP_mobile, facecolor='r', edgecolor='k')
    ax.set_title("LARGEST_CONTENTFUL_PAINT_MS для Mobile")
    ax.set_ylabel("мс")
    ax.hlines(2500, 0, len(sputnik), colors="g")
    ax.grid(True) 
    for label in ax.get_xticklabels():
        label.set(rotation=90, horizontalalignment='center')
    imgLCP_mobile_in_memory = BytesIO()
    plt.savefig(imgLCP_mobile_in_memory, format="png")
    LCP_mobile_image = base64.b64encode(imgLCP_mobile_in_memory.getvalue()).decode()
    plt.clf()
    context = {
        "LCP_desktop_image": LCP_desktop_image,
        "LCP_mobile_image": LCP_mobile_image,
    }
    return render(request, 'getdata/sputnik_results.html', context)

