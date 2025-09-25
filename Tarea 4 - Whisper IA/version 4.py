import numpy
import transformers
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq, WhisperProcessor, WhisperForConditionalGeneration
import torch
import safetensors.torch
import os
import librosa
import ffmpeg
import subprocess
import json

# Cargar las configuraciones desde el JSON
with open("config.json", "r") as f:
    config = json.load(f)

device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

directorio_actual = os.path.abspath(os.path.dirname(__file__))
os.chdir(str(directorio_actual))

nombre_usuario_windows = "Carlos"  # Ya no es necesario
directorio_modelo = config["model_directory"]
if os.path.exists(directorio_modelo):
    print(f"La ubicación del modelo existe! Accediendo al directorio actual...")
else:
    print(f"La ubicación del modelo que se ha puesto no existe, échale un vistazo ---> {directorio_modelo}")

print(f"Se está ejecutando el script desde --> {directorio_actual}")

model_id = "openai/whisper-large-v3"

if directorio_actual:
    archivos_en_directorio = os.listdir(directorio_actual)
    archivos_a_elegir = [file for file in archivos_en_directorio if str(file).endswith((".wav", ".mp3", "mp4"))]

    print(f"Mostrando archivos válidos para ejecución con whisper {archivos_a_elegir}")

    archivo_seleccionado = input("Escribe el nombre del archivo a ejecutar \n ---> ")

    print(f"Has seleccionado el archivo {archivo_seleccionado}")

    camino_al_audio = os.path.join(directorio_actual, archivo_seleccionado)

    print(f"Se está cogiendo el archivo de audio desde aquí --> {camino_al_audio}")

    if os.path.exists(camino_al_audio):
        print("La dirección al archivo de audio es correcta! Se cargará el modelo")
        processor = WhisperProcessor.from_pretrained(directorio_modelo)

        model = WhisperForConditionalGeneration.from_pretrained(directorio_modelo, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True)
        direccion_ffmpeg = config["ffmpeg_directory"]
        if processor and model:
            print("El modelo se ha cargado")

            input_file = archivo_seleccionado
            output_file = f"16ksr_{archivo_seleccionado}"
            camino_al_audio_nuevo = os.path.join(directorio_actual, output_file)
            camino_al_audio_nuevo_str = str(camino_al_audio_nuevo)
            new_sample_rate = config["output_sample_rate"]

            ffmpeg_command = [direccion_ffmpeg, "-i", input_file, "-ar", str(new_sample_rate), output_file]

            segundos_por_segmento = config["chunk_seconds"]
            nombre_carpeta_segmentos = config["output_directory"]
            nombre_para_archivos = f"trozo_num_%03d_{archivo_seleccionado}"
            nombre_segmento_dir = f"\\{nombre_para_archivos}"
            direccion_chunks_sin_nombre = str(directorio_actual + "\\" + nombre_carpeta_segmentos)
            if not os.path.exists(direccion_chunks_sin_nombre):
                os.makedirs(direccion_chunks_sin_nombre)

            direccion_chunks_completa = str(direccion_chunks_sin_nombre + nombre_segmento_dir)
            print(direccion_chunks_completa, "---> dirección de los chunks")

            ffmpeg_command_gen_chunks = [direccion_ffmpeg, "-i", str(camino_al_audio_nuevo), "-f", "segment", "-segment_time", str(segundos_por_segmento), "-c", "copy", direccion_chunks_completa]

            subprocess.run(ffmpeg_command)
            subprocess.run(ffmpeg_command_gen_chunks)

            print(f"Archivo con la sample rate necesaria para procesamiento del modelo creado en {camino_al_audio_nuevo_str}")
            print(f"Se han creado segmentos de {segundos_por_segmento} segundos cada uno del archivo {output_file} y se han almacenado aquí ---> {direccion_chunks_completa}")

            if os.path.exists(camino_al_audio_nuevo):
                os.remove(camino_al_audio_nuevo)
                print(f"Se ha borrado el archivo en {camino_al_audio_nuevo} puesto que ya no es necesario a partir de aquí")

                if os.path.exists(direccion_chunks_sin_nombre):
                    print("El camino a los trozos del audio existe! cargando los trozos con librosa...")

                    segmentos = sorted(os.listdir(direccion_chunks_sin_nombre))
                    print(f"Se han detectado estos segmentos --> {segmentos}")

                    nombre_archivo_generado = config["text_output_file"].format(audio_file=archivo_seleccionado)
                    with open(nombre_archivo_generado, "w") as archivo:
                        for segmento in segmentos:
                            fragmento_path = os.path.join(direccion_chunks_sin_nombre, segmento)
                            audio_chunk, _ = librosa.load(fragmento_path, sr=16000)
                            print("Transcribiendo fragmento de audio a texto...")

                            dialogo_detectado = processor(audio_chunk, sampling_rate=16000, return_tensors="pt").input_features

                            with torch.no_grad():
                                dialogo_generado = model.generate(dialogo_detectado)
                                salida_de_generacion = processor.batch_decode((dialogo_generado), skip_special_tokens=True)[0]

                                salida_completa = str("")
                                salida_completa += salida_de_generacion + " "

                                salida_completa_limpia = salida_completa.strip()
                                salida_completa_limpia_str = str(salida_completa_limpia).replace(".", "\n")

                                if salida_completa_limpia:
                                    print("Fragmento procesado correctamente! tiene", len(salida_completa_limpia_str), "caracteres de longitud")
                                    print(f"Fragmento escrito en {nombre_archivo_generado}")
                                    archivo.write(salida_completa_limpia_str)
                                else:
                                    print("No hay salida de generación...")

                else:
                    print(f"El camino al archivo de audio de 16000 sr, {output_file} no existe, compruébalo --> {camino_al_audio_nuevo_str}")

        else:
            print("El modelo no se ha cargado")

    else:
        print(f"La dirección del archivo de audio es incorrecta, échale un vistazo: {camino_al_audio}")
