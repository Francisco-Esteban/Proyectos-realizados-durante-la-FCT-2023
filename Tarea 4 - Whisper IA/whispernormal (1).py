import numpy
import transformers
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq, WhisperProcessor, WhisperForConditionalGeneration
import torch
import safetensors.torch
import os
import librosa
import ffmpeg
import subprocess

device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

directorio_actual = os.path.abspath(os.path.dirname(__file__))
os.chdir(str(directorio_actual))

nombre_usuario_windows = "Carlos"
directorio_modelo = f"C:/Users/{nombre_usuario_windows}/.cache/huggingface/hub/models--openai--whisper-large-v3/snapshots/1ecca609f9a5ae2cd97a576a9725bc714c022a93"
if directorio_modelo is True :
    print(f"La ubicación del modelo existe! Accediendo al directorio actual...")

else: 
    print(f"La ubicación del modelo que se ha puesto no existe, echale un vistazo ---> {directorio_modelo}")

print(f"Se está ejecutando el script desde --> {directorio_actual}")


model_id = "openai/whisper-large-v3"

if directorio_actual : True

archivos_en_directorio = os.listdir(directorio_actual)
archivos_a_elegir = [ file for file in archivos_en_directorio  if str(file).endswith((".wav", ".mp3", "mp4")) ]


print(f"Mostrando archivos válidos para ejecución con whisper {archivos_a_elegir}")

archivo_seleccionado = input("Escribe el nombre del archivo a ejecutar \n ---> ")

print(f"has seleccionado el archivo {archivo_seleccionado}")

camino_al_audio = os.path.join(directorio_actual, archivo_seleccionado)

print(f"se está cogiendo el archivo de audio desde aquí --> {camino_al_audio}")




if camino_al_audio :
    print("La dirección al archivo de audio es correcta! Se cargará el modelo")
    processor = WhisperProcessor.from_pretrained(directorio_modelo)

    model = WhisperForConditionalGeneration.from_pretrained(directorio_modelo,torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True)
    direccion_ffmpeg = "C:/Users/Carlos/Desktop/whisper/ffmpeg/app/bin/ffmpeg.exe"
    if processor and model :
        print("El modelo se ha cargado")
       
        input_file = archivo_seleccionado
        output_file = f"16ksr{archivo_seleccionado}"
        camino_al_audio_nuevo = os.path.join(directorio_actual, output_file)
        camino_al_audio_nuevo_str = str(camino_al_audio_nuevo)
        new_sample_rate = 16000


        ffmpeg_command = [direccion_ffmpeg, "-i", input_file, "-ar", str(new_sample_rate), output_file]


        subprocess.run(ffmpeg_command)

        print(f"archivo con la sample rate necesaria para procesamiento del modelo creado en {camino_al_audio_nuevo_str}")
        if os.path.exists(camino_al_audio_nuevo_str) :

            print("El camino al archivo nuevo existe! cargando el archivo con librosa...")

            audio, rate = librosa.load(camino_al_audio_nuevo_str, sr=16000)

            entrada_para_generacion = processor(audio, sampling_rate= 16000, return_tensors= "pt" ).input_features
            print(entrada_para_generacion.shape)

            generacion_config = {
            "max_length": 9999,  
            "num_beams": 5,
            }

            with torch.no_grad():
                dialogo_detectado = model.generate(entrada_para_generacion, **generacion_config)

                #Comprueba que el tensor (como una especie de lista) de pytorch no esté vacío
                if dialogo_detectado.numel() >0: 
                    print("Se ha detectado dialogo para ser procesado, ahora generando texto basandose en este...")
                
                else: print("no se ha detectado un dialogo con el que generar texto aunque sí se ha detectado el archivo de audio")

                #Se decodifica la salida de generacioni la salida de generación existe, imprime cuando mide en caracteres + la salida + pasa la salida a un txt nuevo con el nombre de abajo

                salida_de_generacion = processor.batch_decode(dialogo_detectado, skip_special_tokens = True)
                salida_de_generacion_str = str(salida_de_generacion[0])
                nombre_archivo_generado = f"texto_de_{archivo_seleccionado}"


                if salida_de_generacion :
                    print("La salida del texto tiene la longitud de", len(salida_de_generacion_str), "caracteres")
                    print(salida_de_generacion_str)

                    with open(nombre_archivo_generado, "w") as archivo:
                        archivo.write(salida_de_generacion_str)

                else: 
                    print("No hay salida de generación...")
        else :
            print(f"El camino al archivo de audio nuevo {output_file} no existe, compruebalo --> {camino_al_audio_nuevo_str}")
        

    else: print("El modelo no se ha cargado")




else: 
    print(f"la direccion del  del archivo de audio es incorrecta, echale un vistazo: {camino_al_audio}")





