#me4401-32b mac.log from me router and using command dis mac-address dy
from pprint import pprint
import pandas as pd
import numpy as np
import csv
import os
import re
import time
######
# in ME dis mac-add dy 
# in MP dis arp all
#       dis current-configuration int
#       dis int des
######
def main() :
    ME_mac_file = 'me mac.log'
    MP_arp_file = 'mp cmi arp.log'
    MP_int_des = 'mp int des.log'
    MP_int_con = 'mp cmi int con.log'
############################################################ ME part########################################
    me_mac = None   #in me -- dis mac-add dy 
    me_mac = []
    with open(ME_mac_file, 'r') as file:  
        for line in file:
            line = line.split()
            me_mac.append(line)
    print("first start at :"+str(me_mac[5]))
    me_mac =me_mac[6:] #mac add start at [6]
    # print(len(me_mac))
    print("last end at :"+str(me_mac[-1]),"\n")
    me_mac = me_mac[:-3] #delete last 3 useless data // or 2 chang it urself
    print("first data is :",me_mac[0])
    print("last data is :",me_mac[-1],"\n")

    #check all data have same len(att)
    yyy = []
    for i in range(len(me_mac)) :
        if(len(me_mac[i])<=6) :
            continue
        else :
            yyy.append(me_mac[i])
    me_mac = yyy

    me_mac = splitVlanfrominterface(me_mac,4)
    print("after faded vlan :",me_mac[0])
    print("len is :",len(me_mac),"\n")

    # me_mac = checkHavevlanornot(me_mac,7)
    # print("after select only having vlan :",me_mac[0])
    # print("len is :",len(me_mac),"\n")
          

################################################################################################################
################################################################################################################
################################################################################################################
################################################################################################################
################################################################################################################
################################################################################################################

    me_mac = filtercutVSIthatuse(me_mac,1,"HSI",1)
    me_mac = filtercutVSIthatuse(me_mac,1,"HOTSPOT",1)
    me_mac = filtercutVSIthatuse(me_mac,1,"1005",1)
    me_mac = filtercutVSIthatuse(me_mac,1,"1084",1)

    # keep_vsi_list = ["1005","1084"]
    # me_mac = filterkeepVSIthatuse(me_mac,1,keep_vsi_list,1)

################################################################################################################
################################################################################################################
################################################################################################################
################################################################################################################
################################################################################################################
################################################################################################################
    print(me_mac)
    print("after filter :",me_mac[0])
    print("len is :",len(me_mac),"\n")

    with open('me_mac.csv', 'w', newline = '') as fp:
        writer = csv.writer(fp, delimiter = ',')
        for row in me_mac:
            writer.writerow(row)

    mac_in_me = []
    for mac in me_mac :
        mac_in_me.append(mac[0])
    # print (mac_in_me,"\n")
    # for i in me_mac :
    #     print(i)
# ############################################################ ME part########################################

    
# ########################################################### MP part########################################
    mp_arp = []   # in mp -- dis arp all
    with open(MP_arp_file, 'r') as file:  
        for line in file:
            line = line.split()
            mp_arp.append(line)
    mp_arp = mp_arp[4:]
    mp_arp = mp_arp[:-3]

    for i in mp_arp :
        if(len(i)==1) :
            mp_arp.remove(i)

    mp_arp = splitVlanfrominterface(mp_arp,4)
    mp_arp = checkVPNfromarp(mp_arp)
    for i in mp_arp : # check all att have same number of column
        if(len(i)!=7) :
            print ("error")

    print("This is example of me_mac :")
    print(me_mac[0])
    print("This is example of mp_arp :")
    print(mp_arp[0],"\n")

    interface_vsi_list = findvsionMp(MP_int_con) # use -- dis current-configuration int
    print("This is example of interface_vsi_list :")
    print(interface_vsi_list[0],"\n")

    for i in range(len(interface_vsi_list)) : #replaceWord
        if("Virtual-Ethernet" in interface_vsi_list[i][0]) :
            if("1." in interface_vsi_list[i][0]) :
                interface_vsi_list[i][0] = interface_vsi_list[i][0].replace("1.","0.") 
            interface_vsi_list[i][0] = interface_vsi_list[i][0].replace("Virtual-Ethernet","VE") 
        elif("GigabitEthernet" in interface_vsi_list[i][0]) :
            if("1." in interface_vsi_list[i][0]) :
                interface_vsi_list[i][0] = interface_vsi_list[i][0].replace("1.","0.") 
            interface_vsi_list[i][0] = interface_vsi_list[i][0].replace("GigabitEthernet","GE")

    print("This is example of interface_vsi_list after chang word:")
    print(interface_vsi_list[0],"\n")
 
    #compare interface_vsi_list to mp_arp
    for i in range(len(mp_arp)) :
        for j in range(len(interface_vsi_list)) :
            if (mp_arp[i][4]==interface_vsi_list[j][0]) :
                mp_arp[i].append(interface_vsi_list[j][1])
                break
    #insert data that no VSI name
    for i in range(len(mp_arp)) :
        if(len(mp_arp[i])==7) :
            mp_arp[i].append("No VSI name")

    print("This is example of mp_arp after add vsi :")
    print(mp_arp[0],"\n")

    # mapped_dataset = mapMacaddress(me_mac,0,mp_arp,1)
    # # print (mapped_dataset)
    # print (len(mapped_dataset))
