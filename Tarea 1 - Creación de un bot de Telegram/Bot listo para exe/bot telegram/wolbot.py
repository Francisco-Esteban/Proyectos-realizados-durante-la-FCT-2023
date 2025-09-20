
import re
import telebot
import json
import datosbot
import re
import os
import scapy
from scapy.all import sendp
from scapy.layers.l2 import Ether


cwd = os.path.dirname(__file__)
os.chdir(cwd)

print("Corriendo script desde ---> " + os.getcwd())  

camino = os.path.join(cwd, "direccionesMAC.json")

if os.path.exists(camino) == True :

    print(f"El camino hacia la configuración existe, es este: {camino}")

else: print("El camino hacia la configuración no existe")   


with open(camino, "r" ) as file:


        dict = json.loads(file.read())

        n1 = dict["n1"]
        n2 = dict["n2"]
        n3 = dict["n3"]
        n4 = dict["n4"]
        n5 = dict["n5"]
        n6 = dict["n6"]



# Se crea un proceso que controla todo el envío del paquete WOL





# Aquí comienzan los comandos del bot y su configuración con la hoja de datos

bot= telebot.TeleBot(datosbot.token)

@bot.message_handler(commands=["start"])

def mensajedeentrada(message):

    bot.reply_to(message, "Seleccione un ordenador para encender")


    




@bot.message_handler(commands=["help"])
def mensajedeayuda(message):
    bot.reply_to(message, 
                  "El bot usa los siguientes comandos: \n \n " 

                  "/start --> inicia comunicación con el bot \n \n"

                  "/help ---> muestra todos los comandos \n \n"

                  "/datospc + num de pc  --> muestra los datos de un pc  \n \n"

                  "/encenderpc + num de pc --> enciende el pc indicado con el número \n \n"
                  
                  )
     
    



@bot.message_handler(commands=[r"datospc"])
def obtenerdatospc(message):
    
    match = re.search(r"/datospc (\d+)", message.text)
    if match :
    
        numeropc = match.group(1)
        print(f"El numero del PC es {numeropc}")
        if numeropc:
            variable = "n" + str(numeropc)
            infopc = dict.get(variable)
            infopclimpisima = str(infopc).replace("'", "").replace("{", "").replace(":", " - ").replace("}", "")
            print(f"La info del PC es {str(infopclimpisima)}")

            if infopclimpisima != "None" :
                print("la condicion no funciona")
                bot.reply_to(message, "El ordenador seleccionado tiene la siguiente dirección MAC \n \n ---> " + str(infopclimpisima) + " \n \n Si desea encenderlo, use el comando /encenderpc + un número del 1 al 6")

            if infopclimpisima == "None" :
                print("la condicion funciona")
                bot.reply_to(message, "pruebe otra vez con un valor distinto")


        if 1< int(numeropc) >6 :  bot.reply_to(message, "El número debe de ser solamente del 1 al 6")
        
        
    else: bot.reply_to(message, "Hay que poner un número junto al comando /datospc separado de un espacio, no solamente texto o un numero puesto sin espacio \n \n --> ejemplo correcto: /datospc 1")
        
            









@bot.message_handler(commands=[r"encenderpc"]) 
 
def enviarwol(message):

    # el proceso de enviar el paquete correctamente
        match = re.match(r"/encenderpc (\d+)", message.text)
        if match :
              
            numeropcWOL = match.group(1)
            print(f"El numero del PC es {numeropcWOL}")
            variable = "n" + str(numeropcWOL)
            

            bot.reply_to(message, "Se hará un encendido del ordenador número " + str(numeropcWOL) )
        mac_sin_puntos = dict.get(variable).replace( ":", "").replace("-", "")
        mac_en_bytes = bytes.fromhex(mac_sin_puntos)
        

        if mac_en_bytes:

            bot.reply_to(message, "Transformando la" + str(mac_sin_puntos) + "en bytes...")

        else: bot.reply_to(message, "no se ha podido transformar la MAC" + str(mac_sin_puntos) + "en bytes...")

    # El contenido de este paquete es el número 255 repetido 6 veces para hacer que la tarjeta de red preste atención más la MAC en bytes repetida 16 veces
    # Esto es como escribir el contenido de una carta
        
        contenido_de_paquete_WOL = b"\xFF" * 6 +  mac_en_bytes * 16

        if contenido_de_paquete_WOL: 
             bot.reply_to(message, "contenido del paquete creado")

        else: 
             bot.reply_to(message, "No se ha podido crear el contenido del paquete")

            
    # El destinatario de este paquete es una dirección que tiene todos los valores al máximo (255) o también conocida como la dirección de broadcast, ahora estamos indicando la dirección de la carta
    #  es como ponerle el sello de destinatario a la carta que hemos creado

        paquete_WOL = Ether(dst = "ff:ff:ff:ff:ff:ff") / contenido_de_paquete_WOL

        if paquete_WOL:
             
                bot.reply_to(message, "Estableciendo destinatario del paquete...")

        else:
                bot.reply_to(message, "No se ha establecido el destinatario del paquete")

    # Este paso será enviar el paquete a la dirección de broadcast, es importante poner el nombre del ordenador que se quiere encender

        sendp(paquete_WOL, "Wi-Fi")
        bot.reply_to(message, "Se ha enviado el paquete WOL al PC número" + str(numeropcWOL) )
        


    


# El bot siempre procesará los comandos según el código y si el bot encuentra un error, evitará apagarse y se reiniciará.

if __name__ == "__main__":
        bot.polling(none_stop =True)

       