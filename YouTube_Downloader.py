import PySimpleGUI as sg
from pytube import YouTube
import os

# Define a área de trabalho do usuário como padrão
desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

sg.theme('reddit')

layout = [
    [sg.Text('Link'), sg.Input(key='link')],
    [sg.FolderBrowse('Escolher onde salvar', target='input_anexos'), sg.Input(key='input_anexos')],
    [sg.Button('Salvar Vídeo'), sg.Button('Salvar Áudio')],
    [sg.Output(size=(65, 10))]
]

janela = sg.Window('Janela Principal', layout=layout)

def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    sg.cprint(f'Download progress: {percentage_of_completion:.2f}%')

def DownloadVideo(link, path):
    try:
        youtubeObject = YouTube(link, on_progress_callback=progress_function)
        youtubeStream = youtubeObject.streams.get_highest_resolution()
        file_path = os.path.join(path, youtubeStream.default_filename)
        new_file_path = os.path.join(path, youtubeObject.title + '_video.' + youtubeStream.subtype)
        if os.path.exists(file_path):
            os.rename(file_path, new_file_path)
        youtubeStream.download(output_path=path)
        print("Download do vídeo feito com sucesso!")
    except Exception as e:
        print(f'Ocorreu um erro ao baixar o vídeo: {e}')

def DownloadAudio(link, path):
    try:
        youtubeObject = YouTube(link, on_progress_callback=progress_function)
        youtubeStream = youtubeObject.streams.filter(only_audio=True).first()
        file_path = os.path.join(path, youtubeStream.default_filename)
        new_file_path = os.path.join(path, youtubeObject.title + '_audio.' + youtubeStream.subtype)
        if os.path.exists(file_path):
            os.rename(file_path, new_file_path)
        youtubeStream.download(output_path=path)
        print("Download do áudio feito com sucesso!")
    except Exception as e:
        print(f'Ocorreu um erro ao baixar o áudio: {e}')

while True:
    event, values = janela.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'Salvar Vídeo':
        link = values['link']
        pasta_salvar = values['input_anexos'] if values['input_anexos'] else desktop_path
        DownloadVideo(link, pasta_salvar)
    elif event == 'Salvar Áudio':
        link = values['link']
        pasta_salvar = values['input_anexos'] if values['input_anexos'] else desktop_path
        DownloadAudio(link, pasta_salvar)

janela.close()
