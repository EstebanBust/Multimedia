import subprocess
import shlex
import time
import os
import json
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from urllib.parse import quote

def download_video(request):
    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        if not video_url:
            return HttpResponseBadRequest("No URL provided")

        # Definir la ruta para los archivos
        video_dir = os.path.join(settings.MEDIA_ROOT, 'videos')
        thumbnail_dir = os.path.join(settings.MEDIA_ROOT, 'thumbnails')
        os.makedirs(video_dir, exist_ok=True)
        os.makedirs(thumbnail_dir, exist_ok=True)

        # Obtener el título del video usando yt-dlp
        try:
            # Medir el tiempo de descarga
            start_time = time.time()
            
            info_command = f'yt-dlp -J "{video_url}"'
            info_args = shlex.split(info_command)
            result = subprocess.run(info_args, capture_output=True, text=True, check=True)
            video_info = json.loads(result.stdout)
            video_title = video_info['title']
            video_title = video_title.replace('/', '_').replace('\\', '_')  # Reemplaza caracteres no válidos para nombres de archivos

            # Definir el nombre del archivo de salida
            output_file = os.path.join(video_dir, video_title)
            thumbnail_file = os.path.join(thumbnail_dir, f"{video_title}")
            
            # Todo este codigo verifica si existe el video para no descargarlo nuevamente
            video_filename = f"{video_title}.mp4"
            thumbnail_filename = f"{video_title}.jpg"
            output_file = os.path.join(video_dir, video_filename)
            thumbnail_file = os.path.join(thumbnail_dir, thumbnail_filename)
            
            # Verificar si el video y la miniatura ya existen
            # Todo este codigo verifica si existe el video para no descargarlo nuevamente
            if os.path.exists(output_file) and os.path.exists(thumbnail_file):
                # Si el video y la miniatura ya existen, redirigir directamente a la reproducción
                end_time = time.time()
                elapsed_time = end_time - start_time
                print(elapsed_time, "segundos")
                return redirect('play_video', video_path=f"videos/{video_filename}")
            
            # Comando para descargar el video y convertirlo a MP4
            download_command = (
                f'yt-dlp "{video_url}" '
                f'--format "bestvideo+bestaudio/best" '
                f'--merge-output-format mp4 '
                f'-o "{output_file}.%(ext)s" '
            )

            # Ejecutar el comando de descarga
            subprocess.run(shlex.split(download_command), capture_output=True, text=True, check=True)
            
            thumbnail_command = (
                f'yt-dlp "{video_url}" '
                f'--skip-download '
                f'--write-thumbnail '
                f'--convert-thumbnails jpg '
                f'-o "{thumbnail_file}"'
            )
            subprocess.run(shlex.split(thumbnail_command), capture_output=True, text=True, check=True)
            
            # Medir el tiempo de finalización
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(elapsed_time, "segundos")

            # Confirmar que la descarga y conversión fueron exitosas
            downloaded_file = f"{output_file}.mp4"
            if os.path.exists(downloaded_file):
                # Redirigir a la vista de reproducción en caso de éxito
                return redirect('play_video', video_path=f"videos/{os.path.basename(downloaded_file)}")
            else:
                return HttpResponseBadRequest("Download or conversion failed")
        
        except subprocess.CalledProcessError as e:
            return HttpResponseBadRequest(f"Error during download: {e}")
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Failed to decode video information")
    
    return render(request, 'download_video.html')

def play_video(request, video_path):
    video_url = os.path.join(settings.MEDIA_URL, video_path)
    return render(request, 'play_video.html', {'video_url': video_url})

def lista_videos(request):
    video_dir = os.path.join(settings.MEDIA_ROOT, 'videos')
    video_files = [f for f in os.listdir(video_dir) if os.path.isfile(os.path.join(video_dir, f))]
    
    # Generar una lista con la información necesaria
    videos = []
    for f in video_files:
        if f.endswith('.mp4'):
            video_title = os.path.splitext(f)[0]
            video_path = os.path.join(settings.MEDIA_URL, 'videos', f)
            thumbnail_path = os.path.join(settings.MEDIA_URL, 'thumbnails', f"{video_title}.jpg")
            videos.append({
                'title': video_title,
                'video_url': video_path,
                'thumbnail_url': thumbnail_path,
                'play_url': f"/play_video/{quote(f)}"
            })
    
    return render(request, 'lista_videos.html', {'videos': videos})
