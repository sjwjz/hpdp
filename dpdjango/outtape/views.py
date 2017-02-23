from django.shortcuts import render
from django.http import HttpResponse
from outtape import tapes
# Create your views here.

def index(request):
    #return HttpResponse("out tape.")
    #aaa = 'you are welcome'
    #return HttpResponse(tape)
    #tape = [1,2,3,4]
    #ctape = {'a':'good','b':'bad','c':'very good'}
    return render(request,'outtape/chuku.html',{'tapes':tapes})

def move_tape_to_i(*tape):
    pass

def outtape(request):
    out_tapes_bar = request.POST.getlist('tape')
    out_tapes = {}
    for tape in out_tapes_bar:
        print tapes[tape][1]
        out_tapes[tape]=[tapes[tape][0],tapes[tape][1],tapes[tape][7]]
    return render(request,'outtape/outtape.html',{'out_tapes':out_tapes})