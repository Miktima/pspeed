from django.shortcuts import render
from .models import Sputnik, Data
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db.models import Count
from .PageSpeed import PageSpeed
from .forms import DataForm
import json
import re

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
    # Заполняем списки для выбора порталов
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
        md = ps.lE_metrics_desktop
        mm = ps.lE_metrics_mobile
        # Удаляем три не очень важные(?) метрики из настольной и мобильной метрик (при их наличии)
        if md.get("CUMULATIVE_LAYOUT_SHIFT_SCORE") != None:
            md.pop("CUMULATIVE_LAYOUT_SHIFT_SCORE")
        if md.get("EXPERIMENTAL_INTERACTION_TO_NEXT_PAINT") != None:
            md.pop("EXPERIMENTAL_INTERACTION_TO_NEXT_PAINT")
        if md.get("INTERACTION_TO_NEXT_PAINT") != None:
            md.pop("INTERACTION_TO_NEXT_PAINT")
        if md.get("EXPERIMENTAL_TIME_TO_FIRST_BYTE") != None:
            md.pop("EXPERIMENTAL_TIME_TO_FIRST_BYTE")
        if mm.get("CUMULATIVE_LAYOUT_SHIFT_SCORE") != None:
            mm.pop("CUMULATIVE_LAYOUT_SHIFT_SCORE")
        if mm.get("EXPERIMENTAL_INTERACTION_TO_NEXT_PAINT") != None:
            mm.pop("EXPERIMENTAL_INTERACTION_TO_NEXT_PAINT")
        if mm.get("INTERACTION_TO_NEXT_PAINT") != None:
            mm.pop("INTERACTION_TO_NEXT_PAINT")
        if mm.get("EXPERIMENTAL_TIME_TO_FIRST_BYTE") != None:
            mm.pop("EXPERIMENTAL_TIME_TO_FIRST_BYTE")
        context = {
            "lE_metrics_desktop": ps.lE_metrics_desktop,
            "olE_metrics_desktop": ps.olE_metrics_desktop,
            "lE_metrics_mobile": ps.lE_metrics_mobile,
            "olE_metrics_mobile": ps.olE_metrics_mobile,
            "metricsDesktop": md,
            "metricsMobile": mm,
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
    data_le_mobile_FCP = []
    data_le_mobile_FID = []
    data_le_mobile_LCP = []
    for d in data.values_list('dataLEMobile', flat=True):
        data_le_mobile_FCP.append(d["FIRST_CONTENTFUL_PAINT_MS"]["percentile"])
        data_le_mobile_FID.append(d["FIRST_INPUT_DELAY_MS"]["percentile"])
        data_le_mobile_LCP.append(d["LARGEST_CONTENTFUL_PAINT_MS"]["percentile"])
    # Определение тиков для оси ординат (дат)
    locator = mdates.AutoDateLocator(minticks=5, maxticks=9)
    formatter = mdates.ConciseDateFormatter(locator)
    # График FIRST_CONTENTFUL_PAINT_MS
    fig, ax = plt.subplots(figsize=(7, 7), layout='constrained')
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    ax.plot(timestamps, data_le_desktop_FCP, label="Desktop")
    ax.plot(timestamps, data_le_mobile_FCP, label="Mobile")
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
    ax.plot(timestamps, data_le_desktop_FID, label="Desktop")
    ax.plot(timestamps, data_le_mobile_FID, label="Mobile")
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
    ax.plot(timestamps, data_le_desktop_LCP, label="Desktop")
    ax.plot(timestamps, data_le_mobile_LCP, label="Mobile")
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
        "portal": portal,
    }
    return render(request, 'getdata/saved_results.html', context)

def save_data(request):
    form = DataForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            portal_id = form.cleaned_data["portal"]
            portal_row = Sputnik.objects.get(id=portal_id)
            # print(form.cleaned_data["le_metrics_desktop"])
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

