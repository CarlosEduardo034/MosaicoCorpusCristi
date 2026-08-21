from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from pypdf import PdfWriter, PdfReader
import os
import shutil
import tempfile
from tkinter import Tk
from tkinter.filedialog import askopenfilename

COLUNAS = 5
LINHAS = 4

PASTA_RAIZ = "Mosaicos"
PASTA_ORIGINAL = os.path.join(
    PASTA_RAIZ,
    "Original"
)
PASTA_PDF = os.path.join(
    PASTA_RAIZ,
    "PDF"
)
os.makedirs(PASTA_ORIGINAL, exist_ok=True)
os.makedirs(PASTA_PDF, exist_ok=True)

def gerar_mosaico():
    Tk().withdraw()
    imagem_selecionada = askopenfilename(
        title="Selecione uma imagem",
        filetypes=[
            ("Imagens", "*.png *.jpg *.jpeg *.bmp *.webp"),
            ("Todos os arquivos", "*.*")
        ]
    )

    if not imagem_selecionada:
        print("Nenhuma imagem selecionada.")
        return
    nome_arquivo = os.path.basename(imagem_selecionada)
    imagem_original = os.path.join(
        PASTA_ORIGINAL,
        nome_arquivo
    )
    shutil.copy2(
        imagem_selecionada,
        imagem_original
    )

    nome_base = os.path.splitext(nome_arquivo)[0]
    pdf_saida = os.path.join(
        PASTA_PDF,
        f"{nome_base}_mosaico.pdf"
    )
    contador = 2

    while os.path.exists(pdf_saida):
        pdf_saida = os.path.join(
            PASTA_PDF,
            f"{nome_base}_mosaico_{contador}.pdf"
        )
        contador += 1

    img = Image.open(imagem_original)
    largura, altura = img.size
    print(f"Imagem carregada: {largura} x {altura} px")

    largura_bloco = largura / COLUNAS
    altura_bloco = altura / LINHAS

    c = canvas.Canvas(pdf_saida, pagesize=A4)
    pagina_largura, pagina_altura = A4
    numero_pagina = 1
    img_largura, img_altura = img.size
    escala = min(
        pagina_largura / img_largura,
        pagina_altura / img_altura
    )

    nova_largura = img_largura * escala
    nova_altura = img_altura * escala
    x = (pagina_largura - nova_largura) / 2
    y = (pagina_altura - nova_altura) / 2

    RODAPE = "rodape.png"
    if os.path.exists(RODAPE):
        largura_rodape = 120
        altura_rodape = 60
        margem = 15
        
        c.drawImage(
            RODAPE,
            pagina_largura - largura_rodape - margem,
            margem,
            width=largura_rodape,
            height=altura_rodape,
            preserveAspectRatio=True,
            mask='auto'
        )
    c.drawImage(
        imagem_original,
        x,
        y,
        width=nova_largura,
        height=nova_altura
    )

    c.setFont("Helvetica-Bold", 14)
    c.drawString(20, 20, "Visão Geral do Mosaico")
    c.setFont("Helvetica", 10)
    c.drawRightString(
        pagina_largura - 20,
        20,
        f"Página {numero_pagina}"
    )

    numero_pagina += 1
    c.showPage()

    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            esquerda = int(coluna * largura_bloco)
            topo = int(linha * altura_bloco)
            direita = int((coluna + 1) * largura_bloco)
            baixo = int((linha + 1) * altura_bloco)
            recorte = img.crop(
                (
                    esquerda,
                    topo,
                    direita,
                    baixo
                )
            )
            letra_linha = chr(65 + linha)
            nome_pagina = f"{letra_linha}{coluna + 1}"
            
            with tempfile.NamedTemporaryFile(
                suffix=".png",
                delete=False
            ) as arquivo_temp:
                recorte.save(arquivo_temp.name)
                c.drawImage(
                    arquivo_temp.name,
                    0,
                    0,
                    width=pagina_largura,
                    height=pagina_altura,
                    preserveAspectRatio=False
                )

            os.remove(arquivo_temp.name)
            c.setFont("Helvetica", 10)
            c.drawRightString(
                pagina_largura - 20,
                20,
                f"Página {numero_pagina} ({nome_pagina})"
            )

            numero_pagina += 1
            c.showPage()
            print(f"Página {nome_pagina} criada")
    c.save()

    print("Processamento concluído com sucesso!")
    print("Mapa de montagem:")
    print("A1 A2 A3 A4 A5")
    print("B1 B2 B3 B4 B5")
    print("C1 C2 C3 C4 C5")
    print("D1 D2 D3 D4 D5")
    print(f"Imagem original: {imagem_original}")
    print(f"PDF: {pdf_saida}")

