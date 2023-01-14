import netmiko
import re
Swit1= {
        "device_type":"cisco_ios",
        "host":"192.168.0.4",
        "username":"cisco",
        "password":'cisco',
        "port":"22",
        "secret":"cisco",
        }
CONEX= netmiko.ConnectHandler(**Swit1)
x = input("introduce mac address")
while True:
    COMANDO = CONEX.send_command("sh mac address-table")
    
    look = re.search(x, COMANDO)
    if look is not None:       
        seat = "show mac address-table address"+" "+x
        elprin = CONEX.send_command(seat)
        
        PORT = re.findall(r"\w\w\w?\d\/\d\/?\d?\d?", elprin)
        PUERTO= (PORT[0])
        print("MAC address encontrada en el puerto: ", PUERTO)

        cdp  = CONEX.send_command("sh cdp neigh")
        PORT2 = re.findall(r"(Gi|Fa)", cdp)#((Gi|Fa)|\d\/\d\/?\d?\d?)
        PORT3 = re.findall(r"(\d\/\d\/?\d?\d?)", cdp)
        try:
            for pp in range (0,20,2):
                PRT=(PORT2[pp])
            
                PRT2=(PORT3[pp])
                PRT3= (PRT)+(PRT2)
                if PRT3 == PUERTO:                
                    break
        except IndexError:
            print("")
            break
        PRT=(PORT2[pp])
        PRT2=(PORT3[pp])
        PRT3= (PRT)+(PRT2)
    
        posID=pp//2
        posIP=pp*2//2
        if PRT3 == PUERTO:
            Ndet = CONEX.send_command("sh cdp neigh det")
            LaIP= re.findall(r"\d\d\d[.]\d\d?\d?[.]\d\d?\d?[.]\d\d?\d?", Ndet)
            ID= re.findall(r"Device.ID: ..?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?", Ndet)
            SWITCH = (ID[posID])
            IP =(LaIP[posIP])
            Swit2= {
                    "device_type":"cisco_ios",
                    "host":IP,
                    "username":"cisco",
                    "password":'cisco',
                    "port":"22",
                    "secret":"cisco",
                 }
            CONEX= netmiko.ConnectHandler(**Swit2)
            print("conectado a: ", SWITCH)
            trell = CONEX.send_command("sh running-config | include hos")
            HOST= re.findall(r"[^hostname ]..?.?.?.?.?.?.?.?.?", trell)
            olei= (HOST[0])
            print("ACTUAL: ", olei)
    else:
        print("No se encontro la mac address")
        break