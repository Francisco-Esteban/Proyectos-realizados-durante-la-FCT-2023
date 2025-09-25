import numpy as np
import torch
import os
import librosa
import subprocess
from pydub import AudioSegment
from transformers import WhisperProcessor, WhisperForConditionalGeneration

# Configuración del dispositivo y tipo de datos
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

# Establecer el directorio actual
directorio_actual = os.path.abspath(os.path.dirname(__file__))
os.chdir(directorio_actual)

# Configuración del modelo
nombre_usuario_windows = "Carlos"
directorio_modelo = f"C:/Users/{nombre_usuario_windows}/.cache/huggingface/hub/models--openai--whisper-large-v3/snapshots/1ecca609f9a5ae2cd97a576a9725bc714c022a93"
if os.path.exists(directorio_modelo):
    print(f"La ubicación del modelo existe! Accediendo al directorio actual...")
else:
    print(f"La ubicación del modelo que se ha puesto no existe, échale un vistazo ---> {directorio_modelo}")

print(f"Se está ejecutando el script desde --> {directorio_actual}")

# Mostrar archivos válidos
archivos_en_directorio = os.listdir(directorio_actual)
archivos_a_elegir = [file for file in archivos_en_directorio if str(file).endswith((".wav", ".mp3", "mp4"))]

print(f"Mostrando archivos válidos para ejecución con whisper {archivos_a_elegir}")

# Selección del archivo
archivo_seleccionado = input("Escribe el nombre del archivo a ejecutar \n ---> ")

print(f"Has seleccionado el archivo {archivo_seleccionado}")

camino_al_audio = os.path.join(directorio_actual, archivo_seleccionado)

print(f"Se está cogiendo el archivo de audio desde aquí --> {camino_al_audio}")

# Verificar la existencia del archivo de audio
if os.path.exists(camino_al_audio):
    print("La dirección al archivo de audio es correcta! Se cargará el modelo")
    processor = WhisperProcessor.from_pretrained(directorio_modelo)
    model = WhisperForConditionalGeneration.from_pretrained(directorio_modelo, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True)
    
    direccion_ffmpeg = "C:/Users/Carlos/Desktop/whisper/ffmpeg/app/bin/ffmpeg.exe"
    if processor and model:
        print("El modelo se ha cargado")
        
        input_file = archivo_seleccionado
        output_file = f"16ksr_{archivo_seleccionado}"
        camino_al_audio_nuevo = os.path.join(directorio_actual, output_file)
        new_sample_rate = 16000

        # Convertir el archivo de audio a 16 kHz
        ffmpeg_command = [direccion_ffmpeg, "-i", input_file, "-ar", str(new_sample_rate), output_file]
        subprocess.run(ffmpeg_command)
        print(f"Archivo con la sample rate necesaria para procesamiento del modelo creado en {camino_al_audio_nuevo}")

        if os.path.exists(camino_al_audio_nuevo):
            print("El camino al archivo nuevo existe! Cargando el archivo con librosa...")

            # Directorio de fragmentos
            directorio_fragmentos = os.path.join(directorio_actual, "fragmentos")
            if not os.path.exists(directorio_fragmentos):
                os.makedirs(directorio_fragmentos)

            # Dividir el audio en fragmentos y guardarlos
            audio = AudioSegment.from_file(camino_al_audio_nuevo)
            chunk_length_ms = 30000  # 30 segundos
            for i, chunk in enumerate(audio[::chunk_length_ms]):
                fragmento_path = os.path.join(directorio_fragmentos, f"fragmento_{i}.wav")
                chunk.export(fragmento_path, format="wav")

            # Transcribir los fragmentos en orden
            full_transcription = ""
            fragmentos = sorted(os.listdir(directorio_fragmentos), key=lambda x: int(x.split('_')[1].split('.')[0]))

            for fragmento in fragmentos:
                fragmento_path = os.path.join(directorio_fragmentos, fragmento)
                audio_chunk, _ = librosa.load(fragmento_path, sr=16000)
                input_features = processor(audio_chunk, sampling_rate=16000, return_tensors="pt").input_features
                with torch.no_grad():
                    generated_ids = model.generate(input_features)
                transcription = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
                full_transcription += transcription + " "

            full_transcription = full_transcription.strip()

            # Guardar la transcripción completa en un archivo
            nombre_archivo_generado = f"texto_de_{archivo_seleccionado}.txt"
            with open(nombre_archivo_generado, "w") as archivo:
                archivo.write(full_transcription)

            print(f"La transcripción completa tiene una longitud de {len(full_transcription)} caracteres")
            print(full_transcription)

        else:
            print(f"El camino al archivo de audio nuevo {output_file} no existe, compruébalo --> {camino_al_audio_nuevo}")
    else:
        print("El modelo no se ha cargado")
else:
    print(f"La dirección del archivo de audio es incorrecta, échale un vistazo: {camino_al_audio}")
