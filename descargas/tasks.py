import os
import subprocess
import shlex
import json
from celery import shared_task
from django.conf import settings

@shared_task
def download_video_task(video_url):
    # Definir la ruta para los archivos
    video_dir = os.path.join(settings.MEDIA_ROOT, 'videos')
    thumbnail_dir = os.path.join(settings.MEDIA_ROOT, 'thumbnails')
    os.makedirs(video_dir, exist_ok=True)
    os.makedirs(thumbnail_dir, exist_ok=True)

    try:
        # Obtener el título del video usando yt-dlp
        info_command = f'yt-dlp -J "{video_url}"'
        info_args = shlex.split(info_command)
        result = subprocess.run(info_args, capture_output=True, text=True, check=True)
        video_info = json.loads(result.stdout)
        video_title = video_info['title'].replace('/', '_').replace('\\', '_')  # Reemplaza caracteres no válidos

        # Definir el nombre del archivo de salida
        video_filename = f"{video_title}.mp4"
        thumbnail_filename = f"{video_title}.jpg"
        output_file = os.path.join(video_dir, video_filename)
        thumbnail_file = os.path.join(thumbnail_dir, thumbnail_filename)

        # Descargar el video y convertirlo a MP4
        download_command = (
            f'yt-dlp "{video_url}" '
            f'--format "bestvideo+bestaudio/best" '
            f'--merge-output-format mp4 '
            f'-o "{output_file}.%(ext)s" '
        )
        subprocess.run(shlex.split(download_command), capture_output=True, text=True, check=True)

        # Descargar y convertir la miniatura a JPG
        thumbnail_command = (
            f'yt-dlp "{video_url}" '
            f'--skip-download '
            f'--write-thumbnail '
            f'--convert-thumbnails jpg '
            f'-o "{thumbnail_file}"'
        )
        subprocess.run(shlex.split(thumbnail_command), capture_output=True, text=True, check=True)

        return f"Download completed: {video_filename}, Thumbnail: {thumbnail_filename}"

    except subprocess.CalledProcessError as e:
        return f"Error during download: {e}"
    except json.JSONDecodeError:
        return "Failed to decode video information"
