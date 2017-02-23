from django.test import TestCase

# Create your tests here.

    
f = open('outtape/tape.txt','r')
lines = f.readlines()
f.close
tapes = {}
for line in lines:
    l = line.split()
    tapes[l[0]] = []
    tapes[l[0]] = l
