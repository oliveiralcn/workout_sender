import sys
import json
import socket
import pywhatkit as kit
from PyQt5.QtCore import QThread, QSocketNotifier, QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QPushButton, QGridLayout, QTextEdit, QLineEdit

# Abrindo .json com os modelos de treinos
with open('treinos.json', 'r', encoding='utf-8') as t:
    treinos = json.load(t)
# Fechar o arquivo
t.close()

class MinhaThread(QThread):
    notificador = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.notificador_socket = QSocketNotifier(self.socket.fileno(), QSocketNotifier.Read)
        self.notificador_socket.activated.connect(self.ler_socket)

    def run(self):
        self.socket.bind(('localhost', 8888))
        self.exec_()

    def ler_socket(self, socket):
        data, addr = socket.recvfrom(1024)
        self.notificador.emit(data)

class Janela(QWidget):
    def __init__(self):
        super().__init__()

        # Configurar a janela
        self.setWindowTitle('Enviador de treinos')
        self.setGeometry(20, 20, 500, 90)

        # Criar as widgets
        self.nome_label = QLabel('Nome social:')
        self.nome_textbox = QLineEdit()

        self.telefone_label = QLabel('Whatsapp:')
        self.telefone_textbox = QLineEdit()

        self.sexo_label = QLabel('Selecione o sexo:')
        self.sexo_combo = QComboBox()
        self.sexo_combo.addItems(['Homem', 'Mulher'])

        self.nivel_label = QLabel('Selecione o nível:')
        self.nivel_combo = QComboBox()
        self.nivel_combo.addItems(['Iniciante', 'Intermediario', 'Avancado'])

        self.enviar_botao = QPushButton('Enviar pelo WhatsApp')

        separador1 = QLabel()
        separador1.setFixedSize(1, 50)
        separador1.setStyleSheet('background-color: black')

        separador2 = QLabel()
        separador2.setFixedSize(1, 50)
        separador2.setStyleSheet('background-color: black')

        # Configurar o layout
        layout = QGridLayout()
        layout.addWidget(self.nome_label, 0, 0)
        layout.addWidget(self.nome_textbox, 0, 1, 1, 4)
        layout.addWidget(self.telefone_label, 1, 0)
        layout.addWidget(self.telefone_textbox, 1, 1, 1, 4)
        layout.addWidget(self.sexo_label, 2, 0)
        layout.addWidget(self.sexo_combo, 3, 0)
        layout.addWidget(separador1, 2, 1, 4, 1)
        layout.addWidget(self.nivel_label, 2, 2)
        layout.addWidget(self.nivel_combo, 3, 2)
        layout.addWidget(separador2, 2, 3, 4, 1)
        layout.addWidget(self.enviar_botao, 2, 4, 3, 4)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 0)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 0)
        layout.setColumnStretch(4, 1)
        self.setLayout(layout)

        # Conectar sinais e slots
        self.sexo_combo.currentIndexChanged.connect(self.sexo_selecionado)
        self.nivel_combo.currentIndexChanged.connect(self.nivel_selecionado)
        self.enviar_botao.clicked.connect(self.enviar)

    def sexo_selecionado(self, index):
        self.sexo = self.sexo_combo.currentText()
        

    def nivel_selecionado(self, index):
        self.nivel = self.nivel_combo.currentText()

    def enviar(self):
        nome = self.nome_textbox.text()
        nome = nome.lower().title().strip()

        telefone = self.telefone_textbox.text()
        telefone = telefone.strip()
        numero_celular_completo = f"+55{telefone}"


        sexo = self.sexo_combo.currentText()
        sexo = sexo.lower().strip()

        nivel = self.nivel_combo.currentText()
        nivel = nivel.lower().strip()

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


        kit.sendwhatmsg_instantly(numero_celular_completo, mensagem)


# Inicializar o aplicativo
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Criar e exibir a janela
    janela = Janela()
    janela.show()

    # Executar o loop de eventos do aplicativo
    sys.exit(app.exec_())
