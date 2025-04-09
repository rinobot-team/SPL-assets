import os
import cv2
import numpy as np
import argparse

def adjust_illumination(img, alpha, beta):
    """
    Ajusta brilho e contraste da imagem.
    nova_imagem = alpha * img + beta
    Parâmetros:
      - alpha: controle de contraste (ex.: 0.7 a 1.3)
      - beta: controle de brilho (ex.: -25 a +25)
    """
    return cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

def random_rotation(img, max_angle=45):
    """
    Rotaciona a imagem aleatoriamente em torno do centro.
    O ângulo é sorteado entre -max_angle e +max_angle graus.
    """
    h, w = img.shape[:2]
    angle = np.random.uniform(-max_angle, max_angle)
    M = cv2.getRotationMatrix2D((w/2, h/2), angle, 1.0)
    # Usa BORDER_REFLECT para evitar bordas escuras
    return cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REFLECT)

def create_random_background(shape):
    """
    Cria uma imagem de fundo de cor sólida aleatória.
    Parâmetro:
      - shape: tupla (altura, largura, canais)
    """
    # Sorteia uma cor aleatória para cada canal (B, G, R)
    bg_color = np.random.randint(0, 256, size=(3,), dtype=np.uint8)
    return np.full(shape, bg_color, dtype=np.uint8)

def extract_foreground(img, threshold_value=250):
    """
    Extrai o objeto da imagem considerando que o fundo é quase branco.
    Converte para escala de cinza, aplica threshold inverso para criar uma máscara.
    Retorna:
      - fg: a imagem (foreground)
      - mask: a máscara (valores 0 ou 1) com o objeto em 1.
    Se o fundo não for branco, ajuste o parâmetro threshold_value.
    """
    # Converte para escala de cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Cria uma máscara: pixels abaixo de threshold_value são considerados objeto
    _, mask = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY_INV)
    # Converte a máscara para escala de 0 a 1 (float32)
    mask = mask.astype(np.float32) / 255.0
    # Converte máscara para 3 canais para multiplicar com a imagem colorida
    mask = cv2.merge([mask, mask, mask])
    return img, mask

def composite_foreground_background(fg, mask, background):
    """
    Compoe o objeto (foreground) com o fundo (background) usando a máscara.
    Fórmula: resultado = (mask * fg) + ((1 - mask) * background)
    """
    fg = fg.astype(np.float32)
    background = background.astype(np.float32)
    comp = mask * fg + (1 - mask) * background
    return cv2.convertScaleAbs(comp)

def generate_variations(img_path, output_dir, num_variations):
    """
    Gera variações da imagem aplicando:
      - ajuste de brilho/contraste,
      - rotação,
      - substituição do fundo por uma cor aleatória.
    Salva as imagens no diretório de saída.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Carrega a imagem original
    img = cv2.imread(img_path)
    if img is None:
        raise FileNotFoundError(f"Imagem não encontrada: {img_path}")
    
    # Extrai o objeto com base no fundo branco (pode ser ajustado)
    fg, mask = extract_foreground(img, threshold_value=250)
    
    h, w = img.shape[:2]
    
    for i in range(num_variations):
        # 1. Ajuste aleatório de iluminação
        alpha = np.random.uniform(0.7, 1.3)  # contraste
        beta  = np.random.uniform(-20, 20)     # brilho
        img_adjusted = adjust_illumination(fg, alpha, beta)
        
        # 2. Aplica rotação aleatória
        img_rotated = random_rotation(img_adjusted, max_angle=25)
        mask_rotated = random_rotation(mask, max_angle=25)
        
        # 3. Gera um fundo aleatório
        background = create_random_background((h, w, 3))
        
        # 4. Compoe o objeto (após transformação) com o fundo
        result = composite_foreground_background(img_rotated, mask_rotated, background)
        
        # Salva a imagem resultante
        out_path = os.path.join(output_dir, f"variation_{i}.png")
        cv2.imwrite(out_path, result)
        print(f"[OK] Variação {i} salva em: {out_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Gera variações de uma imagem (rotação, variação de luz e fundo) sem usar opencv_createsamples"
    )
    parser.add_argument("image", help="Caminho da imagem de entrada (.jpg/.png)")
    parser.add_argument("output", help="Diretório para salvar as variações")
    parser.add_argument("--num", type=int, default=3, help="Número de variações a gerar (padrão: 3)")
    args = parser.parse_args()
    
    generate_variations(args.image, args.output, args.num)

if __name__ == "__main__":
    main()
#   Exemplo de uso
#   python3 create_samples.py nome_da_imagem.png variacoes/ --num 3
