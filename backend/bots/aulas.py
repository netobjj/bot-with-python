from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from time import time
import datetime
import csv
import sys
from globais import url_alfa_new_login, email, password

# sys.stdout.reconfigure(encoding='utf-8')

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
        

def definir_nova_situacao_aulas(novo_status, nome_arquivo):
    # Inicializa o navegador do Selenium (certifique-se de ter o navegador apropriado instalado: Chrome, Firefox, etc.)
    navegador = webdriver.Chrome()
    realizar_login_alfa(navegador, email, password)

    start = time()
    # Python/Bot/inativar_aulas.csv
    path_uploads = "C:/Users/Jose Euclides/Desktop/Programação/Python/Bot/backend/uploads/"
    path_file = path_uploads + str(nome_arquivo)
    with open(path_file, newline="") as arquivo, open(path_uploads + str("relatorio.csv"), "w", newline="", encoding="utf-8") as file_report:
        leitor_csv = csv.reader(arquivo, delimiter=",")
        writer_csv = csv.writer(file_report)

        qtd_alteracoes = 0
        qtd_alteracoes_total = 0
        for index, linha in enumerate(leitor_csv):
            # Acessando os valores das colunas por índice
            id_aula = linha[0]
            link = str("https://www.alfaconcursos.com.br/admin/lesson/") + \
                str(id_aula) + str("/toggle_status_with_replace")
            navegador.get(link)

            # Define o atual status da Aula
            status_aula = ''
            # Status: Inativa
            if (navegador.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/ul/li[3]/a/i").get_attribute("class") == "circle fa fa-times-circle"):
                status_aula = "inativa"
            else:
                status_aula = "ativa"

            # Coloca o novo status que o user passou
            if (status_aula != novo_status):
                button_mudar_status = navegador.find_element(By.XPATH, str(
                    '//*[@id="edit_lesson_') + str(id_aula) + str('"]/div[2]/button[1]'))
                button_mudar_status.click()
                qtd_alteracoes += 1
                qtd_alteracoes_total += 1
                writer_csv.writerow([id_aula, novo_status + "da"])
                sleep(0.75)
            else:
                writer_csv.writerow([id_aula, "not changed!"])

            if (index >= 1 and qtd_alteracoes > 100):
                qtd_alteracoes = 0
                min = 60 # 60 segundos

                print(str((time() - start) / 60) + str(" minutos por 100 alterações"))
                start = time()
                sleep((5 * min))
                if (index % 250 == 0):
                    print(str("oba! +250 aulas, esperar 2min (") + str(datetime.datetime.now()) + ")")
                    sleep(120)
                if (index % 1000 == 0):
                    print(str("oba! +1000 aulas, esperar +3min (") + str(datetime.datetime.now()) + ")")
                    sleep(300) # mais 300 s de espera

    # Fecha o navegador
    navegador.quit()


# Exemplo de uso
def executar_funcoes():
    definir_nova_situacao_aulas("ativa", "inativar_aulas.csv")

executar_funcoes()