

# Estos son los parámetros de la máquina, los que tienen comentarios encima deben de cambiarse al hacer una VM nueva o una sola vez

ramMB = 4096

discoGB = 50

# Se debe de cambiar POR CADA MÁQUINA VIRTUAL NUEVA porque no puede haber 2 VMs con el mismo nombre
nombremaquina= "verdaderamenteestasi"

sistemaoperativo= "Linux"



nombreDeDiscoVM= "efectivamente.vdi"

tipoDeDisco = "hdd"

formatoDisco = "VDI"

portdisco = 0

devicedisco = 0

controladornombre= "micontrolador"

controladortipo= "SATA"

chipset="PIIX3"





controladornombreISO= "micontroladorISO"

controladortipoISO = "IDE"

chipsetISO="PIIX3"

portISO = 1

devISO = 1

typeISO = "dvddrive"


# Se debe de cambiar UNA SOLA VEZ porque la ruta no será la misma para acceder a los discos de las máquinas virtuales

rutadiscovm = (f"C:/Users/Carlos/{str(nombreDeDiscoVM)}")

# Se debe de cambiar UNA SOLA VEZ porque la ruta no será la misma para acceder a VBoxManage.exe

rutadevbox = "C:/Program Files/Oracle/VirtualBox/VBoxManage.exe"