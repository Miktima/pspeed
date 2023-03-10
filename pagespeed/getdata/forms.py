from django import forms
import json
from .models import Sputnik

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class DataForm(forms.Form):
    le_metrics_desktop = forms.JSONField()
    ole_metrics_desktop = forms.JSONField()
    le_metrics_mobile = forms.JSONField()
    ole_metrics_mobile = forms.JSONField()
    portal = forms.IntegerField()

    def clean_le_metrics_desktop (self):
        data = self.cleaned_data["le_metrics_desktop"]
        # В данных надо изменить одинарные кавычки на двойные (наследие очищения данных, передающихся через форму)
        # Проверяем, что данные - JSON
        try:
            data_dic = json.loads(data.replace("\'", "\""))
        except json.JSONDecodeError as e:
            raise ValidationError(_('JSONDecodeError: ' + e.msg)) 
        # Проверяем, что данные имеют соответствующие ключи
        if data_dic.get("LARGEST_CONTENTFUL_PAINT_MS") == None:
            raise ValidationError(_("The field 'le_metrics_desktop' has not LARGEST_CONTENTFUL_PAINT_MS keys"))
        return data_dic

    def clean_ole_metrics_desktop (self):
        data = self.cleaned_data["ole_metrics_desktop"]
        # В данных надо изменить одинарные кавычки на двойные (наследие очищения данных, передающихся через форму)
        # Проверяем, что данные - JSON
        try:
            data_dic = json.loads(data.replace("\'", "\""))
        except json.JSONDecodeError as e:
            raise ValidationError(_('JSONDecodeError: ' + e.msg)) 
        # Проверяем, что данные имеют соответствующие ключи
        if data_dic.get("LARGEST_CONTENTFUL_PAINT_MS") == None:
            raise ValidationError(_("The field 'le_metrics_desktop' has not LARGEST_CONTENTFUL_PAINT_MS keys"))
        return data_dic

    def clean_le_metrics_mobile (self):
        data = self.cleaned_data["le_metrics_mobile"]
        # В данных надо изменить одинарные кавычки на двойные (наследие очищения данных, передающихся через форму)
        # Проверяем, что данные - JSON
        try:
            data_dic = json.loads(data.replace("\'", "\""))
        except json.JSONDecodeError as e:
            raise ValidationError(_('JSONDecodeError: ' + e.msg)) 
        # Проверяем, что данные имеют соответствующие ключи
        if data_dic.get("LARGEST_CONTENTFUL_PAINT_MS") == None:
            raise ValidationError(_("The field 'le_metrics_desktop' has not LARGEST_CONTENTFUL_PAINT_MS keys"))
        return data_dic

    def clean_ole_metrics_mobile (self):
        data = self.cleaned_data["ole_metrics_mobile"]
        # В данных надо изменить одинарные кавычки на двойные (наследие очищения данных, передающихся через форму)
        # Проверяем, что данные - JSON
        try:
            data_dic = json.loads(data.replace("\'", "\""))
        except json.JSONDecodeError as e:
            raise ValidationError(_('JSONDecodeError: ' + e.msg)) 
        # Проверяем, что данные имеют соответствующие ключи
        if data_dic.get("LARGEST_CONTENTFUL_PAINT_MS") == None:
            raise ValidationError(_("The field 'le_metrics_desktop' has not LARGEST_CONTENTFUL_PAINT_MS keys"))
        return data_dic

    def clean_portal (self):
        data = self.cleaned_data["portal"]
        # Устанавливаем значение в целое и проверяем, что есть такой портал
        data = int(data)
        portal_row = Sputnik.objects.filter(id=data)
        if portal_row.exists() == False:
            raise ValidationError(_("There are no portals with id: " + data))
        return data