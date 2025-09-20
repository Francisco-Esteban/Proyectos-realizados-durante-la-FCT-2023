
import telebot

import datosbot
import re
import scapy
from scapy.all import sendp
from scapy.layers.l2 import Ether


ordenadoresparaboot = { 

    1: {"direccionip" : "123.123.123.123", "mac": "9UG:4HNG:UN3:4N9F:UFUN9"},

    2: {"direccionip" : "123.123.123.123", "mac": "9UG:4HNG:UN3:4N9F:UFUN9"},

    3: {"direccionip" : "123.123.123.123", "mac": "9UG:4HNG:UN3:4N9F:UFUN9"},

    4: {"direccionip" : "123.123.123.123", "mac": "9UG:4HNG:UN3:4N9F:UFUN9"} 
                        
                                                                   
} 

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
     
    



@bot.message_handler(commands=["datospc(d+)"])
def obtenerdatospc(message, numeropc, infopc):
    
    match = re.match(r"datospc(d+)", message.text) 
    if match :
    
        numeropc = match.group(1)

        if numeropc :
            
            infopc = ordenadoresparaboot.get(numeropc)

            bot.reply_to(message, "El Ordenador número " + str(numeropc) + " Tiene los siguientes datos " + str(infopc), "Si desea encenderlo, use el comando encenderpc + número del ordenador a encender")

        else:
             bot.reply_to(message, "No se ha podido obtener la información del ordenador seleccionado ")

        






    @bot.message_handler(commands=["encenderpc(d+)"]) 
    def enviarwol(message, mac_sin_puntos, mac_en_bytes, paquete_WOL, contenido_de_paquete_WOL):

    # el proceso de enviar el paquete correctamente

        mac_sin_puntos=  ordenadoresparaboot["mac"].replace( ":", " ")
        mac_en_bytes = bytes.fromhex(mac_sin_puntos)

        if mac_en_bytes:

            bot.reply_to(message, "Transformando la" + str(mac_sin_puntos) + "en bytes...")

        else: 
        
            bot.reply_to(message, "no se ha podido transformar la MAC" + str(mac_sin_puntos) + "en bytes...")

    # El contenido de este paquete es el número 255 repetido 6 veces para hacer que la tarjeta de red preste atención más la MAC en bytes repetida 16 veces
    # Esto es como escribir el contenido de una carta
        
        contenido_de_paquete_WOL = b"\xFF" * 6 + mac_en_bytes * 16

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
        bot.reply_to(message, "Se ha enviado el paquete WOL al PC número" + str(numeropc) )
        


    obtenerdatospc(message, numeropc, infopc)
    bot.reply_to(message, "Se hará un encendido del ordenador" + str(numeropc) )
    


# El bot siempre procesará los comandos según el código y si el bot encuentra un error, evitará apagarse y se reiniciará.

if __name__ == "__main__":
        bot.polling(none_stop =True)