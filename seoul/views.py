from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime
from django.shortcuts import render,redirect
from urllib.request import Request,urlopen
from urllib.parse import urlencode,unquote,quote_plus
import json
import matplotlib
import xmltodict
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import font_manager, rc
import requests
from seoul.models import Vaccine,Patient,Patient2
matplotlib.rcParams["font.family"] = "malgun Gothic"
matplotlib.rcParams["axes.unicode_minus"] = False
import cx_Oracle as ora  #오라클 연동

# Create your views here.
def connections():
    try:
        conn=ora.connect('ora_user/1234@localhost:1521/orcl')
    except Exception as e:
        print('예외 발생')
    return conn

def chart(request):
    conn=ora.connect('ora_user/1234@localhost:1521/orcl')
    vaccineData()
    qs = Vaccine.objects.all()

    obeject_df3 = pd.DataFrame.from_records(qs.values())
    print("object.all() : ",obeject_df3)
    context = {'chart':qs}
    print(context)
    chartshow()
    return render(request,'sview.html',context)

def vaccineData():
    ServiceKey = 'XlIxr1CyGCs5BSRNmrg%2Bzz7qcLN02uchkN%2B98y2XKl5HeokzvNW3%2BbdKU3DQ%2FWs6ybm8bQm3CWeFSi3O6JyX5g%3D%3D'
    url = 'https://api.odcloud.kr/api/15094083/v1/uddi:c56fbd05-7fc0-42de-86f6-d9334784049a?page=1&perPage=30&serviceKey={}'.format(ServiceKey)
    response = requests.get(url)
    # response의 내용을 text변환
    contents = response.text
    #json->dataframe
    df = pd.DataFrame.from_dict(json.loads(contents)['data'])
   
    rows = []
    for x in df.values:
        row = [str(x[-1]),int(x[3]),int(x[5]),int(x[7]),int(x[9]),int(x[0])]
        rows.append(row)
        location = row[0]
        month = row[1]
        month7 = row[2]
        month8 = row[3]
        month9 = row[4]
        month10 = row[5]
        qs = Vaccine(location=location, month=month, month7=month7, month8=month8,month9=month9,month10=month10)
        qs.save()

def chartshow():
    qs = Vaccine.objects.all()
    vData = pd.DataFrame.from_records(qs.values())
    #그래프 격자가 위치할 기본 틀을 만들기
    fig = plt.figure()
    #그래프 격자 만들기 
    ax1 = fig.add_subplot(111)   #1행1열의1번째 그래프
    # ax2 = ax1.twinx()    #y축을 두 개 만들거라서
    # p1, = ax1.plot(df['자치구'],df['2-6월 1차접종자'],'b', label='접종자')
    p1, = ax1.plot(vData.columns[1:],vData.iloc[0][1:],'b', label=vData.iloc[0][0])
    p2, = ax1.plot(vData.columns[1:],vData.iloc[1][1:],'r', label=vData.iloc[1][0])
    
    # for i in range(25):
        # p1, = ax1.plot(vData.columns[1:],vData.iloc[i][1:],'b', label=vData.iloc[i][0])
    ax1.legend([p1,p2],[p1.get_label(),p2.get_label()])
    # print(df.iloc[0].values) #관악구 value만 뽑음

    ax1.set_title('서울 자치구별 백신 접종 현황')
    ax1.set_xlabel('기준일')
    ax1.set_ylabel('접종자수')
    
    #
    ax1.tick_params(axis='x', labelrotation=90) #x축 label 90도 표
    ax1.grid(axis='y')
    fig.tight_layout(pad=1)

    plt.show()



#승채님 view

