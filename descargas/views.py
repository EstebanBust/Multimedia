from django.shortcuts import render
import yt_dlp

def search_videos(request):
    query = request.GET.get('q', '')  # Obtener el término de búsqueda desde la URL
    video_results = []

    if query:
        ydl_opts = {
            'noplaylist': True,
            'quiet': True,
            'extract_flat': True  # Obtén solo la información del video sin descargar
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_query = f"ytsearch10:{query}"
            result = ydl.extract_info(search_query, download=False)
            print(result)
            if 'entries' in result:
                for entry in result['entries']:
                    # Si hay miniaturas, tomamos la primera
                    if 'thumbnails' in entry and entry['thumbnails']:
                        entry['thumbnail'] = entry['thumbnails'][0]['url']
                    else:
                        entry['thumbnail'] = ''
                    video_results.append(entry)
                    
    return render(request, 'search_results.html', {'videos': video_results, 'query': query})
