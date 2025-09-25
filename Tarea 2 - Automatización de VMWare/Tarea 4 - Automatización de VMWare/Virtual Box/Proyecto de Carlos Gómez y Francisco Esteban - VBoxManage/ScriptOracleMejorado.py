
import os
import watchdog
import time
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import subprocess
import configdeVM


# Aquí se harán unas variables en las que se ponen los parámetros que pide la VM
# estas variables se usarán para hacer un comando con ellas que el script pondrá automáticamente en la consola de Vbox tras abrirlo automáticamente son subprocess.call



# Los comandos para crear la máquina y configurarla

# Esta función define lo que se hará al crear un archivo en la carpeta MV dentro de ISOS, crear el archivo sería pegar una ISO en la carpeta

# En este caso he hecho que el script comunique que una ISO se ha detectado.

    
def al_crear_archivo(event):



    nombrearchivo = os.path.basename(event.src_path)
    caminoarchivo = event.src_path

    comandovbox = [ (configdeVM.rutadevbox) , "createvm", "--name", str(configdeVM.nombremaquina), "--ostype", str(configdeVM.sistemaoperativo), "--register"]

    comandovboxMemoria = [(configdeVM.rutadevbox) , "modifyvm", str(configdeVM.nombremaquina), "--memory", str(configdeVM.ramMB) ]

    comandovboxCrearDisco = [ (configdeVM.rutadevbox) , "createhd", "--filename", str(configdeVM.nombreDeDiscoVM), "--size", str(configdeVM.discoGB), "--format", str(configdeVM.formatoDisco)]

    comandovboxCrearControlador= [ (configdeVM.rutadevbox),"storagectl", str(configdeVM.nombremaquina), "--add", str(configdeVM.controladortipo), "--name", str(configdeVM.controladornombre)] 

    comandovboxCrearControladorISO= [ (configdeVM.rutadevbox), "storagectl", str(configdeVM.nombremaquina), "--add", str(configdeVM.controladortipoISO), "--name", str(configdeVM.controladornombreISO)]

    comandovboxPonerDisco = [ (configdeVM.rutadevbox) , "storageattach", str(configdeVM.nombremaquina), "--storagectl", str(configdeVM.controladornombre), "--port", str(configdeVM.portdisco) , "--device", str(configdeVM.devicedisco) , "--type", str(configdeVM.tipoDeDisco), "--medium", str(configdeVM.rutadiscovm)]

    comandovboxPonerISO = [ (configdeVM.rutadevbox) , "storageattach", str(configdeVM.nombremaquina),  "--storagectl", str(configdeVM.controladornombreISO), "--port", str(configdeVM.portISO) , "--device", str(configdeVM.devISO) , "--type", str(configdeVM.typeISO), "--medium", str(caminoarchivo)]
    
    comandoencender = [ (configdeVM.rutadevbox), "startvm", str(configdeVM.nombremaquina) ]

    # Si el archivo (event.file en el código) que ha producido el evento (ser creado) termina en ISO se hace lo siguiente:
    if nombrearchivo.endswith(".iso"):

        print("un archivo ISO se ha añadido a la carpeta")

    # además de esto, llamará a una función que ejecutará el .exe de vboxmanage
        subprocess.call(f"where {configdeVM.rutadevbox}") 
        # además de estas dos cosas, llamará a una función que cuando se le llame, le de la información de las variables al VMware
        
        subprocess.check_output(comandovbox)

        print(f"se ha creado la Máquina virtual con el nombre  {str(configdeVM.nombremaquina)} y el sistema operativo de tipo {str(configdeVM.sistemaoperativo)}")

        subprocess.check_output(comandovboxMemoria)

        print(f"se ha asignado {int(configdeVM.ramMB)} MB de RAM a la máquina virtual {str(configdeVM.nombremaquina)}")

        subprocess.check_output(comandovboxCrearDisco)

        print(f"se ha creado el disco virtual con el nombre  {str(configdeVM.nombreDeDiscoVM)} que tiene {int(configdeVM.discoGB)} GB de almacenamiento")

        subprocess.check_output(comandovboxCrearControlador)

        print(f"se ha creado un controlador de disco  {str(configdeVM.controladortipo)}")

        subprocess.check_output(comandovboxCrearControladorISO)

        print(f"se ha creado un controlador de disco  {str(configdeVM.controladortipoISO)}")

        subprocess.check_output(comandovboxPonerDisco)

        print(f"Se ha asignado el disco {str(configdeVM.nombreDeDiscoVM)} a la máquina virtual {str(configdeVM.nombremaquina)}")

        subprocess.check_output(comandovboxPonerISO)

        print(f"se ha asignado la ISO {str(nombrearchivo)} a la VM {str(configdeVM.nombremaquina)}" )



    # Si todos los procesos se completan, se imprime esto

        print("¡La VM se ha creado correctamente!")

        subprocess.check_output(comandoencender)

        print(f"Se está encendiendo la máquina virtual llamada {str(configdeVM.nombremaquina)}" )

            
        

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



  