
# Primer comando del bot. /start

import telebot
import datosbot



bot = telebot.TeleBot("6783665959:AAFaMFFA6OshH5uy0iBjyBTfudgef8btrhQ")


@bot.command(commands=["/start"])
def start(mensaje):
    bot.reply_to(mensaje, "¡Hola! Soy un bot destinado a realizar Wake On LAN")
bot.polling()




# Segundo comando del bot. /encenderpc


import wakeonlan
from wakeonlan import send_magic_packet 


ordenadoresparaboot = { 

    1: {"direccionip" : "123.123.123.123", "mac": "9UG:4HNG:UN3:4N9F:UFUN9"},

    2: {"direccionip" : "123.123.123.123", "mac": "9UG:4HNG:UN3:4N9F:UFUN9"},

    3: {"direccionip" : "123.123.123.123", "mac": "9UG:4HNG:UN3:4N9F:UFUN9"},

    4: {"direccionip" : "123.123.123.123", "mac": "9UG:4HNG:UN3:4N9F:UFUN9"} 
                        
                                                                   
} 


  

