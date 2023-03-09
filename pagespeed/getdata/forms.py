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

    def clean_jsonfield (self, field:str, keymetrics:str):
        data = self.cleaned_data[field]
        # Проверяем, что данные - JSON
        try:
            data_dic = json.loads(data)
        except json.JSONDecodeError as e:
            raise ValidationError(_('JSONDecodeError: ' + e.msg)) 
        # Проверяем, что данные имеют соответствующие ключи
        if data_dic[keymetrics]["metrics"] == None:
            raise ValidationError(_(field + " has not [" + keymetrics + "][metrics] keys"))
        return data

    def clean_portalid (self, field:str):
        data = self.cleaned_data[field]
        # Устанавливаем значение в целое и проверяем, что есть такой портал
        data = int(data)
        portal_row = Sputnik.objects.filter(id=data)
        if portal_row.exists() == False:
            raise ValidationError(_("There are not portals with id: " + data))