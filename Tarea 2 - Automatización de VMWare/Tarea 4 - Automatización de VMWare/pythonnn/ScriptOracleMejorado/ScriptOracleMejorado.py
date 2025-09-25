
import os
import watchdog
import time
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import subprocess
import json


cwd = os.path.dirname(__file__)
os.chdir(cwd)

print("Corriendo script desde ---> " + os.getcwd())  

camino = os.path.join(cwd, "configdeVM.json")

if os.path.exists(camino) == True :

    print(f"El camino hacia la configuración existe, es este: {camino}")

else: print("El camino hacia la configuración no existe")   


with open(camino, "r" ) as file:


        data = json.loads(file.read())

        

        ramMB = data.get("ramMB")


        discoGB = data.get("discoGB")


        nombremaquina = data.get("nombremaquina")

        sistemaoperativo= data.get("sistemaoperativo")

        nombreDeDiscoVM= data.get("nombreDeDiscoVM")

        tipoDeDisco = data.get("tipoDeDisco")

        formatoDisco = data.get("formatoDisco")

        portdisco = data.get("portdisco")

        devicedisco = data.get("devicedisco")

        controladornombre= data.get("controladornombre")

        controladortipo= data.get("controladortipo")

        chipset= data.get("chipset")

        controladornombreISO= data.get("controladornombreISO")

        controladortipoISO  = data.get("controladortipoISO")

        chipsetISO = data.get("chipsetISO")

        portISO = data.get("portISO")

        devISO = data.get("devISO")

        typeISO = data.get("typeISO")

        rutadiscovm = data.get("rutadiscovm")

        rutadevbox = data.get("rutadevbox")

        print("Esta es la ruta donde está el vbox manage: ", rutadevbox)


    
def al_crear_archivo(event):



    nombrearchivo = os.path.basename(event.src_path)
    caminoarchivo = event.src_path

    comandovbox = [ str(rutadevbox) , "createvm", "--name", str(nombremaquina), "--ostype", str(sistemaoperativo), "--register"]

    comandovboxMemoria = [str(rutadevbox) , "modifyvm", str(nombremaquina), "--memory", str(ramMB) ]

    comandovboxCrearDisco = [ str(rutadevbox) , "createhd", "--filename", str(nombreDeDiscoVM), "--size", str(discoGB), "--format", str(formatoDisco)]

    comandovboxCrearControlador= [ str(rutadevbox),"storagectl", str(nombremaquina), "--add", str(controladortipo), "--name", str(controladornombre)] 

    comandovboxCrearControladorISO= [ str(rutadevbox), "storagectl", str(nombremaquina), "--add", str(controladortipoISO), "--name", str(controladornombreISO)]

    comandovboxPonerDisco = [ str(rutadevbox) , "storageattach", str(nombremaquina), "--storagectl", str(controladornombre), "--port", str(portdisco) , "--device", str(devicedisco) , "--type", str(tipoDeDisco), "--medium", str(rutadiscovm) + str(nombreDeDiscoVM)]

    comandovboxPonerISO = [ str(rutadevbox) , "storageattach", str(nombremaquina),  "--storagectl", str(controladornombreISO), "--port", str(portISO) , "--device", str(devISO) , "--type", str(typeISO), "--medium", str(caminoarchivo)]
    
    comandoencender = [ str(rutadevbox), "startvm", str(nombremaquina) ]

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

        subprocess.check_output(comandoencender)

        print(f"Se está encendiendo la máquina virtual llamada {str(nombremaquina)}" )

            
        

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



  