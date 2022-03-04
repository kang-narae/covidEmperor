import csv
from django.http import JsonResponse
from django.shortcuts import render
import requests
import json
import xmltodict
from fin.models import dailycovid , dailyvaccine
import pandas as pd 
import cx_Oracle as ora
import matplotlib.pyplot as plt
import pandas as pd
import FinanceDataReader as fdr
from dateutil.parser import parse
import numpy as np


# Create your views here.

def connections():
    try:
        conn=ora.connect('system/1234@localhost:1521/orcl')
    except Exception as e:
        print('예외 발생')
    return conn

def chart(request):
    # covidData()
    # vaccineData()
    
    return render(request, 'chart.html')

# def plot(request):
#     covid = dailycovid.objects.all().values() # dict type
#     #print(datas)                         # <QuerySet [{'jikwon_no': 1, 'jikwon_name': '홍길동', ...
#     covid = pd.DataFrame(covid)
#     covid.columns = ['strdate', 'intdate','deathCnt', 'decideCnt']
#     covid= covid[::-1]
#     covid['datetype']= pd.to_datetime(covid['strdate'], format="%Y%m%d")
#     covid['decide1000']= covid['decideCnt']/1000
#     # 오늘 누적 확진자 - 어제 누적 확진자(diff())-> 하루 확진다, 값이 없을 경우 0으로 대체
#     covid['dailydecide']=covid['decideCnt'].diff().fillna(0)
#     # (다음행 - 현재행)÷현재행
#     covid['dailydiff']=covid['dailydecide'].pct_change().fillna(0)
#     # covid['dailydiff'] = covid['dailydiff']*100
#     jscovid = [covid['dailydecide'].to_json(orient = 'columns')]
#     context={'chart_data':jscovid}
#     return JsonResponse(context)

def plot(request):
    qs = dailycovid.objects.all().values().order_by('intdate')
    # print(qs)
    return render(request, 'plot.html')

def chart_data(request):
    covid = dailycovid.objects.all().values().order_by('intdate')
    covid = pd.DataFrame(covid)
    covid.columns = ['strdate', 'intdate','deathCnt', 'decideCnt']
    # print(covid)
    covid['dailydecide']=covid['decideCnt'].diff().fillna(0)
    intdate = covid['intdate'].values.tolist()
    dailydecide = covid['dailydecide'].values.tolist()
    # print(intdate)
    context = {'intdate':intdate,'dailydecide':dailydecide}
    return JsonResponse(context)



def code_data(request):
    code = request.GET.get('code')
    print(code)
    codedata = fdr.DataReader(code,'2020-01-01', '2022-01-19')
    codedata['percent']=codedata['Close']/codedata.iloc[0,1]*100
    codedata.reset_index(inplace=True)
    codeclose = codedata['percent'].values.tolist()
    codedate = codedata['Date'].values.tolist()
    print(codedata)
    context = {'codeclose':codeclose, 'codedate':codedate}
    return JsonResponse(context)

def covidData():

    #나래꺼 url 
    # m_servicekey= 'kPvWkLn8zX%2FrcSryaV88GKZw89YENVfrgvH06AuvYSrXsHOx6r705chjRSn%2F%2BjrdwYpeOPms5YcVRuYID5eWkA%3D%3D'
    # url='http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson?serviceKey={}&pageNo=1&numOfRows=10&startCreateDt=20200120&endCreateDt=20220119'.format(m_servicekey)
    # response =requests.get(url)

    #수찬꺼 url
    url='http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson?serviceKey=JvU2PSq9lh1mHsrlM5p7uq9GeNuR4KrBvrHcZO0jIb7unq5lANtM0HkaDA35GqYh3vhuWTXxlWrXqE8AZiqVSA%3D%3D&pageNo=1&numOfRows=1000&startCreateDt=20200120&endCreateDt=20220119'
    
    
    response= requests.get(url)
    contents=response.text    #받아온 텍스트는 xml 형식.
    dictionary = xmltodict.parse(contents)   # xml을 dic형식으로 만들고
    json_str= json.dumps(dictionary)   #dic을 json 형식으로 만들었는데 이러면 json str타입이 나옴.
    json_ob= json.loads(json_str)   # json str을 다시 json dict 객체로 만듦.
    covidData= json_ob['response']['body']['items']['item'] #해당 키 내의 벨류값 찾아옴


    filename='확진 및 사망자.csv'
    f= open(filename, 'w', encoding='utf-8-sig', newline='')
    writer= csv.writer(f)
    title= "date, intdate, deathCnt, decideCnt".split(',')
    writer.writerow(title)

    # print(json_ob)
    # print(covidData)
    # print(type(json_ob))
    # print(json_ob)
    # print(covidData)

    
    for i in covidData:
        # rowdata=[]
        date= i['stateDt']
        deathCnt= i['deathCnt']
        decideCnt= i['decideCnt']
        qs = dailycovid(strdate=date,intdate=int(date), deathCnt=int(deathCnt), decideCnt=int(decideCnt))
        qs.save()
        # rowdata.append(date)
        # rowdata.append(int(date))
        # rowdata.append(deathCnt)
        # rowdata.append(decideCnt)
        # writer.writerow(rowdata)
        
        


def vaccineData():
    service_key = 'JvU2PSq9lh1mHsrlM5p7uq9GeNuR4KrBvrHcZO0jIb7unq5lANtM0HkaDA35GqYh3vhuWTXxlWrXqE8AZiqVSA%3D%3D'
    # filename = '백신 접종.csv'
    # f= open(filename, 'w', encoding='utf-8-sig', newline = '')
    # writer = csv.writer(f)
    # title = "date,firstCnt,secondCnt,thirdCnt,totalFirstCnt,totalSecondCnt,totalThirdCnt".split(',')
    # writer.writerow(title) 
    vaccineData = [] # 전체 data 리스트(2중)
    for i in range(356):  #페이지 별로
        url = f'http://api.odcloud.kr/api/15077756/v1/vaccine-stat?page={i}&perPage=18&serviceKey={service_key}'
        res = requests.get(url)
        contents = res.json()
        data = [] # 날짜별로 data를 넣을 리스트
        for i in range(18):  #날짜 row 별로
            if contents['data'][i]['sido'] == '전국':
                data.append(contents['data'][i]['baseDate'][0:4]+contents['data'][i]['baseDate'][5:7]+contents['data'][i]['baseDate'][8:10])
                data.append(int(contents['data'][i]['baseDate'][0:4]+contents['data'][i]['baseDate'][5:7]+contents['data'][i]['baseDate'][8:10]))
                data.append(contents['data'][i]['firstCnt'])
                data.append(contents['data'][i]['secondCnt'])
                data.append(contents['data'][i]['thirdCnt'])
                data.append(contents['data'][i]['totalFirstCnt'])
                data.append(contents['data'][i]['totalSecondCnt'])
                data.append(contents['data'][i]['totalThirdCnt'])
        # writer.writerow(data)
        vaccineData.append(data)
        
    for i in vaccineData:  #날짜 row 별로
        date = i[0]
        intdate = i[1]
        firstCnt = i[2]
        secondCnt = i[3]
        thirdCnt = i[4]
        totalFirstCnt = i[5]
        totalSecondCnt = i[6]
        totalThirdCnt = i[7]
        qs = dailyvaccine(strdate = date, intdate = intdate, firstCnt = firstCnt, secondCnt = secondCnt, thirdCnt = thirdCnt\
            ,totalFirstCnt = totalFirstCnt,totalSecondCnt = totalSecondCnt,totalThirdCnt = totalThirdCnt )
        qs.save()
