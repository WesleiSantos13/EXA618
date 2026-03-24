import urllib.request
from bs4 import BeautifulSoup

dados = []

# Ler os links
with open("seeds.txt", "r", encoding="utf-8") as f:
    for linha in f:
        url = linha.strip()
        print("Processando:", url)

        
        page = urllib.request.urlopen(url)
        html = page.read().decode('utf-8')
        soup = BeautifulSoup(html, 'lxml')

        titulo = soup.title.string if soup.title else "Sem título"
        imagens = [img.attrs.get("src") for img in soup.find_all('img')]

        dados.append({
                "url": url,
                "titulo": titulo,
                "imagens": imagens
            })

print(dados)

# 🔧 Gerar HTML final
html_final = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Resultados</title>
</head>
<body>
    <h1>Páginas coletadas</h1>
"""

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
        <img src="{img}" width="200"><br>
        """

    html_final += """
    <hr>
    """

html_final += """
</body>
</html>
"""

# Salvar arquivo
with open("resultado.html", "w", encoding="utf-8") as f:
    f.write(html_final)

print("Arquivo resultado.html gerado com sucesso!")

