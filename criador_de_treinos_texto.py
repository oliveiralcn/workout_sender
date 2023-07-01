import json
from colorama import init, Fore, Style
import os
import pywhatkit as kit
import pyautogui

init(autoreset=True)

def limpar_tela():
    os.system('clear')

def receber_dados():
    limpar_tela()
    repeticoes = int(input("Quantos treinos quer enviar? "))
    alunos = []
    for rep in range(repeticoes):
        aluno = {}
        limpar_tela()
        aluno['nome'] = str(input("Digite o nome do aluno para tornar a mensagem mais pessoal: "))
        
        limpar_tela()
        area_celular = str(input("Digite o código de área do celular do aluno: "))
        limpar_tela()
        numero_celular = str(input("Digite o numero celular sem traços: "))
        aluno['celular'] = f"+55{area_celular}{numero_celular}"

        limpar_tela()
        while True:
            print('Escolha o sexo do aluno: \n   1 - Masculino;\n   2 - Feminino;')
            resposta1 = int(input("Resposta: "))
            if resposta1 == 1:
                aluno['sexo'] = "homem"
                limpar_tela()
                break
            elif resposta1 == 2:
                aluno['sexo'] = "mulher"
                limpar_tela()
                break
            else:
                limpar_tela()
                print(Fore.MAGENTA + Style.BRIGHT + "Alternativa inválida!" + Style.RESET_ALL)

        while True:
            print('Escolha o nível do aluno: \n   1 - Iniciante;\n   2 - Intermediário; \n   3 - Avançado;')
            resposta2 = int(input("Resposta: "))
            if resposta2 == 1:
                aluno['nivel'] = "iniciante"
                limpar_tela()  
                break
            elif resposta2 == 2:
                aluno['nivel'] = "intermediario"
                limpar_tela()
                break
            elif resposta2 == 3:
                aluno['nivel'] = "avancado"
                limpar_tela()
                break
            else:
                limpar_tela()
                print(Fore.MAGENTA + Style.BRIGHT + "Alternativa inválida!" + Style.RESET_ALL)

        alunos.append(aluno)
    return(alunos)
        

# Abrir o arquivo com os modelos de treinos
with open('treinos.json', 'r', encoding='utf-8') as t:
    treinos = json.load(t)

# Fechar o arquivo
t.close()

alunos = receber_dados()

for aluno in alunos:
    limpar_tela()
    nome = aluno['nome']
    celular = aluno['celular']
    sexo = aluno['sexo']
    nivel = aluno['nivel']

    print(Fore.BLUE + Style.BRIGHT + f'Enviando mensagem para {nome}' + Style.RESET_ALL)


    mensagem = f'**Olá {nome}, seja bem-vindo à família RM Arena Fitness! Aqui está sua ficha de treino:** \n'
    mensagem+="_Não esqueça de alongar e aquecer bem os músculos antes de cada treino!_ \n"
    mensagem+= " \n_**Os treinos devem seguir uma ordem, iniciando-se a segunda feira com o treino que vem depois do último treino executado._ \n_Ex: sábado fez o treino B, então segunda é treino C._ \n"

    plano_de_treino = treinos[sexo][nivel]
    for dia in plano_de_treino:
        mensagem += 40*"="
        mensagem += f'\n \n*TREINO - {dia}* \n \n'
        contador = 1
        for exercicio in plano_de_treino[dia]:
            mensagem += f'   {contador:02} - {exercicio}; \n'
            contador+=1
        mensagem += "\n"

    kit.sendwhatmsg_instantly(celular, mensagem)
    
    limpar_tela()

    print(Fore.GREEN + Style.BRIGHT + f"O treino foi enviado para o {nome}" + Style.RESET_ALL)

    pyautogui.sleep(4)
    
    pyautogui.hotkey('ctrl','w')
