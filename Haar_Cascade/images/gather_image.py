from icrawler.builtin import BingImageCrawler
import os
import concurrent.futures
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

target_number = 10  # Número de imagens por classe

# Dicionário contendo classes positivas e negativas
categories = {
    # 'p': ['football ball', 'soccer ball', 'ball', 'soccer spl ball', 'standart football ballS'],
    # 'n': ['human face', 'NAO V6', 'red gloves', 'football field', 'goal'],

    'p': ['football ball', 'soccer ball', 'ball', 'soccer spl ball', 'standart football ballS'],
    'n': ['human face', 'NAO V6', 'red gloves', 'football field', 'goal'],
}

def download_images(folder, keyword):
    try:
        logging.info(f"Starting download for {keyword} in folder {folder}")
        crawler = BingImageCrawler(storage={'root_dir': f'{folder}'})
        crawler.crawl(keyword=keyword, filters=None, max_num=target_number, offset=0)
        logging.info(f"Finished download for {keyword} in folder {folder}")
    except Exception as e:
        logging.error(f"Error downloading {keyword}: {e}")

# Criar diretórios e baixar imagens
for folder, classes in categories.items():
    os.makedirs(f'{folder}', exist_ok=True)
    
    # Usando ThreadPoolExecutor para paralelizar o download de imagens
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(download_images, folder, c) for c in classes]
        
        # Esperar todas as threads terminarem
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logging.error(f"Error in thread: {e}")

logging.info("All downloads completed.")