###################################################################################### 
    int_des = []   # mp -- dis int des
    with open(MP_int_des, 'r') as file:  
        for line in file:
            line = line.split()
            int_des.append(line)
    int_des = int_des[14:]

    for i in range(len(int_des)) :  # check have or not descri
        tmp = int_des[i]
        if (len(int_des[i])<4) :
            int_des[i].append("No descri")

############################# INT DES ###########################################################
    match = []
    for i in me_mac :
        for j in mp_arp :
            if(i[0]==j[1] and i[1]==j[7]) :
                match.append(j)
    
    print("This is example of match :")
    print(match[0])
    print(len(match),"\n")
    
    temp_match = match
    for i in range(len(temp_match)) :
        for j in range(len(int_des)) :
            if(temp_match[i][4]==int_des[j][0]) :
                match[i].append(int_des[j][3])
                break

    print("This is example after add descri :")
    print (match[0])

    ############### add command
    for i in range(len(match)) :
        match[i].append("ping -vpn-instance "+match[i][5]+" -c 3 -m 100 -t 300 -q "+match[i][0])

    match = sorted(match, key=lambda x : x[7])
    with open('Other.csv', 'w', newline = '') as fp:
        writer = csv.writer(fp, delimiter = ',')
        for row in match:
            writer.writerow(row)
    
    
#######################################################################################################################


def findvsionMp(filename) :
    interface_vsi = []

    with open(filename, 'r') as file:  
        state = True
        interface = []
        vsi = []
        for line in file:
            if "#" in line :
                continue
            if(state == True) :
                if "interface " in line:
                    line = line.split()
                    interface = line[1]
                if "l2 binding vsi " in line:
                    line = line.split()
                    vsi = line[3]
                if((interface)and(vsi)) :
                    tmp = []
                    tmp.append(interface)
                    tmp.append(vsi)
                    interface_vsi.append(tmp)
                    interface = []
                    vsi = []
    return interface_vsi

def mapMacaddress(me_dataset,me_column,mp_dataset,mp_column) :
    #in fact number of mac in mp always > me
    tmp = []
    for i in mp_dataset :
        for j in me_dataset :
            temp = []
            if(i[mp_column]==j[me_column]) :
                space =["-----"]
                join_list = i+space+j
                tmp.append(join_list)
    return tmp

def filterkeepVSIthatuse(dataset,column_of_vsi,word_of_vsi_list,position_of_filter) : #ไม่เอาตัวไหนบ้าง
    tmp = []
    for i in dataset :
        vsi = i[column_of_vsi]
        vsi = vsi.split("-")
        print (vsi)
        if(len(vsi)<2) :
            continue
        else :
            if(vsi[position_of_filter] in word_of_vsi_list) :
                tmp.append(i)
            else :
                continue
    return tmp

def filtercutVSIthatuse(dataset,column_of_vsi,word_of_vsi,position_of_filter) : #ไม่เอาตัวไหนบ้าง
    tmp = []
    for i in dataset :
        vsi = i[column_of_vsi]
        vsi = vsi.split("-")
        if(len(vsi)<2) :
            continue
        else :
            if(vsi[position_of_filter] == word_of_vsi) :
                # print("kuy")
                continue
            else :
                tmp.append(i)
            
    return tmp

def checkVPNfromarp(dataset) :
    temp = []
    for arp in dataset :
        if(len(arp)==6) : # 6 is len(dataset[0])
            # print ("no VPN")
            arp.append("nan")
        temp.append(arp)
    return temp

def checkHavevlanornot (dataset,column) :
    tmp = []
    for i in dataset :
        if(i[column] == "nan") :
            continue
        else :
            tmp.append(i)
    return tmp

def splitVlanfrominterface(setdata,column) :
    temp = []
    for i in setdata :
        kuy = i[column]
        kuy = kuy.split(".")
        if(len(kuy)==1) :
            # print (i)
            # print ("have data no vlan")
            kuy.append("nan")
        i.append(kuy[1])
        temp.append(i)
    return temp


if __name__ == "__main__":
    main()