# SPL-assets
## O que temos:
- [X] Cross Toolchain 2.8.5 (C++)
- [ ] Cross Toolchain 2.1.4 (C++)
- [ ] Imagem 2.8.5 Robocupper
- [ ] Imagem 2.1.4


## Treinamento do Haar cascade
- Consiste em uma coleta de imagens para o uso de treinamento de pesos para identificação de objetos desejáveis durante o jogo.
- Já esta presente os pesos e o procedimento para coletar imagens de bolas pretas e brancas e de objetos a ignorar.

### Scripts disponíveis

- Dentro dos scripts, estão:
    - gather_image.py: Coleta de imagens seguindo as classes positivas (objetos a serem identificados) e negativas (objetos a serem ignorados).
    - ordenate.py: Ordenação das imagens e para o seu treinamento.
    Quantidade boa encontrada para o treinamento: 50 imagens positivas para 800 negativas.

    - trains_cascade.py: Utiliza os pesos encontrados após o treinamento com as imagens coletadas em cima de um exemplo fornecido para verificar a acurácia da identificação.
        - OBS: O teste não pode estar contido no conjunto de postivos ou negativos.

### Construção dos pesos:

A construção dos pesos para a identificação dos objetos foi feita utilizando uma interface gráfica presente apenas para windows encontrada em https://amin-ahmadi.com/cascade-trainer-gui/ e seguindo o seguinte passo a passo https://medium.com/@vipulgote4/guide-to-make-custom-haar-cascade-xml-file-for-object-detection-with-opencv-6932e22c3f0e