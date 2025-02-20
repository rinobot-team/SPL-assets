import cv2
import numpy as np

# Caminhos dos arquivos
cascade_path = r"../wheights/cascade_ball.xml"
image_path = r"../images/test/football.jpeg"

# Carregar classificador treinado
face_cascade = cv2.CascadeClassifier(cascade_path)

if face_cascade.empty():
    raise IOError("Erro ao carregar o classificador. Verifique o caminho do arquivo.")

# Carregar imagem
img = cv2.imread(image_path)

if img is None:
    raise IOError("Erro ao carregar a imagem. Verifique o caminho do arquivo.")

# Redimensionamento proporcional
scale_factor = 400 / max(img.shape[:2])  # Mantém a proporção
new_size = (int(img.shape[1] * scale_factor), int(img.shape[0] * scale_factor))
resized = cv2.resize(img, new_size)

# Conversão para escala de cinza
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

# Aplicar filtro Gaussiano para suavizar a imagem e melhorar a detecção
gray = cv2.GaussianBlur(gray, (5, 5), 0)

# Ajuste dos parâmetros de detecção
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(20, 20))

# Desenhar retângulos ao redor dos objetos detectados
for (x, y, w, h) in faces:
    cv2.rectangle(resized, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Exibir resultado
cv2.imshow('Detecção de Bolas', resized)
cv2.waitKey(0)
cv2.destroyAllWindows()
