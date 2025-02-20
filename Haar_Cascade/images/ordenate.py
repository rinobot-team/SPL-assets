import os

def renumerar_arquivos(pasta):
    # Lista todos os arquivos na pasta
    arquivos = [arq for arq in os.listdir(pasta) if os.path.isfile(os.path.join(pasta, arq))]
    
    # Ordena os arquivos (opcional, dependendo da necessidade)
    arquivos.sort()

    # Renomeia os arquivos
    for indice, nome_arquivo in enumerate(arquivos, start=1):
        # Define o novo nome no formato 00001, 00002, etc.
        novo_nome = f"{indice:05d}{os.path.splitext(nome_arquivo)[1]}"  # Mantém a extensão original
        caminho_antigo = os.path.join(pasta, nome_arquivo)
        caminho_novo = os.path.join(pasta, novo_nome)
        
        # Renomeia o arquivo
        os.rename(caminho_antigo, caminho_novo)
        print(f"Renomeado: {nome_arquivo} -> {novo_nome}")

    print("Renumeração concluída!")

# Caminho da pasta onde os arquivos estão
pasta = 'p'  # Substitua pelo caminho da sua pasta
renumerar_arquivos(pasta)
pasta = 'n'  # Substitua pelo caminho da sua pasta
renumerar_arquivos(pasta)