def menu_mesclagem():
    fila_mesclagem = []
    while True:
        print()
        print("=" * 40)
        print("MESCLAGEM DE PDFs")
        print("=" * 40)
        print(f"Arquivos na fila: {len(fila_mesclagem)}")
        print()
        print("1 - Adicionar arquivo à mesclagem")
        print("2 - Listar arquivos")
        print("3 - Remover arquivo")
        print("4 - Mesclar arquivos")
        print("5 - Voltar")
        print()
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            Tk().withdraw()
            arquivo = askopenfilename(
                title="Selecione um PDF",
                filetypes=[
                    ("PDF", "*.pdf")
                ]
            )
            if arquivo:
                fila_mesclagem.append(arquivo)
                print()
                print("Arquivo adicionado:")
                print(os.path.basename(arquivo))
        elif opcao == "2":
            print()
            if not fila_mesclagem:
                print("Nenhum arquivo na fila.")
                continue
            print("Arquivos na fila:")
            for i, arquivo in enumerate(
                fila_mesclagem,
                start=1
            ):
                print(
                    f"{i} - {os.path.basename(arquivo)}"
                )
        elif opcao == "3":
            if not fila_mesclagem:
                print("Fila vazia.")
                continue
            print()
            for i, arquivo in enumerate(
                fila_mesclagem,
                start=1
            ):
                print(
                    f"{i} - {os.path.basename(arquivo)}"
                )
            try:
                indice = int(
                    input(
                        "Número do arquivo para remover: "
                    )
                )
                removido = fila_mesclagem.pop(
                    indice - 1
                )
                print(
                    f"Removido: {os.path.basename(removido)}"
                )
            except:
                print("Opção inválida.")
        elif opcao == "4":
            if len(fila_mesclagem) == 0:
                print("Nenhum PDF na fila.")
                continue
            nome_final = input(
                "Nome do PDF final: "
            ).strip()
            if not nome_final:
                print("Nome inválido.")
                continue
            pdf_final = os.path.join(
                PASTA_PDF,
                f"{nome_final}.pdf"
            )
            contador = 2
            while os.path.exists(pdf_final):
                pdf_final = os.path.join(
                    PASTA_PDF,
                    f"{nome_final}_{contador}.pdf"
                )
                contador += 1
            writer = PdfWriter()
            for pdf in fila_mesclagem:
                reader = PdfReader(pdf)
                for pagina in reader.pages:
                    writer.add_page(pagina)
            with open(pdf_final, "wb") as arquivo_saida:
                writer.write(arquivo_saida)
            print()
            print("PDF mesclado com sucesso!")
            print(pdf_final)
        elif opcao == "5":
            break
        else:
            print("Opção inválida.")

while True:
    print()
    print("=" * 40)
    print("GERADOR DE MOSAICOS")
    print("=" * 40)
    print("1 - Gerar novo mosaico")
    print("2 - Mesclar PDFs")
    print("3 - Finalizar execução")
    print()

    opcao = input("Escolha uma opção: ").strip()

    if opcao == "1":
        gerar_mosaico()
    elif opcao == "2":
        menu_mesclagem()
    elif opcao == "3":
        print("Encerrando programa...")
        break
    else:
        print("Opção inválida.")
