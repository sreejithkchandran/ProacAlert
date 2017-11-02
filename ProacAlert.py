import xml.etree.ElementTree as ET
import re
import urllib
import sqlite3
from easy7zip import easy7zip
import os
import ctypes
from ctypes import *
from ctypes.wintypes import *
import win32com.client as win32
from ConfigParser import SafeConfigParser
import schedule
import time
import smtplib
import datetime
import sys
import string
MB_OK = 0x0
MB_ICONWARNING = 0x00000030

__author__ = 'Sreejith KOVILAKATHUVEETTIL CHANDRAN'
__version__ = '0.0.1'
__copyright__ = " Copyright 2017,SREEJITH KOVILAKATHUVEETTIL CHANDRAN"
__email__ = "sreeju_kc@hotmail.com"
__license__ = "Apache License 2.0"
__last_modification__ = '2017.10.21'


"""This is a Windows based vulnerability alert application, this applicatiion sync with NVD NIST data base on a regular interval and alert the user either via popup, outlook email or email relay"""
"""It can be tuned based on product, vendor or CVE score or combining all together using a config.ini file which comes along with the package, and also includes a sqlite DB to avoid duplicate alerting """
"""The objective of this tool is to alert about new vulnerabilities by running as a completely local instance without any server or web service. This tool can be installed on Windows desktop or server."""
"""The only prerequisite is a preinstalled 7-Zip commandline version program in either C:\ or C:\Program Files."""
"""Default CVE Score is 7, so even if you comment out the score session in config.ini it will continue to report score 7"""
"""Please look at the config.ini file or readme for more information"""
"""As sync time is 2hrs this application wont perfrom anything if you run before that period."""
"""The best approach is to run this application via schedule task and make sure to provide application directory path in "start in", otherwise it wont work""" 

def sync():
    cudir = os.getcwd()
    os.chdir(cudir)
    filenam = "nvdcve-2.0-recent.xml"
    rnw = time.time()
    if os.path.exists("nvdcve-2.0-recent.xml"):
        file_modified = datetime.datetime.fromtimestamp(os.path.getatime("nvdcve-2.0-recent.xml"))
        if datetime.datetime.now() - file_modified > datetime.timedelta(hours=2):
            try:
                os.remove("nvdcve-2.0-recent.xml.zip")
                os.remove("nvdcve-2.0-recent.xml")
            except Exception as e:
                print (e.message, e.args)
                time.sleep(60)
            dwnl(cudir)
            inpu(filenam,cudir)
        else:
            sys.exit()
    else:
        dwnl(cudir)
        inpu(filenam,cudir)
