# --*-- coding:utf-8 --*--
import re
import web

fname = 'files/backup.txt'
with open(fname,'r') as f:
    report = f.read().strip()

p = re.compile(r'Object status.*?:\s+(\S+).*?Started.*?:\s+([A-Z].*?\d{4}).*?Finished.*?:\s+([A-Z].*?\d{4}).*?Object size.*?:\s+(\d+).*?Device name\s+:\s+(\S+\s+\S+).*?session name:(\S+)',re.S)
#p = re.compile(r'Object status.*?:\s+(\S+)\s+\n\s+Started\s+:\s+([A-Z].*?\d{4})\s+\n\s+Finished\s+:\s+([A-Z].*?\d{4})\s+\n\s+Object size\s+:\s+(\d+)\s+KB\s+\n\s+')
L = p.findall(report)
