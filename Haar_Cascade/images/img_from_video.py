import cv2
import os
import argparse

def extract_frames(video_path: str, output_folder: str) -> float:
    """
    Extrai todos os frames de um vídeo e salva como imagens,
    retornando a taxa de FPS do vídeo.

    :param video_path: Caminho para o arquivo de vídeo.
    :param output_folder: Pasta onde os frames serão salvos.
    :return: FPS do vídeo.
    """
    # Abre o vídeo
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Não foi possível abrir o vídeo: {video_path}")

    # Obtém a taxa de FPS
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"[INFO] Taxa de FPS: {fps:.2f}")

    # Cria a pasta de saída, se não existir
    os.makedirs(output_folder, exist_ok=True)

    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Nome do arquivo: frame_00001.jpg, frame_00002.jpg, ...
        filename = os.path.join(output_folder, f"frame_{frame_idx:05d}.jpg")
        cv2.imwrite(filename, frame)
        frame_idx += 1

    cap.release()
    print(f"[INFO] Total de frames extraídos: {frame_idx}")
    return fps

def main():
    parser = argparse.ArgumentParser(
        description="Extrai frames de um vídeo e informa a taxa de FPS."
    )
    parser.add_argument("video", help="Caminho para o arquivo de vídeo (ex: video.mp4)")
    parser.add_argument(
        "-o", "--output",
        default="frames",
        help="Pasta de saída para os frames (padrão: ./frames)"
    )
    args = parser.parse_args()

    fps = extract_frames(args.video, args.output)
    print(f"[OK] Frames salvos em '{args.output}'. Vídeo com {fps:.2f} FPS.")

if __name__ == "__main__":
    main()
