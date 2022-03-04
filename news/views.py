from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.core.paginator import Paginator
from news.models import News, Comment
from django.db.models import Max,Min,Avg 

def nlist(request):
    qs = News.objects.all().order_by('-n_no')
    paginator=Paginator(qs,5)
    nowpage=int(request.GET.get('nowpage',1))
    nlist=paginator.get_page(nowpage)
    context = {'nlist':nlist,'nowpage':nowpage}
    return render(request, 'nlist.html', context)


def nview(request,n_no):
    qs = News.objects.get(n_no=b_no)
    qs.n_hit += 1
    qs.save()
    context={'board':qs}
    return render(request,'nview.html',context)

def nwrite(request):
    return render(request, 'nwrite.html')

def nwriteOk(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    no = News.objects.aggregate(max_b_no=Max('b_no'))
    max_no = no['max_b_no'] 
    max_no += 1         
    n_no = max_no
    qs = News(n_no=n_no,n_title=title,n_content=content)
    qs.save()
    return redirect('board:nlist')

def nmodify(request,n_no):
    qs = News.objects.get(n_no=n_no)
    context={'board':qs}
    return render(request,'nmodify.html',context)

def nmodifyOk(request):
    n_no = request.POST.get('n_no')
    n_title = request.POST.get('n_title')
    n_content = request.POST.get('b_content')
    qs = News.objects.get(n_no=n_no)
    qs.n_title = n_title
    qs.n_content = n_content
    qs.save()
    return render(request,'nview.html',{"board":qs})

def ndelete(request,b_no):
    qs = News.objects.get(n_no=n_no)
    qs.delete()
    return redirect('board:nlist')


def comlist(request):
    qs = Comment.objects.all().order_by('-c_no')
    clist = list(qs.values())
    # context={'clist':qs}
    return JsonResponse(clist,safe=False)

def comm_count(): # 하단 댓글 저장의 숫자를 증가시키는 함수 전역함수로 빼봄 
    
    # c_no 수동으로 1씩증가해서 저장시켜줌.
    no = Comment.objects.aggregate(max_c_no=Max('c_no'))
    max_no = no['max_c_no']   # b_no 최대 번호를 찾음 1.2.5. ... 26
    max_no += 1          #최고 높은 숫자를 만들어줌. 27 = no+1
    return max_no

#하단 댓글 저장
def commwrite(request):
    
    # c_no 1씩증가 함수
    # 1씩증가 함수 호출
    c_no = comm_count()
    
    
    id = request.session.get('session_id')  # session에서 id값 변수저장
    print("views id : ",id)
    # models 2.member객체
    member = Member.objects.get(m_id=id)
    b_no = request.GET.get("b_no")     # board b_no 변수저장
    # models 3.fboard객체
    fboard = Fboard.objects.get(b_no=b_no)
    # 4.c_pw
    c_pw = request.GET.get("c_pw")     #ajax으로 넘어온 pw 변수저장
    # 5.c_content
    c_content = request.GET.get("c_content")  #ajax으로 넘어온 content변수 저장
    # 6.c_date
    # 댓글저장
    qs = Comment(c_no=c_no,member=member,fboard=fboard,c_pw=c_pw,c_content=c_content)
    qs.save()
    context = {
        "c_no": qs.c_no, 
        "member_id": qs.member_id, 
        "c_pw": qs.c_pw,
        "c_content":qs.c_content,
        "c_date":qs.c_date }
    return JsonResponse(context)

#하단 댓글 삭제 (ajax)
def commdelete(request):
    c_no = request.GET.get('c_no')
    qs = Comment.objects.get(c_no = c_no)
    qs.delete()
    context = {'result':'댓글이 삭제되었습니다(views).'}
    
    return JsonResponse(context , safe=False)

def commupdateok(request):
    c_no = request.GET.get('c_no')
    c_content = request.GET.get('c_content')
    qs = Comment.objects.get(c_no = c_no)
    qs.c_content = c_content
    qs.save()
    
    context = {
        "c_no": qs.c_no, 
        "member_id": qs.member_id, 
        "c_pw": qs.c_pw,
        "c_content":qs.c_content,
        "c_date":qs.c_date 
    }
    return JsonResponse(context)