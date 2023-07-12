from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from time import time
import datetime
import csv
import sys

sys.stdout.reconfigure(encoding='utf-8') # type: ignore
from globais import url_alfa_new_login, email, password


def realizar_login_alfa(naveg, email, password):
    # Comando abaixo para Realizar o login
    try:
        naveg.get(url_alfa_new_login)  # Abre a página de login
        email_input = naveg.find_element(By.ID, "email")
        password_input = naveg.find_element(By.ID, "password")
        login_button = naveg.find_element(By.NAME, "button")
        email_input.send_keys(email)  # Insere o nome de usuário
        password_input.send_keys(password)  # Insere a senha
        login_button.click()  # Clica no botão de login
        # Aguarda um intervalo de tempo para o login ser realizado completamente
        sleep(2)
        return "Logado com sucesso!"
    except:
        print ("Erro ao tentar logar!")

def ordenar():
    naveg = webdriver.Chrome()
    realizar_login_alfa(naveg, email, password)

    path_csv_questions = "C:/Users/Jose Euclides/Desktop/Programação/Python/Bot/backend/uploads/csv_questoes/"
    path_file = path_csv_questions + "arquivo.csv"
    with open(path_file, newline="", mode='r', encoding='utf-8') as file:
        reader_csv = csv.reader(file, delimiter=";")

        for index, linha in enumerate(reader_csv):
            # Acessando os valores das colunas por índice
            id_doc_question = linha[0]
            #id_edict = linha[1]
            sequence = linha[2]

    # ATENTO
    id_edict = 55

    url_edict_question = "https://www.alfaconcursos.com.br/admin_v2/edicts/edicts/" + str(id_edict) + "/questions"
    naveg.get(url_edict_question)

    # <li class="page-item last"><a class="page-link" href="/admin_v2/edicts/edicts/59/questions?page=15">Último »</a></li>
    ultima_pagina = naveg.find_element(By.CSS_SELECTOR, 'li.page-item.last > a.page-link')
    split_num_page = ultima_pagina.get_attribute('href').split("?page=")
    num_ult_page = int(split_num_page[1])
    print(num_ult_page)

    list_url_questions = []
    page = 1

    # Percorre a page para pegar as questoes do edital
    while page <= num_ult_page:
        naveg.get(url_edict_question + '?page=' + str(page))
        
        
        # Pega as questões de cada Página
        elements_questions = naveg.find_elements(By.CSS_SELECTOR, 'a.btn.btn-show[href^="/admin_v2/edicts/edicts/' + str(id_edict) + '/questions/"]')
        # <a class="btn btn-show" href="/admin_v2/edicts/edicts/59/questions/1348">Exibir</a>
        for e in elements_questions:
            list_url_questions.append(e.get_attribute('href'))

        page += 1

    print(str(len(list_url_questions)) + " questões")

    for url_question in list_url_questions:
        naveg.get(url_question)

        # Get sequence question
        sequence_question = naveg.find_element(By.CSS_SELECTOR, 'span.bg-primary > span.bg-secondary').text.split("nº")[1]
        num_seq = int(sequence_question)
        
        # Get ulr doc_google_gerenciador
        url_doc_google = naveg.find_element(By.CSS_SELECTOR, 'a[href^="https://docs.google.com/document/d/"]').get_attribute('href') # https://docs.google.com/document/d/11hbz8MSwtrX0AGrj4oQSX3ul9qaieLuPlK97KwXKbvM/edit
        print()
        # Pegar o link do doc google no gerenciador
            # comparo esses dois links e num_seq pra ver se é a mesma sequência
            # Se for sequência diferente, altero no gerenciador para a sequência da Planilha
        # 
        # 
        # 
        #


        # PRÓXIMOS PASSOS

        # pegar a lista de docs_google do edital

         


        # <span class="badge bg-primary">Prova Objetiva - Papiloscopista</span>
        # <span class="badge bg-secondary">nº 8</span>



    

            
   
                 
            

ordenar()