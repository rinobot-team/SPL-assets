import cv2
import numpy as np
import os

# Caminhos dos arquivos (uso correto de caminhos no Linux)
cascade_path = os.path.join("wheights/cascade_ball.xml")
image_path = os.path.join("../images/test/football.jpeg")
output_path = os.path.join("resultado_detectado.png")  # Caminho para salvar a imagem

# Verifica se os arquivos existem
if not os.path.exists(cascade_path):
    raise FileNotFoundError(f"Arquivo do classificador não encontrado: {cascade_path}")

if not os.path.exists(image_path):
    raise FileNotFoundError(f"Arquivo da imagem não encontrado: {image_path}")

# Carregar classificador treinado
ball_cascade = cv2.CascadeClassifier(cascade_path)

if ball_cascade.empty():
    raise IOError("Erro ao carregar o classificador. Verifique se o arquivo XML está correto.")

# Carregar imagem
img = cv2.imread(image_path)

if img is None:
    raise IOError("Erro ao carregar a imagem. Verifique se o caminho está correto.")

# Redimensionamento proporcional
scale_factor = 400 / max(img.shape[:2])  # Mantém a proporção
new_size = (int(img.shape[1] * scale_factor), int(img.shape[0] * scale_factor))
resized = cv2.resize(img, new_size, interpolation=cv2.INTER_LINEAR)

# Conversão para escala de cinza
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

# Aplicar filtro Gaussiano para suavizar a imagem
gray = cv2.GaussianBlur(gray, (5, 5), 0)

# Detecção de objetos
balls = ball_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(20, 20))

# Desenhar retângulos ao redor das bolas detectadas
for (x, y, w, h) in balls:
    cv2.rectangle(resized, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Salvar a imagem com as detecções
cv2.imwrite(output_path, resized)
print(f"Imagem salva com as detecções: {output_path}")