def inpu(filenam,cudir):
    config = SafeConfigParser()
    config.read('config.ini')
    ven =""
    pro = ""
    scs = ""
    emaout = ""
    emre = ""
    sendemai = ""
    receemai = ""
    port = ""
    emrelay=False
    outmail= False
    popup = True
    if config.has_option('CVE', 'Product'):
        pro = config.get('CVE', 'Product')
    if config.has_option('CVE', 'Vendor'):
        ven = config.get('CVE', 'Vendor')
    if config.has_option('CVE', 'Score'):
        scs =config.get('CVE', 'Score')
    if config.has_option('Outlook Mail', 'Recipient'):
        emaout =config.get('Outlook Mail', 'Recipient')
    if config.has_option('EMAIL Relay', 'Relay IP'):
        emre=config.get('EMAIL Relay', 'Relay IP')
    if config.has_option('EMAIL Relay', 'Port'):
        port=config.get('EMAIL Relay', 'Port')
    if config.has_option('EMAIL Relay', 'Sender'):
        sendemai=config.get('EMAIL Relay', 'Sender')
    if config.has_option('EMAIL Relay', 'Recipient'):
        receemai=config.get('EMAIL Relay', 'Recipient')
    velist = ven.split(",")
    velist = filter(None, velist)
    velist = list(set(velist))
    velist = [x.lower() for x in velist]
    prlist = pro.split(",")
    prlist = filter(None, prlist)
    prlist = list(set(prlist))
    prlist = [x.lower() for x in prlist]
    eamilist = emaout.split(",")
    eamilist = filter(None, eamilist)
    eamilist = list(set(eamilist))
    senemailist = sendemai
    recemailist = receemai.split(",")
    recemailist = filter(None, recemailist)
    recemailist = list(set(recemailist))
    if eamilist:
        for email in eamilist:
            if not re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",email):
                print email +" is not a valid email address.If you are using mutiple email address then use comma to seperate .Please correct and continue."
                if os.path.exists("nvdcve-2.0-recent.xml"):
                    os.remove("nvdcve-2.0-recent.xml.zip")
                    os.remove("nvdcve-2.0-recent.xml")  
                time.sleep(60)
                sys.exit()
    if senemailist:
        if not re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",senemailist):
            print senemailist +" sender is not a valid email address.If you are using mutiple email address then use comma to seperate .Please correct and continue."
            if os.path.exists("nvdcve-2.0-recent.xml"):
                os.remove("nvdcve-2.0-recent.xml.zip")
                os.remove("nvdcve-2.0-recent.xml")
            time.sleep(60)
            sys.exit()
    if recemailist:
        for remail in recemailist:
            if not re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",remail):
                print remail +" receiver is not a valid email address.If you are using mutiple email address then use comma to seperate .Please correct and continue."
                if os.path.exists("nvdcve-2.0-recent.xml"):
                    os.remove("nvdcve-2.0-recent.xml.zip")
                    os.remove("nvdcve-2.0-recent.xml")
                time.sleep(60)
                sys.exit()
    if emre:
        if not re.match("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$",emre):
                print emre +" is not a valid email address.If you are using mutiple email address then use comma to seperate .Please correct and continue."
                if os.path.exists("nvdcve-2.0-recent.xml"):
                    os.remove("nvdcve-2.0-recent.xml.zip")
                    os.remove("nvdcve-2.0-recent.xml")
                time.sleep(60)
                sys.exit()
    if not scs or not re.match("\d+\.\d+|\d+",scs):
        scs = 7.0
    if not re.match("\d+",port):
        port = '25'
    port = str(port)
    scf = float(scs)
    if scf > 10:
        scf = 7.0
    print scf
    if emre and senemailist and recemailist:
        emrelay = True
    if eamilist:
        outmail = True
    if emrelay == True and outmail == True:
        outmail = False
    xmpar(filenam,cudir,velist,prlist,eamilist,scf,emre,port,senemailist,recemailist,emrelay,outmail)
