import socket
import re
from telethon import TelegramClient
from telethon import events
from wakeonlan import send_magic_packet
import datosbot 
import tracemalloc 

tracemalloc.start()

client = TelegramClient(datosbot.bot_token, datosbot.api_id, datosbot.api_hash).start(bot_token=datosbot.bot_token)
WOLPowerswitchBot= TelegramClient(datosbot.bot_token, datosbot.api_id, datosbot.api_hash)

"""
Creando un diccionario de python para guardar la info de todos los ordenadores, 
similar a un array en java. Solo que esto permite guardar variables dentro de ellas mientras que las arrays solo valores

Dentro de este diccionario se encuentran dos "keys" que son direccionip y mac, son similares a las variables en java

"""



ordenadoresparaboot = { 

    1: {"direccionip" : "123.123.123.123", "mac": "9UG:4HNG:UN3:4N9F:UFUN9"},

    2: {"direccionip" : "123.123.123.123", "mac": "9UG:4HNG:UN3:4N9F:UFUN9"},

    3: {"direccionip" : "123.123.123.123", "mac": "9UG:4HNG:UN3:4N9F:UFUN9"},

    4: {"direccionip" : "123.123.123.123", "mac": "9UG:4HNG:UN3:4N9F:UFUN9"} 
                        
                                                                   
} 

# Se crea un proceso que controla todo el envío del paquete WOL

async def enviarwol(event):

    # el try controla el proceso de enviar el paquete correctamente
    try: 

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', 9))
        magic_packet = b'\xFF' * 6 + bytes.fromhex(ordenadoresparaboot["mac"].replace(':' ''))


        # enviando el magic packet a la dirección IP por el puerto 9
        sock.sendto(magic_packet, (ordenadoresparaboot["direccionip"], 9))

        client.send_message(event, 'El paquete se ha enviado al ordenador {num_pc}')
        

    # el except controla todos los resultados que no tienen que ver con el recurso

    except Exception as e:
        await client.send_message(event, 'Error, el paquete no se ha enviado al ordenador {num_pc}')
        

    # el finally controla todas las cosas que se hacen se complete el proceso o no
        
    finally:
        
        sock.close()
        await client.disconnect()



client.start()

@client.on(events.NewMessage(chats= datosbot.chat_name, pattern=r'/start'))
async def gestionar_comando_start(event):
  
 await client.send_message(event, 'Selecciona el ordenador a encender')



@client.on(events.NewMessage(pattern=r'/encenderpc(/d)'))
async def como_gestionar_comando(event, client ,num_pc) :


    # la r quiere decir raw, para que el programa interprete las barras (/) como simplemente texto "crudo"

        if re.match(r"/ encenderpc(/d)", client(events.NewMessage(pattern=r'/encenderpc(/d)')) ):

            num_pc = int(client(events.NewMessage(pattern=r'/encenderpc(/d)')) )

    
    # Si el número del comando es 1, se coge la información con el número 1 en el diccionario y llama a la función papasfritas
        if num_pc == 1 :
            ordenadoresparaboot[1] ; enviarwol(client, num_pc)

        
        
        

    # Si el número del comando es 2, se coge la información con el número 2 en el diccionario y llama a la función papasfritas
        if num_pc == 2 :
            ordenadoresparaboot[2] ; enviarwol(client, num_pc)

        

    # Si el número del comando es 3, se coge la información con el número 3 en el diccionario y llama a la función papasfritas
        if    num_pc == 3 :
            ordenadoresparaboot[3] ; enviarwol(client, num_pc)

        


    # Si el número del comando es 4, se coge la información con el número 4 en el diccionario y llama a la función papasfritas
        if num_pc == 4 :
            ordenadoresparaboot[4] ; enviarwol(client, num_pc)

    # Si el número del comando es otra cosa, se envía el mensaje de error y no llama a la función papasfritas
        else : 

            WOLPowerswitchBot.send_message(event, 'Error, el numero de pc puesto no es valido, ponga un numero del 1 al 4')






client.run_until_disconnected()





