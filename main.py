import tkinter as tk
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random
import threading

# Função para buscar uma postagem aleatória


def buscar_postagem_aleatoria():
    url = url_entry.get()

    def buscar_postagem_aleatoria_assincronamente():
        # Configurando as opções do driver para torná-lo invisível (modo headless)
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        # Configurando o driver do navegador (neste caso, Chrome)
        driver = webdriver.Chrome(options=chrome_options)

        # Abrindo a URL no navegador
        driver.get("https://www.threads.net/"+url)

        # Exibindo a mensagem "Aguarde, estou buscando um tweet da @tananan..."
        status_label.config(
            text="\nWait, I'm looking for a random post from " + url + "\n")

        status_label.config(fg="green")

        # Limpando o resultado anterior
        resultado_label.config(text="")

        # Encontrando os elementos que contêm o texto das postagens
        post_elements = []

        # Definindo o número máximo de rolagens para coletar as postagens
        max_rolagens = 10

        # Rolar a página para baixo para carregar mais postagens
        for i in range(max_rolagens):
            # Encontrando os elementos que contêm o texto das postagens na página atual
            post_elements.extend(driver.find_elements(
                By.XPATH, '//div[contains(@class, "x1a6qonq") and contains(@class, "xj0a0fe") and contains(@class, "x126k92a") and contains(@class, "x6prxxf") and contains(@class, "x7r5mf7")]'))

            # Rolando a página para baixo
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

            # Aguardando um curto período após cada rolagem para permitir que as postagens sejam carregadas
            time.sleep(1)

        # Escolhendo uma postagem aleatória da lista
        if post_elements:
            postagem_aleatoria = random.choice(post_elements)
            # Exibindo a label
            resultado_label.config(
                text="Random Post:\n\n")

            # Obtendo o texto do tweet
            tweet_text = postagem_aleatoria.text

            # Definindo um limite de largura para a exibição
            largura_limite = 50  # Defina o valor desejado

            # Dividindo a mensagem em várias linhas
            tweet_lines = [tweet_text[i:i+largura_limite]
                           for i in range(0, len(tweet_text), largura_limite)]

            # Combinando as linhas com quebras de linha
            tweet_formatted = "\n".join(tweet_lines)

            # Exibindo o texto do tweet formatado
            resultado_label.config(
                text=resultado_label.cget("text") + tweet_formatted)
            # Configurando o background para branco e a cor do texto para preta
            resultado_label.config(bg="white", fg="black")
            # Aumentando o tamanho da fonte do texto do tweet
            resultado_label.config(font=("Arial", 16))
        else:
            resultado_label.config(text="\nNo tweets found.")
            resultado_label.config(fg="red")

        # Fechando o navegador
        driver.quit()

    # Criando uma thread para buscar a postagem aleatória
    thread = threading.Thread(target=buscar_postagem_aleatoria_assincronamente)
    thread.start()


# Criando janela da interface
window = tk.Tk()
window.title("Random Post from @any_profile")

# Definindo as dimensões da janela
window.geometry("600x400")  # Largura x Altura

# Calculando o centro da tela
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width - 600) // 2
y = (screen_height - 400) // 2

# Centralizando a janela na tela
window.geometry(f"560x310+{x}+{y}")

# Label e campo de entrada para o URL do perfil
url_label = tk.Label(window, text="@ from the profile:")
url_label.pack()

url_entry = tk.Entry(window)
url_entry.pack()

# Insere o texto "@any_profile" na posição 5 do widget `url_entry`
url_entry.insert(5, "@any_profile")


# Botão para buscar a postagem aleatória
buscar_postagem_button = tk.Button(
    window, text="Search Random Post", command=buscar_postagem_aleatoria)
buscar_postagem_button.pack()

# Label para exibir o status da busca
status_label = tk.Label(window, text="")
status_label.pack()

# Label para exibir o resultado
resultado_label = tk.Label(window, text="")
resultado_label.pack()

# Iniciar a interface
window.mainloop()