def xmpar(filenam,cudir,velist,prlist,eamilist,scf,emre,port,senemailist,recemailist,emrelay,outmail):
    try:
        tree = ET.parse(filenam)
        root = tree.getroot()
    except Exception as e:
        print (e.message, e.args)
        time.sleep(60)
    for entry in root.findall('{http://scap.nist.gov/schema/feed/vulnerability/2.0}entry'):
        prolist = []
        metrilist = []
        id = entry.get('id')
        summary = entry.find('{http://scap.nist.gov/schema/vulnerability/0.4}summary').text
        software = entry.find('{http://scap.nist.gov/schema/vulnerability/0.4}vulnerable-software-list')
        if software is not None:
            for sw in software.findall('{http://scap.nist.gov/schema/vulnerability/0.4}product'):
                prolist.append(sw.text)
        ven = ""
        unipro = list(set(prolist))
        if unipro:
            try:
                 rele=re.compile("cpe:/\w:(.*?)\:(.*?)($|\:)")
                 vendor = [m.group(1) for l in unipro for m in [rele.search(l)] if m]
                 product =[m.group(2) for l in unipro for m in [rele.search(l)] if m]
            except Exception as e:
                print (e.message, e.args)
                time.sleep(60)
            vendor = list(set(vendor))
            product = list(set(product))
        metrics = entry.find('{http://scap.nist.gov/schema/vulnerability/0.4}cvss')
        if metrics is not None:
            for metric in metrics.find('{http://scap.nist.gov/schema/cvss-v2/0.2}base_metrics').findall('*'):
                metrilist.append(metric.tag.replace('{http://scap.nist.gov/schema/cvss-v2/0.2}', '') + ': ' + metric.text)
                score = ""
                sc = ""
                for i in metrilist:
                    if 'score:' in i:
                        score = i
                        sc = re.search("score:\s+(.*)", score).group(1)
                        sc = sc.rstrip('\r')
                        sc = float(sc)
                    if 'generated-on-datetime' in i:
                        dat = i
                        scd = re.search("generated-on-datetime:\s(\d{4}-\d{1,2}-\d{1,2}).*",dat).group(1)
                        scd = scd.rstrip('\r')
            if sc >= scf:
                ret = dbsel(id,cudir)
                if ret == False:
                    ids = str(id)
                    scds = str(scd)
                    scs = str(sc)
                    products = str(product)
                    vendors = str(vendor)
                    summarys = str(summary)
                    if prlist and velist :
                        for vit in velist:
                            if vit in vendor:
                                for pit in  prlist:
                                    if pit in product:
                                        if emrelay == True:
                                            emaire(ids,scds,scs,products,vendors,summarys,emre,port,senemailist,recemailist)
                                        elif outmail == True:
                                            oumail(ids,scds,scs,products,vendors,summarys,eamilist)
                                        else:
                                            pomes(ids,scds,scs,products,vendors,summarys,eamilist)
                                            
                    elif prlist and not velist:
                        for pit in prlist:
                            if pit in product:
                                if emrelay == True:
                                    emaire(ids,scds,scs,products,vendors,summarys,emre,port,senemailist,recemailist)
                                elif outmail == True:
                                    oumail(ids,scds,scs,products,vendors,summarys,eamilist)
                                else:
                                    pomes(ids,scds,scs,products,vendors,summarys,eamilist)
                    elif velist and not prlist:
                        for vit in velist:
                            if vit in vendor:
                                if emrelay == True:
                                    emaire(ids,scds,scs,products,vendors,summarys,emre,port,senemailist,recemailist)
                                elif outmail == True:
                                    oumail(ids,scds,scs,products,vendors,summarys,eamilist)
                                else:
                                    pomes(ids,scds,scs,products,vendors,summarys,eamilist)   
                    elif not prlist and not velist:
                        if emrelay == True:
                            emaire(ids,scds,scs,products,vendors,summarys,emre,port,senemailist,recemailist)
                        elif outmail == True:
                            oumail(ids,scds,scs,products,vendors,summarys,eamilist)
                        else:
                            pomes(ids,scds,scs,products,vendors,summarys,eamilist)
            if score:
                dbins(id,cudir)
            
def dbins(id,cudir):
    pat = False
    if os.path.exists(cudir+"\cvvid.db"):
        pat = True
    if pat == True:
        try:
            conn = sqlite3.connect(cudir+"\cvvid.db")
            cursor = conn.cursor()
        except Exception as e:
            print (e.message, e.args)
            time.sleep(60)
    elif pat == False:
        print "Can't find the DB, please move the cvvid.db file to application directory to continue"
        time.sleep(60)
        sys.exit()
    try:
        cursor.execute("INSERT OR IGNORE INTO CVV(CVID) values(?);",(id,))
        conn.commit()
    except Exception as e:
        print (e.message, e.args)
        time.sleep(60)
    conn.close()
def dbsel(id,cudir):
    pat = False
    if os.path.exists(cudir+"\cvvid.db"):
        pat = True
    if pat == True:
        try:
            conn = sqlite3.connect(cudir+"\cvvid.db")
            cursor = conn.cursor()
        except Exception as e:
            print (e.message, e.args)
            time.sleep(60)
    elif pat == False:
        print "Can't find the DB, please move the cvvid.db file to application directory to continue"
        time.sleep(60)
        sys.exit()
    try:
        cursor.execute("SELECT * FROM CVV WHERE CVID=? ",(id,))
        li = cursor.fetchone()
        if not li:
            return False
        conn.close()
    except Exception as e:
        print (e.message, e.args)
        time.sleep(60)
