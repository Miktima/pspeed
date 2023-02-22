import requests
import json

class PageSpeed:
    def __init__(self, portal):
    # Определяем параметры запросов
        self.apiKey = ""
        self.serviceUrl = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        self.portal = portal
        self.lE_metrics = {}
        self.olE_metrics = {}
        
    def get_result(self):
        # Получаем результат в соответствии с https://developers.google.com/speed/docs/insights/v5/get-started?hl=ru
        params = {
            'url': self.portal,
            'category': 'performance',
            'strategy': 'desktop'
            }
        response = requests.get(self.serviceUrl, params=params)
        rdict = response.json()
        self.lE_metrics = rdict["loadingExperience"]["metrics"]
        self.olE_metrics = rdict["originLoadingExperience"]["metrics"]
        return True

