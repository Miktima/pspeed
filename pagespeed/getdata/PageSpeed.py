import requests
import time


class PageSpeed:
    def __init__(self, portal):
    # Определяем параметры запросов
        self.apiKey = ""
        self.serviceUrl = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        self.portal = portal
        self.lE_metrics_desktop = {}
        self.olE_metrics_desktop = {}
        self.lE_metrics_mobile = {}
        self.olE_metrics_mobile = {}
        self.error = ""
        
    def get_result(self):
        # Получаем результат в соответствии с https://developers.google.com/speed/docs/insights/v5/get-started?hl=ru
        # Получаем метрики для desktop
        params = {
            'url': self.portal,
            'category': 'performance',
            'strategy': 'desktop'
            }
        response = requests.get(self.serviceUrl, params=params)
        rdict = response.json()
        if "loadingExperience" in rdict:
            self.lE_metrics_desktop = rdict["loadingExperience"]["metrics"]
            self.olE_metrics_desktop = rdict["originLoadingExperience"]["metrics"]
            # На всякий случай ждем 5 секунд пока нет ключа
            time.sleep(5)
            # Получаем метрики для mobile
            params = {
                'url': self.portal,
                'category': 'performance',
                'strategy': 'mobile'
                }
            response = requests.get(self.serviceUrl, params=params)
            rdict = response.json()
            if "loadingExperience" in rdict:
                self.lE_metrics_mobile = rdict["loadingExperience"]["metrics"]
                self.olE_metrics_mobile = rdict["originLoadingExperience"]["metrics"]
                return True
            else: 
                self.error = "Метрики для мобильных устройств отсутствуют"
                return False
        else:
            self.error = "Метрики для настольных браузеров отсутствуют"
            return False