def pomes(ids,scds,scs,products,vendors,summarys,eamilist):
    tvendor = vendors.upper()
    titl = "VULNERABILITY ALERT "+tvendor+"!!"
    id = ids
    ids = "CVE ID: "+ids+'\n\n'
    scds = "CVE generated date: "+scds+"\n\n"
    scs = "CVE Score: "+scs+"\n\n"
    products = "Product: "+ products+"\n\n"
    vendors = "vendor: "+vendors+"\n\n"
    summarys = "Summary: "+summarys+"\n\n\n"
    det = "For more detailed information please visit "+"https://nvd.nist.gov/vuln/detail"+"/"+id+"\n\n\n"
    mes = ids+scds+scs+products+vendors+summarys+det
    try:
        val = ctypes.windll.user32.MessageBoxA(0, mes, titl,MB_OK|MB_ICONWARNING)
        f = "logs.txt"
        with open(f,'a') as files:
            files.write("\n")
            files.write(mes)
            files.write("\n")
            files.write("\n")
            files.write("==============================================================================================\n")
            
    except Exception as e:
        print (e.message, e.args)
        time.sleep(60)
def oumail(ids,scds,scs,products,vendors,summarys,eamilist):
    tvendor = vendors.upper()
    titl = "VULNERABILITY ALERT "+tvendor+"!!"
    hid = "CVE ID: "+ids+"<br>"
    hscd = "CVE generated date: "+scds+"<br>"
    hsc = "CVE score: "+scs+"<br>"
    hproduct = "Product: "+ products+"<br>"
    hvendor = "vendor: "+vendors+"<br>"
    hsummary = "Summary: "+summarys+"<br>"
    url= "https://nvd.nist.gov/vuln/detail"+"/"+ids
    detht = '<a href='+url+'>For more detailed information please visit</a>'
    fomes = hid+"<br>"+hscd+"<br>"+hsc+"<br>"+hproduct+"<br>"+hvendor+"<br>"+hsummary+"<br>"+ "<br>"+"<br>"+"<br>"+detht
    eamilist = ";".join(eamilist)
    try:
        eamilist = str(eamilist)
        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        mail.Subject = titl
        mail.HtmlBody = fomes
        mail.To = eamilist
        mail.Send()
    except Exception as e:
        print (e.message, e.args)
        time.sleep(10)
        pass
def emaire(ids,scds,scs,products,vendors,summarys,emre,port,senemailist,recemailist):
    id = ids
    tvendor = vendors.upper()
    titl = "VULNERABILITY ALERT "+tvendor+"!!"
    ids = "CVE ID: "+ids+'\n\n'
    scds = "CVE generated date: "+scds+"\n\n"
    scs = "CVE Score: "+scs+"\n\n"
    products = "Product: "+ products+"\n\n"
    vendors = "vendor: "+vendors+"\n\n"
    summarys = "Summary: "+summarys+"\n\n\n"
    det = "For more detailed information please visit "+"https://nvd.nist.gov/vuln/detail"+"/"+id+"\n\n\n"
    mes = ids+scds+scs+products+vendors+summarys+det
    subject = "VULNERABILITY ALERT "+tvendor+"!!"
    try:
        message = string.join((
            "From: %s" % senemailist,
            "To: %s" % ', '.join(recemailist),
            "Subject: %s" % titl ,
            "",
            mes
            ), "\r\n")
        #message = 'Subject: %s\n\n%s' % (titl,mes)
        smtpObj = smtplib.SMTP(emre+':'+port) 
        em = smtpObj.sendmail(senemailist,recemailist,message)
    except Exception as e: 
        print (e.message, e.args)
        time.sleep(60)
def dwnl(cudir):
    os.chdir(cudir)
    url = "https://static.nvd.nist.gov/feeds/xml/cve/2.0/nvdcve-2.0-recent.xml.zip"
    try:
        testfile = urllib.URLopener()
        tt = testfile.retrieve(url,"nvdcve-2.0-recent.xml.zip")
        if 'nvdcve-2.0-recent.xml.zip' not in tt:
            raise Exception("Download failed, please make sure your internet connection is ok")
    except Exception as e:
        print (e.message, e.args)
        time.sleep(60)
    try:
        te = easy7zip()
        rr = te.ExtractFromArch(cudir+"\nvdcve-2.0-recent.xml.zip",cudir)
    except Exception as e:
        print (e.message, e.args)
        time.sleep(60)
    
    
if __name__ == "__main__":
    sync()
