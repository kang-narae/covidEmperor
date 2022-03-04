from django.db import models


class Vaccine(models.Model):
    location = models.CharField(max_length=30, primary_key=True)
    # vaccineCnt = models.IntegerField(default=0)
    month = models.IntegerField(default=0)
    month7 = models.IntegerField(default=0)
    month8 = models.IntegerField(default=0)
    month9 = models.IntegerField(default=0)
    month10 = models.IntegerField(default=0)
    
    def __str__(self):
        return self.location
    
class Patient(models.Model):
    
    date = models.CharField(null=False, default=0 ,max_length=100)
    year = models.CharField(null=False, default=0 ,max_length=10)
    month = models.CharField(null=False, default=0 ,max_length=10)
    gangnam = models.IntegerField(null=False, default=0)
    songpa = models.IntegerField(null=False, default=0)
    gangdong = models.IntegerField(null=False, default=0)
    sdm = models.IntegerField(null=False, default=0)
    yangcheon = models.IntegerField(null=False, default=0)
    seocho = models.IntegerField(null=False, default=0)
    junggu = models.IntegerField(null=False, default=0)
    seongdong = models.IntegerField(null=False, default=0)
    yongsan = models.IntegerField(null=False, default=0)
    guro = models.IntegerField(null=False, default=0)
    dongjak = models.IntegerField(null=False, default=0)
    gwangjin =models.IntegerField(null=False, default=0)
    ddm = models.IntegerField(null=False, default=0)
    ydpa = models.IntegerField(null=False, default=0)
    seongbuk = models.IntegerField(null=False, default=0)
    gangbuk = models.IntegerField(null=False, default=0)
    gangseo = models.IntegerField(null=False, default=0)
    geumcheon = models.IntegerField(null=False, default=0)
    gwanak = models.IntegerField(null=False, default=0)
    mapo = models.IntegerField(null=False, default=0)
    dobong = models.IntegerField(null=False, default=0)
    ep = models.IntegerField(null=False, default=0)
    jungnang = models.IntegerField(null=False, default=0)
    jongno = models.IntegerField(null=False, default=0)
    nowon = models.IntegerField(null=False, default=0)

    def __str__(self):
        return self.date
    
    
class Patient2(models.Model):
    
    ward = models.CharField(max_length=100,primary_key=True)
    month1 = models.IntegerField(default=0)
    month2 = models.IntegerField(default=0)
    month3 = models.IntegerField(default=0)
    month4 = models.IntegerField(default=0)
    month5 = models.IntegerField(default=0)
    month6 = models.IntegerField(default=0)
    month7 = models.IntegerField(default=0)
    month8 = models.IntegerField(default=0)
    month9 = models.IntegerField(default=0)
    month10 = models.IntegerField(default=0)
    month11 = models.IntegerField(default=0)
    month12 = models.IntegerField(default=0)
    
    def __str__(self):
        return self.ward    