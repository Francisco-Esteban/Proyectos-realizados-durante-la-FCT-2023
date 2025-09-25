
import os
import watchdog
import time
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import subprocess


# Aquí se harán unas variables en las que se ponen los parámetros que pide la VM
# estas variables se usarán para hacer un comando con ellas que el script pondrá automáticamente en la consola de Vbox tras abrirlo automáticamente son subprocess.call

# Los parámetros de la máquina
ramMB = 4096
discoGB = 50
nombremaquina= "aver5200"
sistemaoperativo= "Linux"



nombreDeDiscoVM= "sis5200.vdi"
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


# Los comandos para crear la máquina y configurarla

# Esta función define lo que se hará al crear un archivo en la carpeta MV dentro de ISOS, crear el archivo sería pegar una ISO en la carpeta

# En este caso he hecho que el script comunique que una ISO se ha detectado.

    
def al_crear_archivo(event):


    rutadiscovm = (f"C:/Users/Carlos/{str(nombreDeDiscoVM)}")
    rutadevbox = "C:/Program Files/Oracle/VirtualBox/VBoxManage.exe"
    nombrearchivo = os.path.basename(event.src_path)
    caminoarchivo = event.src_path

    comandovbox = [ (rutadevbox) , "createvm", "--name", str(nombremaquina), "--ostype", str(sistemaoperativo), "--register"]

    comandovboxMemoria = [(rutadevbox) , "modifyvm", str(nombremaquina), "--memory", str(ramMB) ]

    comandovboxCrearDisco = [ (rutadevbox) , "createhd", "--filename", str(nombreDeDiscoVM), "--size", str(discoGB), "--format", str(formatoDisco)]

    comandovboxCrearControlador= [ (rutadevbox),"storagectl", str(nombremaquina), "--add", str(controladortipo), "--name", str(controladornombre)] 

    comandovboxCrearControladorISO= [ (rutadevbox), "storagectl", str(nombremaquina), "--add", str(controladortipoISO), "--name", str(controladornombreISO)]

    comandovboxPonerDisco = [ (rutadevbox) , "storageattach", str(nombremaquina), "--storagectl", str(controladornombre), "--port", str(portdisco) , "--device", str(devicedisco) , "--type", str(tipoDeDisco), "--medium", str(rutadiscovm)]

    comandovboxPonerISO = [ (rutadevbox) , "storageattach", str(nombremaquina),  "--storagectl", str(controladornombreISO), "--port", str(portISO) , "--device", str(devISO) , "--type", str(typeISO), "--medium", str(caminoarchivo)]
    

    # Si el archivo (event.file en el código) que ha producido el evento (ser creado) termina en ISO se hace lo siguiente:
    if nombrearchivo.endswith(".iso"):

        print("un archivo ISO se ha añadido a la carpeta")

    # además de esto, llamará a una función que ejecutará el .exe de vboxmanage
        subprocess.call(f"where {rutadevbox}") 
        # además de estas dos cosas, llamará a una función que cuando se le llame, le de la información de las variables al VMware
        
        subprocess.check_output(comandovbox)

        print(f"se ha creado la Máquina virtual con el nombre  {str(nombremaquina)} y el sistema operativo de tipo {str(sistemaoperativo)}")

        subprocess.check_output(comandovboxMemoria)

        print(f"se ha asignado {int(ramMB)} MB de RAM a la máquina virtual {str(nombremaquina)}")

        subprocess.check_output(comandovboxCrearDisco)

        print(f"se ha creado el disco virtual con el nombre  {str(nombreDeDiscoVM)} que tiene {int(discoGB)} GB de almacenamiento")

        subprocess.check_output(comandovboxCrearControlador)

        print(f"se ha creado un controlador de disco  {str(controladortipo)}")

        subprocess.check_output(comandovboxCrearControladorISO)

        print(f"se ha creado un controlador de disco  {str(controladortipoISO)}")

        subprocess.check_output(comandovboxPonerDisco)

        print(f"Se ha asignado el disco {str(nombreDeDiscoVM)} a la máquina virtual {str(nombremaquina)}")

        subprocess.check_output(comandovboxPonerISO)

        print(f"se ha asignado la ISO {str(nombrearchivo)} a la VM {str(nombremaquina)}" )



    # Si todos los procesos se completan, se imprime esto

        print("¡La VM se ha creado correctamente!")

            
        

    else : 
    
        print("se ha creado un archivo pero no es un archivo .iso, VMware no será ejecutado ") 

    # Si se detecta un archivo pero no es ISO entonces se comunicará que VMware no puede ejecutarlo porque no es un ISO
    





# configurando el gestor de eventos del sistema de archivos
if __name__ == "__main__" :

    event_handler= FileSystemEventHandler()
    event_handler.on_created = al_crear_archivo

# Estableciendo la ruta en la que tiene que registrar los cambios (ERROR)
    path = "C:/ISOS/VMS"

# Configurando cuando encender el observer y que debe de observar, recursive indica si debe de monitorear las carpetas dentro de esa carpeta o no, no hace falta en este caso
    observer = Observer()
    observer.schedule(event_handler,path,recursive=False)
    observer.start()

# Si el script funciona, se muestra en la consola que funciona
    try:
        print("Script monitoreando, para apagarlo pulsa CTRL + C")
        while True:
            time.sleep(1)

#  Si se interrumpe el script con el teclado pulsando CTRL + C se muestra en la consola que  se ha interrumpido
    except KeyboardInterrupt:
        print("CTRL + C pulsado, el script ha sido interrumpido")
        observer.stop()



  