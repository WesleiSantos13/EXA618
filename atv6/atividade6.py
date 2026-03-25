import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import urlparse

dados = []

headers = {
    "User-Agent": "Mozilla/5.0"
}

# Função para montar URL (concatenação)
def montar_url(base, src):
    if not src:
        return None

    src = src.strip()

    # ignora base64
    if src.startswith("data:"):
        return None

    # já é absoluta
    if src.startswith("http"):
        return src

    # remove ./ do início
    if src.startswith("./"):
        src = src[2:]

    # começa com /
    if src.startswith("/"):
        parsed = urlparse(base)
        return f"{parsed.scheme}://{parsed.netloc}{src}"

    # concatenação padrão
    return base.rstrip("/") + "/" + src.lstrip("/")


#  Ler os links
with open("seeds.txt", "r", encoding="utf-8") as f:
    for linha in f:
        url = linha.strip()
        print("Processando:", url)

        try:
            req = urllib.request.Request(url, headers=headers)
            page = urllib.request.urlopen(req)
            html = page.read().decode('utf-8', errors='ignore')
        except:
            print("Erro ao acessar:", url)
            continue

        soup = BeautifulSoup(html, 'lxml')
        titulo = soup.title.string if soup.title else "Sem título"

        imagens = []
        vistos = set()

        for tag in soup.find_all(['img', 'source']):
            
            src = (
                tag.get("src") or
                tag.get("data-src") or
                tag.get("data-lazy-src") or
                tag.get("srcset")
            )

            if not src:
                continue

            # trata srcset
            if "," in src:
                src = src.split(",")[0]
            if " " in src:
                src = src.split(" ")[0]

            #lógica de concatenação
            img_url = montar_url(url, src)

            if not img_url:
                continue

            # evita duplicadas
            if img_url not in vistos:
                imagens.append(img_url)
                vistos.add(img_url)

        dados.append({
            "url": url,
            "titulo": titulo,
            "imagens": imagens
        })

# 🔧 Gerar HTML final
html_final = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Resultados</title>
</head>
<body>
    <h1>Páginas coletadas</h1>
"""

for item in dados:
    html_final += f"""
    <h2>{item['titulo']}</h2>
    <p>
        <a href="{item['url']}">{item['url']}</a>
    </p>
    """

    for img in item['imagens']:
        html_final += f"""
        <img src="{img}" width="200" onerror="this.style.display='none'"><br>
        """
        
    html_final += "<hr>"

html_final += """
</body>
</html>
"""

#  Salvar arquivo
with open("resultado.html", "w", encoding="utf-8") as f:
    f.write(html_final)

print("Arquivo resultado.html gerado com sucesso!")