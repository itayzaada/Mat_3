# -*- coding: utf-8 -*-

"""
Created on Wed Apr 28 20:20:14 2021

@author: Itay Zaada
"""

def  reader (file):
    fhand = open(file,'r',encoding='UTF-8')
    return fhand
    
def  messages (file):  
    fhand =reader(file)
    fhand=fhand.readlines()
    id=0 
    txti=" "
    text=" " 
    lst=[]
    lst2=[]
    for line in fhand :
        line= line.strip()
        if 'הוסיף/ה'in line or'החליף/ה ' in line or '‏יצרת' in line or 'המדיה' in line or 'שינית את' in line  or 'הסיר/ה ' in line or '‏הוספת' in line or 'עזב/ה' in line  or'מוצפנות'in line or'נוצרה'in line : ## ignore system messages##
            continue 
        if not line .startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')) : ## new message start with date##
           txti=line
           lst[id-1]["text"]=text+" "+txti # add the new messagw to the previus one ##
        else:                      #breaking the line into parts #
           line= line.strip() ## breking to parts by signs ##
           date=line.split(",")
           date0=date[0].strip()# the date#
           date1=date[1].strip()
           time=date1.split(" ",1)
           timer=time[0].strip()## the time#
           telnum=time[1].split(":")
           number=telnum[0].strip().split("-",1)
           telphone=number[1].strip()## the phone number ##ז
           text=telnum[1]##text##
           if telphone not in lst2:## ig thephone is uniqe add it to lst2 and make dict##
               lst2.append(telphone)
               dict={"datetime":date0+ " "+timer, "id" :id,"text": text}
               lst.append(dict)
               id=id+1
           else :
               index=lst2.index(telphone)
               dict={"datetime":date0+ " "+timer, "id" :index,"text": text}
               lst.append(dict)

    return lst 

def  num_of_participants (file):  
    fhand =reader(file)
    fhand=fhand.readlines()[5:]
    txti=" "
    lst2=[]
    for line in fhand :
        line= line.strip()
        if 'הוסיף/ה'in line or'החליף/ה ' in line or '‏יצרת' in line or 'המדיה' in line or 'שינית את' in line  or 'הסיר/ה ' in line or '‏הוספת' in line or 'עזב/ה' in line  or'מוצפנות'in line or'נוצרה'in line : ## ignore system messages##
            continue         
        if not line .startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')) : 
           txti=line
           txti
        else:
           line= line.strip()
           date=line.split(",")
           date1=date[1].strip()
           time=date1.split(" ",1)
           telnum=time[1].split(":")
           number=telnum[0].strip().split("-",1)
           telphone=number[1].strip()##phone number ##ז
           if telphone not in lst2:
               lst2.append(telphone)
           else :
               continue
    return len(lst2) ## the length og lst2 is the number of people in the group ## 

def  metadata (file):  

    fhand =reader(file)
    fhand=fhand.readlines()[:3]
    for line in fhand :
      line= line.strip()
      if "נוצרה על ידי" in line:## if its the line of creation ## 
          date=line.split(",")
          date0=date[0].strip()#date#
          a=line.split("הקבוצה ")
          b=a[1].strip()
          c=b.split("נוצרה על ידי")
          creator=c[1].strip()
          name=c[0].strip()
          name=name.strip()
          dic={"chat_name": name.strip(), "creation_date" :date0,"num_of_participants":num_of_participants (file)  ,"creator":creator}
    return dic


def  groupname (file):  ## to extract the name of he group ## 
    fname=" "
    fhand =reader(file)
    fhand=fhand.readlines()[:3]
    for line in fhand :
      line= line.strip()
      if "נוצרה על ידי" in line  :
          part1=line.split("הקבוצה ")
          part2=part1[1].strip()
          part3=part2.split("נוצרה על ידי")
          name=part3[0].strip()
          name=name.strip()
          fname=name.strip('"')
    return fname


def both (file): ## combine the 2 dict ## 
    dic={"messages":messages(file),"metadata":metadata(file)}
    return dic
    
def json_creator(file): ## create a json file with the group name ## 
    import json
    dic=both(file)
    group=groupname(file)+".json"
    jsonString=json.dumps(dic)
    jsonFile=open(group, "w")
    jsonFile.write(jsonString)

file=input("Enter File Name : ")
print(both(file))
json_creator(file)
