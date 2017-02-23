# -*- coding: utf-8 -*-
import re
import os
from dp.models import bk_policy,bk_plan
#import xlsxwriter

sch_dir = 'd:\\python27\\docu\\dp\\sch'
policy_dir = 'd:\\python27\\docu\\dp\\policy'




def get_sch(str):
    p = re.compile(r'(\d+)month')
    L1 = str.split()
    if str == 'day':
        return 'every day'
    elif str[0].isdigit():
        day_num = re.findall(r'(\d+)day',L1[0])
        if len(L1)  == 1:
            return 'every %s day'%day_num[0]
        else:
            return 'every %s weeks %s'%(day_num[0],' '.join(L1[1:]))
    elif '-month' in L1:
        return 'every month %s day'%L1[1]
    elif len(L1) >2 and 'month' in L1[2]:
        s1 = p.findall(L1[2])
        return 'every %s month %s day'%(s1[0],L1[1])
        #return 'bad'
    else:
        return 'every %s'%' '.join(L1[1:])


def get_bk_sch():
    p = re.compile(r'(full|incr \d)\s+(.*?)\n-every\s+-(\d?day.*?)\s+\n.*?-at\s+(\d+:\d+)')
    sch_dict = {}
    for file in os.listdir(sch_dir):
        fn = os.path.join(sch_dir,file)
        with open(fn,'r') as f:
            lines = f.read()
        if '-disabled' in lines:
            continue
        if not '-every' in lines:
            continue
        sch_dict[file]=p.findall(lines)


    for i,j in sch_dict.items():
        sch[i]={}
        sch[i]['bk_policy']=[]
        for h in j:
            bak_date = get_sch(h[2])
            bak_pro = get_pro(h[1])
            L = {'bk_level':h[0],'protect':bak_pro,'bk_plan':bak_date + ' ' + h[3]}
            sch[i]['bk_policy'].append(L)
    return sch

def get_pro(pro_time):
    if 'protection' in pro_time:
        pro = re.findall(r'-protection\s+-(\w+)\s+(\d+)',pro_time)
        return '%s %s'%(pro[0][1],pro[0][0])
    else:
        return 'default'







########################################################################################

p_dir = re.compile(r'FILESYSTEM\s+"(.*?)".*?\{(.*?)\}',re.S)
p_dev = re.compile(r'DEVICE\s+"(.*?)".*?\{(.*?)\}',re.S)
p_device = re.compile(r'-(.*?)\s+"(.*?)"')

def get_dev(str_file):

    L = p_dev.findall(str_file)
    D_dev = {}
    L_device = []
    L_pool = []
    L_da = []
    for i in L:
        L_device.append(i[0])
        L_dev = p_device.findall(i[1])
        for j in L_dev:
            if j[0] == 'pool':
                if len(L_pool) == 0 or L_pool[-1] != j[1]:
                    L_pool.append(j[1])
            elif j[0] == 'mp_preferred_host' :
                if len(L_da) == 0 or L_da[-1] != j[1]:
                    L_da.append(j[1])

    D_dev['dev']=' '.join(L_device)
    D_dev['pool'] = ' '.join(L_pool)
    D_dev['da'] = ' '.join(L_da)
    return D_dev


def get_dir(str_file):
    L_dir = p_dir.findall(str_file)
    D_dirs = {}
    L_tree = []
    L_exclude = []
    for i in L_dir:
        str_line = ' '.join(i[1].strip().split())
        if str_line  == '':
            L_tree.append(i[0])
        L = str_line.split('-')
        for i in L:
            if len(i)>1:
                dir = i.split()
                if dir[0] == 'trees':
                    L_tree.extend(dir[1:])
                elif dir[0] == 'exclude':
                    L_exclude.extend(dir[1:])
    D_dirs['tree'] = ' '.join(L_tree)
    D_dirs['exclude'] = ' '.join(L_exclude)
    return D_dirs

###################################################################################
sch = {}
def get_all():
    p_post = re.compile(r'POSTEXEC\s+"(.*?)"')
    sch = get_bk_sch()
    for fname in os.listdir(policy_dir):
        if fname not in sch:
            continue
        fn = os.path.join(policy_dir,fname)
        with open(fn,'r') as f:
            lines = f.read()

        sch[fname].update(get_dev(lines))
        sch[fname].update(get_dir(lines))
        sch[fname]['script'] = ' '.join(p_post.findall(lines))



###################################################################################
def write_xls():
    workbook = xlsxwriter.Workbook('backup1.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, u'备份任务')
    worksheet.write(0, 1, u'备份主机')
    worksheet.write(0, 2, u'备份目录')
    worksheet.write(0, 3, u'磁带机')
    worksheet.write(0, 4, 'DA')
    worksheet.write(0, 5, u'备份脚本')
    worksheet.write(0, 6, u'备份级别')
    worksheet.write(0, 7, u'保存期限')
    worksheet.write(0, 8, u'备份计划')

    i = 1
    for task,policy in sch.items():

        #print policy
        try:
            worksheet.write(i,0,task)
            #worksheet.write(i,1,task)
            worksheet.write(i,2,policy['tree'])
            worksheet.write(i,3,policy['dev'])
            worksheet.write(i,4,policy['da'])
            worksheet.write(i,5,policy['script'])
            worksheet.write(i,6,policy['bk_policy'][0]['bk_level'])
            worksheet.write(i,7,policy['bk_policy'][0]['protect'])
            worksheet.write(i,8,policy['bk_policy'][0]['bk_plan'])
        except:
            pass
        i = i + 1

    workbook.close()



#####################################################################################

#D_bk = {}
#for task,policy in sch.items():
#    if len(policy['bk_policy']) == 1:
#        D_bk[task] = {}
#        D_bk[task]['level'] = policy['bk_policy'][0]['bk_level']
#        D_bk[task]['protect'] = policy['bk_policy'][0]['protect']
#        D_bk[task]['bk_plan'] = policy['bk_policy'][0]['bk_plan']

def write_mysql():
    for task_name,policy in sch.items():
        try:
            q = bk_policy(task=task_name,client=policy['da'],trees=policy['tree'],drive=policy['dev'],da=policy['da'],script=policy['script'])
            q.save()
        except:
            pass



def main():
    get_all()



if __name__ == "__main__":
    main()
    #write_xls()
    for i,j in sch.items():
        print i,j



#########################################################################################

#for i,j in sch.items():
#    print i,j
#print len(sch)
#write_xls()
#print sch['CBBSBX6_backup_auto']['tree']
#print sch
####################################################################################
