
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
nombremaquina= "maq2u2inecavs1eir25tualr2eal2"
sistemaoperativo= "Linux"
nombreDeDiscoVM= "di22s15c2sers2eo4322.vdi"
tipoDeDisco = "dvd"
formatoDisco = "VDI"
portdisco = 0
devicedisco = 0
controladornombre= "sata"
controladortipo= "sata"


# Los comandos para crear la máquina y configurarla

# Esta función define lo que se hará al crear un archivo en la carpeta MV dentro de ISOS, crear el archivo sería pegar una ISO en la carpeta

# En este caso he hecho que el script comunique que una ISO se ha detectado.

    
def al_crear_archivo(event):



    rutadevbox = "C:/Program Files/Oracle/VirtualBox/VBoxManage.exe"
    nombrearchivo = os.path.basename(event.src_path)
    caminoarchivo = event.src_path

    comandovbox = [ (rutadevbox) , "createvm", "--name", str(nombremaquina), "--ostype", str(sistemaoperativo), "--register"]
    comandovboxMemoria = [(rutadevbox) , "modifyvm", str(nombremaquina), "--memory", str(ramMB) ]
    comandovboxCrearDisco = [ (rutadevbox) , "createhd", "--filename", str(nombreDeDiscoVM), "--size", str(discoGB), "--format", str(formatoDisco)]
    comandovboxCrearControlador= [ (rutadevbox),"storagectl", str(nombremaquina), "--name", str(controladornombre), "--add", str(controladornombre), "--controller", str(controladortipo)]
    comandovboxPonerDisco = [ (rutadevbox) , "storageattach", str(nombremaquina), "--storagectl", str(controladornombre), "--port", str(portdisco) , "--device", str(devicedisco) , "--type", str(tipoDeDisco), "--medium", "cdrom", str(caminoarchivo)]

    # Si el archivo (event.file en el código) que ha producido el evento (ser creado) termina en ISO se hace lo siguiente:
    if nombrearchivo.endswith(".iso"):

        print("un archivo ISO se ha añadido a la carpeta")

    # además de esto, llamará a una función que ejecutará el .exe de vboxmanage
        subprocess.call(f"where {rutadevbox}") 
        # además de estas dos cosas, llamará a una función que cuando se le llame, le de la información de las variables al VMware
        
        subprocess.check_output(comandovbox)

        subprocess.check_output(comandovboxMemoria)

        subprocess.check_output(comandovboxCrearDisco)

        subprocess.check_output(comandovboxCrearControlador)

        subprocess.check_output(comandovboxPonerDisco)

            
        

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



  