def patient(request):
    
    serial_key= "6453454b53746d6438337244774474"
    url= "http://openapi.seoul.go.kr:8088/{}/json/TbCorona19CountStatusJCG/1/800/".format(serial_key)
    response = requests.get(url)
    contents = response.text
    json_ob = json.loads(contents)
    publicData = json_ob["TbCorona19CountStatusJCG"]["row"]
    df = pd.json_normalize(publicData)


    df['DATETIME'] = pd.to_datetime(df['JCG_DT'])
    # df.set_index = df.index[1]
    df['YEAR'] =df['DATETIME'].dt.year
    df["MONTH"] = df["DATETIME"].dt.month
    df['DATETIME'] =df['DATETIME'].dt.date
    mask = df["YEAR"].isin([2022,2021,2020])
    df = df[mask]
    df = df[:-3] 

    # df = df.apply(pd.to_numeric , errors="coerce")
    df = df[::-1] 



    df = df[["DATETIME","YEAR","MONTH","GANGNAMADD","SONGPAADD","GANGDONGADD","SDMADD","YANGCHEONADD"
                ,"SEOCHOADD","JUNGGUADD","SEONGDONGADD","YONGSANADD","GUROADD","DONGJAKADD"
                ,"GWANGJINADD","DDMADD","YDPADD","SEONGBUKADD","GANGBUKADD","GANGSEOADD","GEUMCHEONADD"
                ,"GWANAKADD","MAPOADD","DOBONGADD","EPADD","JUNGNANGADD","JONGNOADD"
                ,"NOWONADD"
                    ]]
    df =df.rename(columns={
                            "DATETIME":"기준일"
                        ,"YEAR" :" 기준연도"
                        , "MONTH" :"기준월"
                        ,"JONGNOADD":"종로구"
                        ,"JUNGGUADD":"중구"
                        ,"YONGSANADD":"용산구"
                        ,"SEONGDONGADD":"성동구"
                        ,"GWANGJINADD":"광진구"
                        ,"DDMADD":"동대문"
                        ,"JUNGNANGADD":"중랑구"
                        ,"SEONGBUKADD":"성북구"
                        ,"GANGBUKADD":"강북구"
                        ,"DOBONGADD":"도봉구"
                            ,"NOWONADD":"노원구"
                            ,"EPADD":"은평구"
                            ,"SDMADD":"서대문"
                            ,"MAPOADD":"마포구"
                            ,"YANGCHEONADD":"양천구"
                            ,"GANGSEOADD":"강서구"
                            ,"GUROADD":"구로구"
                            ,"GEUMCHEONADD":"금천구"
                            ,"YDPADD":"영등포"
                            ,"DONGJAKADD":"동작구"
                            ,"GWANAKADD":"관악구"
                            ,"SEOCHOADD":"서초구"
                            ,"GANGNAMADD":"강남구"
                            ,"SONGPAADD":"송파구"
                            ,"GANGDONGADD":"강동구"
                    }
                )

    rows=[]
    for x in df.to_records(index=False):
        row=[  x[0],int(x[1] ),int(x[2] ),int(x[3] ),int(x[4] ),int(x[5] ),int(x[6] ),int(x[7] ),int(x[8] ),int(x[9] )
            ,int(x[10] ),int(x[11] ),int(x[12] ),int(x[13] ),int(x[14] ),int(x[15] ),int(x[16] ),int(x[17] ),int(x[18] ),int(x[19] )
            ,int(x[20] ),int(x[21] ),int(x[22] ),int(x[23] ),int(x[24] ),int(x[25]),int(x[26]) ,int(x[27])]
        # 전체 list에 담음.
        rows.append(row)

        date = row[0]
        year = row[1]
        month = row[2]
        gangnam = row[3]
        songpa = row[4]
        gangdong = row[5]
        sdm = row[6]
        yangcheon =row[7] 
        seocho = row[8]
        junggu =row[9]
        seongdong =row[10]
        yongsan = row[11]
        guro = row[12]
        dongjak = row[13]
        gwangjin = row[14]
        ddm = row[15]
        ydpa = row[16]
        seongbuk = row[17]
        gangbuk = row[18]
        gangseo = row[19]
        geumcheon = row[20]
        gwanak = x[21]
        mapo = row[22]
        dobong = row[23]
        ep = row[24]
        jungnang = row[25] 
        jongno = row[26]
        nowon =row[27]
        
        qs = Patient(date=date , year= year, month= month,
                   gangnam=gangnam, songpa= songpa , gangdong= gangdong ,sdm=sdm
                ,yangcheon=yangcheon , seocho=seocho , junggu=junggu , seongdong= seongdong,
                yongsan= yongsan , guro= guro , dongjak= dongjak, gwangjin= gwangjin , ddm= ddm
                , ydpa=ydpa, seongbuk=seongbuk, gangbuk=gangbuk, gangseo= gangseo, geumcheon=geumcheon
                ,gwanak=gwanak, mapo=mapo, dobong=dobong, ep=ep, jungnang=jungnang, jongno=jongno,
                nowon=nowon)
        
        qs.save()

    return render(request,"sview.html")

