# --*-- coding:utf-8 --*--
from django.shortcuts import render
from django.http import HttpResponse
from .models import bk_policy,bk_plan
import dpdjango.dp.dpok as dpok

# Create your views here.
def index(request):
    data = {'a':'1','b':'2','c':'3'}
    dpok.get_all()
    print dpok.sch
    return render(request,'dp/index2.html',{'policy':dpok.sch,})

def detail(request,task_id):
    context = {
        'task':bk_policy.objects.get(pk=task_id)
    }
    return render(request,'dp/detail.html',context)



