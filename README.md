CONTADOR DE ESTRELAS

📜 Introdução
    Este projeto tem como objetivo desenvolver uma solução eficiente para contagem de estrelas em imagens astronômicas de alta resolução, utilizando técnicas de computação paralela. O problema surge da necessidade de processar imagens extremamente grandes, que demandariam muito tempo em processamento sequencial. A solução proposta faz uso de paralelismo com Python e multiprocessing, simulando conceitos de MPI (Message Passing Interface) para acelerar o processamento por meio da divisão de tarefas.



🛑 Descrição do Problema e Justificativa
    O processamento de imagens astronômicas de grandes dimensões (acima de 20GB) apresenta gargalos computacionais quando realizado de forma sequencial, gerando tempos de espera elevados e alto consumo de recursos.

    Portanto, é necessário aplicar estratégias de paralelização para:

    - Reduzir o tempo de execução.

    - Melhorar o uso dos recursos computacionais.

    - Tornar o processamento de dados escalável e eficiente.


🔧 DESCRIÇÃO DA SOLUÇÃO

    Foram implementadas duas versões do algoritmo de detecção de estrelas:

    1. Versão Sequencial:

       	- A imagem inteira (mesmo uma muito grande) é carregada em memória usando memmap, o que permite lidar com arquivos gigantes sem estourar a RAM.
	- O código então divide manualmente a imagem em pedaços (tiles) de tamanho 1024x1024 pixels, que são armazenados em uma lista tiles.
	- Cada tile é processado de forma sequencial, um após o outro, e um pequeno delay artificial (time.sleep) é inserido após o processamento de cada tile.

    2. Versão Paralela (multiprocessing):

        A lista de tiles é distribuída entre múltiplos processos.

        Cada processo realiza a detecção de estrelas em seu subconjunto de tiles de forma independente.

        Ao final, os resultados são reunidos e combinados em uma imagem de saída com as detecções sobrepostas.


📂 Estrutura dos Códigos
    img
        imagem.jpg → Imagem original usada no conversor de imagem.

    gitignore → Ignorando arquivos

    contadordeestrela.py → Processamento linear

    contadorparalelo.py → Processamento paralelo

    conversordeimagem.py → Gera imagem grande em formato TIFF

    requirements.txt → Apresenta todas as bibliotecas que necessitam ser usadas.

    perfomances_analysis.html → Página HTML com os dados.

🧠 Conclusão
    O paralelismo proporcionou ganhos expressivos de desempenho, reduzindo significativamente o tempo de processamento.

    Observa-se que a eficiência diminui conforme aumentamos o número de threads, comportamento esperado devido à sobrecarga de comunicação e gerenciamento dos processos.

    A solução proposta se mostrou escalável e eficaz para processar grandes imagens astronômicas, validando a importância da computação paralela na área de ciência de dados e astronomia.

🚀 Projeto Integrador de Computação Paralela
    Discentes: João Victor Pimenta Lopes e Júlio César
    RA: 63439 / 63697       
