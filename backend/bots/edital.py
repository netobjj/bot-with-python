from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from time import time
import datetime
import csv
import sys

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

def edital():
    print("Edital")

