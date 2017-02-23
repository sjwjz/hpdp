#!/usr/bin/python
import re

str = '''DATALIST "wlwjs7_backup_auto"
DYNAMIC 1 5
POSTEXEC "rename_backup.sh" -on_host "wlwjs7"
DEFAULTS
{
        FILESYSTEM
        {

        } 
        RAWDISK
        {

        } 
}

DEVICE "HP:Ultrium 5-SCSI_19" 
{
        -pool "wlw"
        -mp_preferred_host "cbbssys2"
} 

FILESYSTEM "/pboss_js7/backup01" wlwjs7:"/pboss_js7/backup01"
{
        -trees
                "/pboss_js7/backup01/OBII_BACKUP_AUTO"
} '''
str2 = '''DATALIST "gprsd1_backup_auto2"
DYNAMIC 1 5
POSTEXEC "rename_backup2.sh" -on_host "gprsd1"
DEFAULTS
{
        FILESYSTEM
        {

        } 
        RAWDISK
        {

        } 
}

DEVICE "HP:Ultrium 5-SCSI_13" 
{
        -pool "gprs"
        -mp_preferred_host "gprsd1"
} 

FILESYSTEM "/cbbs_gprsd1/data_backup2" gprsd1:"/cbbs_gprsd1/data_backup2"
{
        -trees
                "/cbbs_gprsd1/data_backup2/OBII_BACKUP_AUTO"
} 
'''
p = re.compile(r'(\w+)\s+\"(\S+)\"')
L1 = p.findall(str)
L2 = p.findall(str2)
print L1
print L2
