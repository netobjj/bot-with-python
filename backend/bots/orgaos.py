from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import csv
from globais import password, email, url_alfa_new_orgao
from aulas import realizar_login_alfa


def cadastra_orgaos():
    # abre o chrome
    chrome = webdriver.Chrome()
    chrome.maximize_window()
    realizar_login_alfa(chrome, email, password)

    nome_arquivo = "novos_orgaos.csv"
    caminho_completo = "C:/Users/Jose Euclides/Desktop/Programação/Python/Bot/backend/uploads/" + str(nome_arquivo)
    with open(caminho_completo, newline="", mode='r', encoding='utf-8-sig') as arquivo:
        leitor_csv = csv.reader(arquivo, delimiter=";")
        for index, linha in enumerate(leitor_csv):
            
            # Definição dos valores que colocaremos nos Campos
            sigla = linha[0]
            nome = linha[1]
            sigla_e_nome = str(sigla) + " - " + str(nome)
            preposicao = linha[2]
            meta_titulo = "Cursos para o Concurso " + str(preposicao) + " " + str(sigla) + " | Alfacon"
            meta_descricao = "Cursos do Alfacon para o Concurso " + str(preposicao) + " " + str(sigla_e_nome)

            chrome.get(url_alfa_new_orgao)

            try:
                chrome.find_element(By.ID, "entity_name").send_keys(sigla_e_nome)
                chrome.find_element(By.ID, "entity_meta_title").send_keys(meta_titulo)
                chrome.find_element(By.ID, "entity_meta_description").send_keys(meta_descricao)
                chrome.find_element(By.NAME, "_add_edit").click()
                print("Sucesso: " + str(sigla_e_nome))
            except: 
                print("Erro em " + str(sigla_e_nome))
            sleep(5)
        sleep(20)


def busca_id_orgao():
    # abre o chrome
    chrome = webdriver.Chrome()
    chrome.maximize_window()
    realizar_login_alfa(chrome, email, password)

    nome_arquivo = "novos_orgaos.csv"
    caminho_completo = "C:/Users/Jose Euclides/Desktop/Programação/Python/Bot/backend/uploads/" + str(nome_arquivo)
    with open(caminho_completo, newline="", mode='r', encoding='utf-8-sig') as arquivo:
        leitor_csv = csv.reader(arquivo, delimiter=";")
        for index, linha in enumerate(leitor_csv):
            
            # Definição dos valores que colocaremos nos Campos
            nome = linha[1]
            sigla = linha[0]
            sigla_e_nome = str(sigla) + " - " + str(nome)
            name_in_query = nome.replace(" ", "+")
            chrome.get("https://www.alfaconcursos.com.br/admin/entity?model_name=entity&utf8=%E2%9C%93&query=" + str(name_in_query))
            btn_view_orgao = chrome.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/div[2]/form[2]/table/tbody/tr/td[8]/ul/li[1]/a")
            link = btn_view_orgao.get_attribute('href')
            id_orgao = link.split("/")[5]
            print(id_orgao + " || " + sigla_e_nome)

            # 'https://www.alfaconcursos.com.br/admin/entity/124'
            sleep(5)
        sleep(20)


busca_id_orgao()