def patient2(request):
        

    serial_key= "6453454b53746d6438337244774474"
    url= "http://openapi.seoul.go.kr:8088/{}/json/TbCorona19CountStatusJCG/1/800/".format(serial_key)
    response = requests.get(url)
    contents = response.text
    json_ob = json.loads(contents)
    publicData = json_ob["TbCorona19CountStatusJCG"]["row"]
    df = pd.json_normalize(publicData)


    df['DATETIME'] = pd.to_datetime(df['JCG_DT'])
    # df.set_index = df.index[1]
    df['YEAR'] =df['DATETIME'].dt.year
    df["MONTH"] = df["DATETIME"].dt.month
    df['DATETIME'] =df['DATETIME'].dt.date
    mask = df["YEAR"].isin([2022,2021,2020])
    df = df[mask]
    df = df[:-3] 
    df = df[::-1] 

    df = df[["YEAR", "MONTH" 
                        ,"JONGNOADD"
                        ,"JUNGGUADD"
                        ,"YONGSANADD"
                        ,"SEONGDONGADD"
                        ,"GWANGJINADD"
                        ,"DDMADD"
                        ,"JUNGNANGADD"
                        ,"SEONGBUKADD"
                        ,"GANGBUKADD"
                        ,"DOBONGADD"
                        ,"NOWONADD"
                        ,"EPADD"
                        ,"SDMADD"
                        ,"MAPOADD"
                        ,"YANGCHEONADD"
                        ,"GANGSEOADD"
                        ,"GUROADD"
                        ,"GEUMCHEONADD"
                        ,"YDPADD"
                        ,"DONGJAKADD"
                        ,"GWANAKADD"
                        ,"SEOCHOADD"
                        ,"GANGNAMADD"
                        ,"SONGPAADD"
                        ,"GANGDONGADD"
                ]]
    df = df.apply(pd.to_numeric , errors="coerce")
    df = df.groupby(["YEAR","MONTH"]).sum()
    df =df.rename(columns={
                        "YEAR" : " 기준연도"
                        , "MONTH" :"기준월"
                        ,"JONGNOADD":"종로구"
                        ,"JUNGGUADD":"중구"
                        ,"YONGSANADD":"용산구"
                        ,"SEONGDONGADD":"성동구"
                        ,"GWANGJINADD":"광진구"
                        ,"DDMADD":"동대문"
                        ,"JUNGNANGADD":"중랑구"
                        ,"SEONGBUKADD":"성북구"
                        ,"GANGBUKADD":"강북구"
                        ,"DOBONGADD":"도봉구"
                        ,"NOWONADD":"노원구"
                        ,"EPADD":"은평구"
                        ,"SDMADD":"서대문"
                        ,"MAPOADD":"마포구"
                        ,"YANGCHEONADD":"양천구"
                        ,"GANGSEOADD":"강서구"
                        ,"GUROADD":"구로구"
                        ,"GEUMCHEONADD":"금천구"
                        ,"YDPADD":"영등포"
                        ,"DONGJAKADD":"동작구"
                        ,"GWANAKADD":"관악구"
                        ,"SEOCHOADD":"서초구"
                        ,"GANGNAMADD":"강남구"
                        ,"SONGPAADD":"송파구"
                        ,"GANGDONGADD":"강동구"
                
                
                }
            )

    df = df.iloc[11:23]
    df = df.transpose()
        
    df["자치구"] = ["종로구","중구","용산구","성동구","광진구","동대문","중랑구","성북구","강북구","도봉구",
                "노원구","은평구","서대문","마포구","양천구","강서구","구로구","금천구","영등포","동작구","관악구",
                "서초구","강남구","송파구","강동구"]
    rows=[]
    for x in df.to_records(index=False):
        row=[  str(x[-1]),int(x[0]),int(x[1] ),int(x[2] ),int(x[3] ),int(x[4] ),int(x[5] ),int(x[6] ),int(x[7] ),int(x[8] ),int(x[9] )
        ,int(x[10] ),int(x[11] )]
            # 전체 list에 담음.
            
        rows.append(row)
    
        ward = row[0]
        month1 = row[1]
        month2 = row[2]
        month3 = row[3]
        month4 = row[4]
        month5 = row[5]
        month6 = row[6]
        month7 = row[7]
        month8 = row[8]
        month9 = row[9]
        month10 = row[10]
        month11 = row[11]
        month12 = row[12]

        qs = Patient2(
        ward = ward , month1= month1 ,
        month2= month2 , month3= month3,
        month4= month4 , month5= month5,
        month6= month6 , month7= month7,
        month8= month8 , month9= month9,
        month10= month10 , month11= month11,
        month12= month12 )
        qs.save()

    return render(request,"sview.html")
