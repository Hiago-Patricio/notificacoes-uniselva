import requests
import dotenv
import os
import bs4
from win10toast import ToastNotifier


def notifica_sobre_novos_editais():
    toaster = ToastNotifier()
    toaster.show_toast('Estágio', 'Há novo(s) edital(is).')


def obtem_html_site() -> str:
    link = os.getenv('LINK')
    quantidade_tentativas_maximas = int(os.getenv('TENTATIVAS'))
    tentativas = 1
    response = requests.get(link)

    while not response.ok and tentativas <= quantidade_tentativas_maximas:
        response = requests.get(link)
        tentativas += 1

    return response.text if response.ok else None


def obtem_editais_do_site(html: str) -> list:
    if html is None:
        return []

    soup = bs4.BeautifulSoup(html, 'html.parser')
    editais = [edital.contents[0].strip() for edital in soup.select('.informacaoGeral .espacamentoTituloImagemIcone')]
    return editais


def verifica_se_existem_novos_editais(editais: list):
    path = os.getenv('ARQUIVO_DE_EDITAIS')

    editais_velhos = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as file:
            editais_velhos = file.readlines()

    novos_editais = [edital + '\n' for edital in editais if edital + '\n' not in editais_velhos]

    with open(path, 'a+', encoding='utf-8') as file:
        file.writelines(novos_editais)

    return novos_editais != []


if __name__ == '__main__':
    dotenv.load_dotenv()
    html = obtem_html_site()
    editais = obtem_editais_do_site(html)

    if verifica_se_existem_novos_editais(editais):
        notifica_sobre_novos_editais()
