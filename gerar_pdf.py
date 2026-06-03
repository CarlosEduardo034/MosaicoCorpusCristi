from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os

# ==========================================
# CONFIGURAÇÕES
# ==========================================

imagem_original = "imagem.png"

COLUNAS = 5
LINHAS = 4

# ==========================================
# PASTAS
# ==========================================

PASTA_RAIZ = "Mosaicos"
PASTA_IMAGENS = os.path.join(PASTA_RAIZ, "Imagens")
PASTA_PDF = os.path.join(PASTA_RAIZ, "PDF")

os.makedirs(PASTA_IMAGENS, exist_ok=True)
os.makedirs(PASTA_PDF, exist_ok=True)

pdf_saida = os.path.join(PASTA_PDF, "mosaico_a4.pdf")

# ==========================================
# ABRE IMAGEM
# ==========================================

img = Image.open(imagem_original)

largura, altura = img.size

print(f"Imagem carregada: {largura} x {altura} px")

# ==========================================
# TAMANHO DOS RECORTES
# ==========================================

largura_bloco = largura / COLUNAS
altura_bloco = altura / LINHAS

# ==========================================
# CRIA PDF
# ==========================================

c = canvas.Canvas(pdf_saida, pagesize=A4)

pagina_largura, pagina_altura = A4

# ==========================================
# PÁGINA 1 - VISÃO GERAL
# ==========================================

img_largura, img_altura = img.size

escala = min(
    pagina_largura / img_largura,
    pagina_altura / img_altura
)

nova_largura = img_largura * escala
nova_altura = img_altura * escala

x = (pagina_largura - nova_largura) / 2
y = (pagina_altura - nova_altura) / 2

c.drawImage(
    imagem_original,
    x,
    y,
    width=nova_largura,
    height=nova_altura
)

c.setFont("Helvetica-Bold", 14)
c.drawString(20, 20, "Visão Geral do Mosaico")

c.showPage()

# ==========================================
# PROCESSAMENTO
# ==========================================

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

        nome_imagem = os.path.join(
            PASTA_IMAGENS,
            f"{nome_pagina}.png"
        )

        recorte.save(nome_imagem)

        c.drawImage(
            nome_imagem,
            0,
            0,
            width=pagina_largura,
            height=pagina_altura,
            preserveAspectRatio=False
        )

        c.showPage()

        print(f"Página {nome_pagina} criada")

# ==========================================
# SALVA PDF
# ==========================================

c.save()

print()
print("Processamento concluído com sucesso!")
print()
print("Mapa de montagem:")
print("A1 A2 A3 A4 A5")
print("B1 B2 B3 B4 B5")
print("C1 C2 C3 C4 C5")
print("D1 D2 D3 D4 D5")
print()
print(f"Imagens: {PASTA_IMAGENS}")
print(f"PDF: {pdf_saida}")