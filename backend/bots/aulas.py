from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from hashlib import md5
from time import sleep
import datetime
import csv


def definir_nova_situacao_aula(url, email, password, novo_status):
    # Inicializa o driver do Selenium (certifique-se de ter o driver apropriado instalado: Chrome, Firefox, etc.)
    driver = webdriver.Chrome()

    # Comando abaixo para Realizar o login
    driver.get(url)  # Abre a página de login
    email_input = driver.find_element(By.ID, "email")
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.NAME, "button")
    email_input.send_keys(email)  # Insere o nome de usuário
    password_input.send_keys(password)  # Insere a senha
    login_button.click()  # Clica no botão de login
    # Aguarda um intervalo de tempo para o login ser realizado completamente
    sleep(2)

    # Python/Bot/inativar_aulas.csv
    with open("Python/Bot/uploads/inativar_aulas.csv", newline="") as arquivo:
        leitor_csv = csv.reader(arquivo, delimiter=",")
        for index, linha in enumerate(leitor_csv):
            # Acessando os valores das colunas por índice
            id_aula = linha[0]
            link = str("https://www.alfaconcursos.com.br/admin/lesson/") + \
                str(id_aula) + str("/toggle_status_with_replace")
            driver.get(link)

            # Define o atual status da Aula
            status_aula = ''
            # Status: Inativa
            if (driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/ul/li[3]/a/i").get_attribute("class") == "circle fa fa-times-circle"):
                status_aula = "inativa"
            else:
                status_aula = "ativa"

            # Coloca o novo status que o user passou
            if (status_aula != novo_status):
                button_mudar_status = driver.find_element(By.XPATH, str(
                    '//*[@id="edit_lesson_') + str(id_aula) + str('"]/div[2]/button[1]'))
                button_mudar_status.click()
                print(str("Aula de id ") + id_aula + str(" ") + novo_status + str("da!"))
                sleep(1)
            else:
                print(str("Aula de id ") + id_aula + str(" não alterada!"))
            if (index >= 1):
                if (index % 59 == 0):
                    print("esperar 300s")
                    sleep(300)
                if (index % 159 == 0):
                    print("esperar 800s")
                    sleep(800)
                if (index % 499 == 0):
                    print("esperar 1000s")
                    sleep(1000)

    # Fecha o navegador
    driver.quit()


# Exemplo de uso
site_login = "https://www.alfaconcursos.com.br/sessions/new?scrollto=signin"
email = "jose.euclides@alfaconcursos.com.br"
password = "anleftao12"
definir_nova_situacao_aula(site_login, email, password, "ativa")
