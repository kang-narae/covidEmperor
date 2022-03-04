
from django.http import JsonResponse
from django.shortcuts import render
import requests
import json
import xmltodict
from fin.models import dailycovid, dailyvaccine
import pandas as pd
import cx_Oracle as ora

# Create your views here.


def plot(request):
    return render(request, 'plot.html')


def covidData():   #db에 데이터 저장
    # m_servicekey= 'kPvWkLn8zX%2FrcSryaV88GKZw89YENVfrgvH06AuvYSrXsHOx6r705chjRSn%2F%2BjrdwYpeOPms5YcVRuYID5eWkA%3D%3D'
    # url='http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson?serviceKey={}&pageNo=1&numOfRows=10&startCreateDt=20200120&endCreateDt=20220119'.format(m_servicekey)
    # response =requests.get(url)

    #수찬꺼
    url='http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson?serviceKey=JvU2PSq9lh1mHsrlM5p7uq9GeNuR4KrBvrHcZO0jIb7unq5lANtM0HkaDA35GqYh3vhuWTXxlWrXqE8AZiqVSA%3D%3D&pageNo=1&numOfRows=1000&startCreateDt=20200120&endCreateDt=20220119'
    
    
    response= requests.get(url)
    contents=response.text    #xml형식의 텍스트를
    dictionary = xmltodict.parse(contents)   # dic형식으로 만들고
    json_str= json.dumps(dictionary)   #이렇게 했는데 str타입이 나와?
    json_ob= json.loads(json_str)   #이렇게 해야 json dict 객체로 만들어서
    covidData= json_ob['response']['body']['items']['item'] #해당 키 내의 벨류값 찾아옴
    # print(json_ob)
    # print(covidData)
    # print(type(json_ob))

    # print(json_ob)
    # print(covidData)

    for i in covidData:
        date= i['stateDt']
        deathCnt= i['deathCnt']
        decideCnt= i['decideCnt']
        qs = dailycovid(strdate=date,intdate=int(date), deathCnt=int(deathCnt), decideCnt=int(decideCnt))
        qs.save()
        
        
        

def vaccineData(): #db에 데이터 저장하는 함수
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
        
        
        
