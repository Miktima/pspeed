from django.db import models

class Sputnik (models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField()
    def __str__(self):
        return self.url	    

class Data (models.Model):
    site = models.ForeignKey(Sputnik, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    dataLEDesktop = models.JSONField()
    dataOLEDesktop = models.JSONField()
    dataLEMobile = models.JSONField()
    dataOLEMobile = models.JSONField()