def collect_results(request):
    # Выбираем список порталов
    portal_list = Sputnik.objects.all()
    # Заполняем списки для выбора даты
    context = {
        'portal_list': portal_list
    }
    return render(request, "getdata/collect_results.html", context=context)    

def auto_results(request):
    portal_id = request.POST['portal']
    if int(portal_id) == 1:
        portal_id = 30
    if int(portal_id) == -1:
        portal_obj = Sputnik.objects.order_by('pk').first()
        next_id = portal_obj.pk
        response = {
            'status': "initial",
            'next': next_id
            }
        return JsonResponse(response)
    elif int(portal_id) > 0:
        portal_obj = Sputnik.objects.get(pk=portal_id)
        is_elements = Sputnik.objects.order_by('pk').filter(pk__gt = portal_id).count()
        if is_elements == 0:
            next_id = -2
        else:
            portal_obj_next = Sputnik.objects.order_by('pk').filter(pk__gt = portal_id).first()
            next_id = portal_obj_next.pk
    # Вызываем утилиту PageSpeed
    ps = PageSpeed(portal_obj.url)
    res = ps.get_result()
    # Если результат отрицательный, то возвращаем соответствующий статус
    if res == False:
        response = {
            'status': "false",
            'next': next_id
            }
        return JsonResponse(response)
    md = ps.lE_metrics_desktop
    mm = ps.lE_metrics_mobile
    # Проверяем, что все "важные" данные есть
    if md.get("FIRST_CONTENTFUL_PAINT_MS") == None or\
        md.get("FIRST_INPUT_DELAY_MS") == None or\
        md.get("LARGEST_CONTENTFUL_PAINT_MS") == None or\
        mm.get("FIRST_CONTENTFUL_PAINT_MS") == None or\
        mm.get("FIRST_INPUT_DELAY_MS") == None or\
        mm.get("LARGEST_CONTENTFUL_PAINT_MS") == None:
            response = {
                "lE_metrics_desktop": json.dumps(ps.lE_metrics_desktop),
                "olE_metrics_desktop": json.dumps(ps.olE_metrics_desktop),
                "lE_metrics_mobile": json.dumps(ps.lE_metrics_mobile),
                "olE_metrics_mobile": json.dumps(ps.olE_metrics_mobile),
                "portal": portal_id,
                "status": "false",
                'next': next_id
            }
    else:
            response = {
                "le_metrics_desktop": json.dumps(ps.lE_metrics_desktop),
                "ole_metrics_desktop": json.dumps(ps.olE_metrics_desktop),
                "le_metrics_mobile": json.dumps(ps.lE_metrics_mobile),
                "ole_metrics_mobile": json.dumps(ps.olE_metrics_mobile),
                "portal": portal_id,
                "status": "true",
                'next': next_id
            }
    return JsonResponse(response)

def save_collected_data(request):
    portals_str = request.POST['portals']
    portals_list = portals_str.split()
    for p in portals_list:
        portal_row = Sputnik.objects.get(id=int(p))
        print ("URL: ", portal_row.url)
        print (request.POST['le_metrics_desktop' + p])
        h = re.sub("\"", "", request.POST['le_metrics_desktop' + p])
        h = re.sub("'", "\"", h)
        # hhh = json.loads(request.POST['le_metrics_desktop' + p])
        hhh = json.loads(h)
        for key, value in hhh.items():
            print ("le_metrics_desktop: key:", key, "   value:", value)
        # data = Data(
        #     dataLEDesktop = json.loads(request.POST['le_metrics_desktop' + p]),
        #     dataOLEDesktop = json.loads(request.POST['ole_metrics_desktop' + p]),
        #     dataLEMobile = json.loads(request.POST['le_metrics_mobile' + p]),
        #     dataOLEMobile = json.loads(request.POST['ole_metrics_mobile' + p]),
        #     site=portal_row
        # )
        # data.save()
    response = {
        "save_status": "true"
    }
    return JsonResponse(response)
