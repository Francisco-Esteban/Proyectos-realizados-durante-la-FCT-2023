
import os
import watchdog
import time
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import subprocess


# Aquí se harán unas variables en las que se ponen los parámetros que pide la VM
# estas variables se usarán para hacer un comando con ellas que el script pondrá automáticamente en la consola de VMware tras abrirlo automáticamente son subprocess.call
ram = 4
disco = 50
nombremaquina= "test"
sistemaoperativo= "Linux"
memoriaenmb= "200 MB"
archivodisco= "disco8.vdi"
tamañodisco= "50 GB"
formato= "VDI"
puerto= "0"
dispositivo= "0"
dispositivoalmacenamiento= "dvd"
rutaiso="C:/ISOS/VMS"


# Esta función define lo que se hará al crear un archivo en la carpeta MV dentro de ISOS, crear el archivo sería pegar una ISO en la carpeta

# En este caso he hecho que el script comunique que una ISO se ha detectado.

    
def al_crear_archivo(event):


    rutadevmplayer = "C:/vmplayer.exe"
    nombrearchivo = os.path.basename(event.src_path)


    # Si el archivo (event.file en el código) que ha producido el evento (ser creado) termina en ISO se hace lo siguiente:
    if os.path.basename(event.src_path).endswith(".iso"):

        print("un archivo ISO se ha añadido a la carpeta")

    # además de esto, llamará a una función que ejecutará el .exe de VMware
        subprocess.call(f"where {rutadevmplayer}") 

        # además de estas dos cosas, llamará a una función que cuando se le llame, le de la información de las variables al VMware
        comandoVMware= ["C:/Program Files/Oracle/VBoxManage.exe", "createvm", "--name", str(nombremaquina), "--ostype", str(sistemaoperativo), "--register", "--cdrom", str(rutaiso)]
        subprocess.call(comandoVMware)
        
        comandoVMware2= ["C:/Program Files/Oracle/VBoxManage.exe", "modifyvm", str(nombremaquina), "--memory", str(memoriaenmb)]
        subprocess.call(comandoVMware2)

        comandoVMware3= ["C:/Program Files/Oracle/VBoxManage.exe", "createhd", "--filename", str(archivodisco), "--size", str(tamañodisco), "--format", str(formato)]
        subprocess.call(comandoVMware3)

        comandoVMware4= ["C:/Program Files/Oracle/VBoxManage.exe", "storageattach", str(nombremaquina), "--storagectl", str(nombremaquina), "--port", str(puerto), "--device", str(dispositivo), "--type", str(dispositivoalmacenamiento), "--medium cdrom", str(rutaiso)]
        subprocess.call(comandoVMware4)

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



  