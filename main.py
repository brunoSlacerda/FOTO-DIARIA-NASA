import requests
from PIL import Image, ImageTk
import tkinter as tk
from io import BytesIO
from googletrans import Translator

def traduzirTexto(texto):
    translator = Translator()
    traducao = translator.translate(texto, dest='pt')
    return traducao.text

def exibirImagem():
    api_key = 'nnCfpdalx4d5vxGGhJiARmQmvczuOveiTCS19DEl'
    url = f'https://api.nasa.gov/planetary/apod?api_key={api_key}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        url_imagem = data.get('url', '')
        explicacao = data.get('explanation')
        dia = data.get('date')


    if url_imagem:
        response_imagem = requests.get(url_imagem)

        if response_imagem.status_code == 200:
            content_type = response_imagem.headers.get('content-type', '')

            if 'image' in content_type:
                try:
                    imagem = Image.open(BytesIO(response_imagem.content))

                    root = tk.Tk()
                    root.title(f"Imagem da NASA dia: {dia}")

                    tk_imagem = ImageTk.PhotoImage(imagem)
                    label_imagem = tk.Label(root, image=tk_imagem)
                    label_imagem.pack()

                    explicacao_traduzida = traduzirTexto(explicacao)

                    explicacao_label = tk.Label(root, text=explicacao_traduzida, wraplength=800, justify='left')
                    explicacao_label.pack(pady=30)

                    root.mainloop()
                except Exception as e:
                    print(f"Erro ao abrir a imagem: {e}")
            else:
                print(f"O conteudo fornecido hoje pela API é um vídeo. Link para o vídeo: https://apod.nasa.gov/apod/astropix.html")
        else:
            print(f"Falha ao baixar a imagem. Código de status: {response_imagem.status_code}")
    else:
        print("URL da imagem não encontrada na resposta da API.")
        
exibirImagem()