from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from time import time
import numpy as np
import datetime
import csv
import sys

sys.path.append("../../backend")
sys.stdout.reconfigure(encoding='utf-8') # type: ignore
from globais import url_alfa_new_login, email, password
from backend.functions.sign_in_alfa import realizar_login_alfa

def ordenar():
    naveg = webdriver.Chrome()
    realizar_login_alfa(naveg, email, password)

    # Abasteçe dados do arquivo.csv em uma lista
    id_edict = ''
    array_questions_csv = []
    path_csv_questions = "C:/Users/Jose Euclides/Desktop/Programação/Python/Bot/backend/uploads/questoes/"
    path_file = path_csv_questions + "sequence.csv"
    with open(path_file, newline="", mode='r', encoding='utf-8') as file:
        reader_csv = csv.reader(file, delimiter=";")
            
        for index, linha in enumerate(reader_csv):
            id_doc_question = linha[0]
            id_edict = linha[1]
            sequence = int(linha[2])
            array_questions_csv.append([id_doc_question, sequence])

    url_edict_question = "https://www.alfaconcursos.com.br/admin_v2/edicts/edicts/" + str(id_edict) + "/questions"
    naveg.get(url_edict_question)

    # <li class="page-item last"><a class="page-link" href="/admin_v2/edicts/edicts/59/questions?page=15">Último »</a></li>
    ultima_pagina = naveg.find_element(By.CSS_SELECTOR, 'li.page-item.last > a.page-link')
    split_num_page = ultima_pagina.get_attribute('href').split("?page=")
    num_ult_page = int(split_num_page[1])
    print(num_ult_page)

    list_questions = []
    page = 1

    # Percorre a page para pegar as questoes do edital
    while page <= num_ult_page:
        naveg.get(url_edict_question + '?page=' + str(page))
        
        
        # Pega as questões de cada Página
        elements_questions = naveg.find_elements(By.CSS_SELECTOR, 'a.btn.btn-show[href^="/admin_v2/edicts/edicts/' + str(id_edict) + '/questions/"]')
        # <a class="btn btn-show" href="/admin_v2/edicts/edicts/59/questions/1348">Exibir</a>
        for e in elements_questions:
            list_questions.append(e.get_attribute('href'))

        page += 1

    print(str(len(list_questions)) + " questões")
    # print(list_questions)


    # Colocar ordem correta
    new_list_question = []
    for index, url_question in enumerate(list_questions):
        try:
            naveg.get(url_question)

            # Get sequence questionn
            sequence_question_site = naveg.find_element(By.CSS_SELECTOR, 'span.badge.bg-primary > span.badge.bg-secondary').text.split("nº")[1]
            num_seq_site = int(sequence_question_site)

            # url_doc_google = naveg.find_element(By.LINK_TEXT, 'Documento do Google').get_attribute('href').split('/')[5]
            url_doc_google = naveg.find_element(By.CSS_SELECTOR, 'a[href^="https://docs.google.com/document/d/"]').get_attribute('href')
            id_doc_google = url_doc_google.split('/')[5]
            new_list_question.append([url_question, id_doc_google, num_seq_site])

        except:
            naveg.save_screenshot(path_csv_questions + str(datetime.datetime.now()) + "foto.png")

    print("Colheu todos os docs google!")
    # Go through the array questions csv
    for value in array_questions_csv:
        id_doc_question_csv = value[0]
        sequence_csv = value[1]
        for question_url_e_id_doc in new_list_question:
            url_question = question_url_e_id_doc[0]
            id_doc_google = question_url_e_id_doc[1]
            sequence_site = question_url_e_id_doc[2]

            try:
                #print(id_doc_question_csv)
                #print(id_doc_google)
                if id_doc_question_csv == id_doc_google:
                    sleep(1)
                    naveg.get(url_question)
                    naveg.refresh()
                    
                    # <a class="text-light text-bold" title="Editar" href="/admin_v2/edicts/edicts/55/questions/2579/phase_questions/2590/edit"><i class="fa fa-pencil"></i></a>
                    url_edit_order = naveg.find_element(By.CSS_SELECTOR, 'span.badge.bg-secondary > a[href*="/phase_questions/"][title="Editar"]').get_attribute('href')
                    naveg.get(url_edit_order)

                    input_new_order = naveg.find_element(By.CSS_SELECTOR, 'input[id="edicts_phase_question_question_number"]')
                    input_commit_att = naveg.find_element(By.CSS_SELECTOR, 'input[name="commit"][type="submit"]')
                    
                    input_new_order.send_keys(Keys.CONTROL + "a")
                    input_new_order.send_keys(Keys.DELETE)
                    input_new_order.send_keys(sequence_csv)     
                    input_commit_att.click()
                    
                    print("Alterado! url: " + str(url_question) + " - new_order: " + str(sequence_csv))
                    # sleep(1)
            except:
                naveg.save_screenshot(path_csv_questions + str(datetime.datetime.now()) + "foto.png")


ordenar()