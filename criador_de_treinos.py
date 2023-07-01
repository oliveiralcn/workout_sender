import sys
import json
import socket
import pywhatkit as kit
from PyQt5.QtCore import QThread, QSocketNotifier, QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QPushButton, QGridLayout, QTextEdit, QLineEdit

treinos = {
    "homem" : {
        "iniciante":{
            "A":[
                "Supino reto - 3 x 8/12",
                "Supino inclinado - 3 x 8/12",
                "Voador - 3 x 10/15",
                "Triceps Francês - 3 x 8/12",
                "Triceps na polia com corda - 3 x 10/15",
                "Triceps testa com halteres - 3 x 8/12",
                "Elevação lateral - 3 x 12/15",
                "Elevação frontal - 3 x 12/15"
            ],
            "B":[
                "Agachamento Livre - 3 x 15/20",
                "Leg Press - 3 x 12/15",
                "Hack - 3 x 8/12",
                "Cadeira extensora - 3 x 12/15",
                "Mesa Flexora - 3 x 10/12",
                "Cadeira Flexora - 3 x 12/15",
                "Cadeira Adutora - 3 x 12/15",
                "Cadeira Abdutora - 3 x 12/15",
                "Panturrilha em pé - 3 x 15/20",
                "Panturrilha sentado - 3 x 15/20"
            ],
            "C":[
                "Puxada alta aberta - 3 x 8/15",
                "Puxada alta fechada - 3 x 8/15",
                "Remada baixa - 3 x 12/15",
                "Pull Down - 3 x 10/15",
                "Rosca Direta - 3 x 10/15",
                "Rosca Alternada - 3 x 10/12",
                "Biceps no Banco Scoth - 3 x 8/12"
            ]
        },
        "intermediario":{
            "A":[
                "Supino inclinado - 3 x 8/15",
                "Crucifixo inclinado - 3 x 10/15",
                "Supino reto - 3 x 10/12",
                "Voador - 4 x 8+15(reduz a carga)",
                "Triceps Francês na polia baixa- 3 x 12/15",
                "Triceps Coice - 3 x 10/12",
                "Tríceps testa com barra - 3 x 10/15",
                "Tríceps cruzado na polia média"
            ],
            "B":[
                "Cadeira extensora - 3 x 12/15",
                "Agachamento Livre - 3 x 15/20",
                "Leg Press - 3 x 12/15",
                "Hack - 3 x 8/12",
                "Afundo - 3 x 10/15",
                "Cadeira Flexora - 3 x 12/15",
                "Mesa Flexora - 3 x 10/15",
                "Cadeira Abdutora - 3 x 12/15",
                "Panturrilha em pé - 3 x 15/20",
                "Panturrilha sentado - 3 x 15/20"
            ],
            "C":[
                "Puxada alta aberta - 3 x 8/15",
                "Puxada alta pegada neutra - 3 x 8/15",
                "Remada articulada pegada neutra - 3 x 12/15",
                "Remada articulada pegada pronada - 3 x 8/12",
                "Pull Down - 3 x 10/15",
                "Rosca Direta - 3 x 10/15",
                "Rosca isométrica - 3 x 10/12",
                "Biceps no Banco Scoth - 3 x 8/12"
            ],
            "D":[
                "Elevação lateral - 3 x 10/15",
                "Elevação frontal com anilha - 3 x 10/15",
                "Voador invertido - 3 x 12/15",
                "Desenvolvimento - 3 x 10/15",
                "Abdominal supra - 3 x 15/20",
                "Abdominal infra - 3 x 10/15",
                "Prancha isométrica - 3 x 40/50 segundos"
            ]
        },
        "avancado":{
            "A":[
                "Supino inclinado - 3 x 8/15",
                "Puxada alta aberta - 3 x 10/12",
                "Crucifixo inclinado - 3 x 10/15",
                "Puxada alta pegada neutra - 3 x 10/12",
                "Supino reto - 3 x 10/15",
                "Remada articulada pegada neutra - 3 x 12",
                "Voador - 4 x 10|10|10(reduz a carga)",
                "Remada baixa inclinada com barra - 3 x 12/15",
                "Cross polia alta - 3 x 12/15",
                "Remada articulada pegada pronada - 3 x 10/12",
                "Flexão de braço - 3 x 10/15 (pode ser executada no joelho)",
                "Cruxifixo invertido - 3 x 10/12"
            ],
            "B":[
                "Agachamento Livre - 3 x 15/20",
                "Leg Press - 3 x 12/15",
                "Cadeira extensora - 3 x 8|12|20 (dropando carga)",
                "Agachamento sumô - 3 x 15 + 30s de isometria",
                "Hack - 3 x 8/12",
                "Afundo - 3 x 10/15",
                "Extensão de joelhos no colchonete - 3 x 15/20",
                "Panturrilha sentado - 3 x 15 + Panturrilha em pé - 3 x 20"
            ],
            "C":[
                "Rosca Direta - 3 x 10/15",
                "Triceps francês - 3 x 10/15",
                "Rosca isométrica - 3 x 10/12",
                "Triceps testa - 3 x 10/15",
                "Biceps no banco inclinado - 3 x 10/12",
                "Triceps na polia com barra - 3 x 12/15",
                "Biceps no Banco Scoth - 3 x 8/12",
                "Triceps coice - 3 x 10/15"
            ],
            "D":[
                "Cadeira flexora - 3 x 15/20",
                "Mesa flexora - 3 x 10/15",
                "Flexão de joelhos em pé - 3 x 10/12",
                "Stiff - 3 x 12/15",
                "Leg (pés altos) - 3 x 12/15 + Bulgaro - 3 x 15",
                "Elevação pélvica - 3 x 10/15",
                "Cadeira abdutora - 3 x 12",
                "Cadeira adutora - 3 x 12"
            ],
            "E":[
                "Elevação lateral - 12 + (série especial '21')",
                "Elevação lateral inclinada - 3 x 12",
                "Elevação frontal na polia baixa - 3 x 12",
                "Desenvolvimento - 3 x 15",
                "Pull face - 3 x 12",
                "Crucifixo invertido (adaptado para os ombros) - 3 x 12",
                "Abdominal supra com pés elevados - 3 x 20",
                "Abdominal infra com pernas extendidas - 3 x 15",
                "Giro russo - 3 x 30/40"
            ]
        }
    },
    "mulher":{
        "iniciante":{
            "A":[
                "Agachamento sumô - 3 x 10/15",
                "Cadeira extensora - 3 x 10/15",
                "Leg - 3 x 8/12",
                "Hack squat - 3 x 8/12",
                "Cadeira flexora - 3 x 12/15",
                "Mesa flexora - 3 x 10/12",
                "Cadeira adutora - 3 x 12/15",
                "Cadeira abdutora - 3 x 12/15",
                "Panturrilha em pé - 3 x 15/20"
            ],
            "B":[
                "Supino inclinado - 3 x 15",
                "Voador - 3 x 15",
                "Puxada alta aberta - 3 x 12/15",
                "Remada baixa com o triangulo - 3 x 15",
                "Rosca direta - 3 x 12",
                "Rosca alternada - 3 x 12",
                "Triceps francês - 3 x 10/12",
                "Triceps na polia com a corda - 3 x 15",
                "Elevação lateral - 3 x 12",
                "Elevação frontal - 3 x 12"
            ]
        },
        "intermediario":{
            "A":[
                "Agachamento livre - 3 x 15",
                "Cadeira extensora - 3 x 10/15",
                "Agachamento sumô - 3 x 10/15",
                "Leg - 3 x 12/15",
                "Afundo - 3 x 15",
                "Hack - 3 x 12",
                "Panturrilha sentada - 3 x 15",
                "Panturrilha em pé - 3 x 15/20"
            ],
            "B":[
                "Supino inclinado - 3 x 15",
                "Voador - 3 x 15",
                "Puxada alta aberta - 3 x 12/15",
                "Remada baixa com o triangulo - 3 x 15",
                "Rosca direta - 3 x 12",
                "Rosca alternada - 3 x 12",
                "Triceps francês - 3 x 10/12",
                "Triceps na polia com a corda - 3 x 15",
                "Elevação lateral - 3 x 12",
                "Elevação frontal - 3 x 12"
            ],
            "C":[
                "Cadeira flexora - 3 x 15",
                "Mesa flexora - 3 x 15",
                "Stiff - 3 x 12/15",
                "Elevação pélvica - 3 x 15",
                "Cadeira abdutora - 3 x 15",
                "Cadeira adutora - 3 x 15",
                "Coice - 3 x 12",
                "Passadas laterias com miniband - 4 x 20"
            ]
        },
        "avancado":{
            "A":[
                "Agachamento livre - 3 x 15",
                "Cadeira extensora - 3 x 8|12|15 (dropando carga)",
                "Cadeira adutora - 3 x 15",
                "Agachamento sumô - 3 x 10/15 + Afundo - 3 x 15",
                "Hack squat- 3 x 12",
                "Leg - 3 x 12/15",
                "Flexão de quadril - 3 x 15",
                "Extensão de joelhos no colchonete - 3 x 20",
                "Panturrilha sentada - 3 x 15 + Panturrilha em pé - 3 x 20"
            ],
            "B":[
                "Rosca direta - 3 x 12",
                "Rosca alternada - 3 x 12",
                "Triceps francês - 3 x 10/12",
                "Triceps na polia com a corda - 3 x 15",
                "Elevação lateral - 3 x 12",
                "Elevação frontal - 3 x 12",
                "Abdominal supra com pés elevados - 3 x 30",
                "Abdominal infra com pernas extendidas - 3 x 20",
                "Giro russo - 3 x 30"
            ],
            "C":[
                "Cadeira flexora - 4 x 20",
                "Mesa flexora - 3 x 15|20 (reduz a carga)",
                "Flexão de joelhos em pé - 3 x 15",
                "Stiff - 3 x 15",
                "Passadas laterias com miniband - 4 x 20",
                "Cadeira abdutora - 3 x 15|20",
                "Elevação pélvica - 3 x 15",
                "Coice - 3 x 12 + Abdução na polia baixa  - 3 x 10",
                "Bulgaro - 3 x 20"
            ],
            "D":[
                "Supino inclinado - 3 x 15",
                "Supino reto - 3 x 15",
                "Voador - 3 x 15",
                "Remada baixa inclinada - 3 x 12",
                "Puxada alta aberta - 3 x 15",
                "Remada articulada pegada pronada - 3 x 12",
                "Voador invertido - 3 x 15",
                "Pull down - 3 x 15"
            ],
            "E":[
                "Cadeira extensora - 4 x 20",
                "Cadeira flexora - 3 x 20",
                "Agachamento livre - 3 x 12",
                "Cadeira abdutora - 3 x 20",
                "Hack squat - 3 x 15",
                "Terra squat - 3 x 15",
                "Leg - 3 x 15",
                "Coice na polia - 3 x 15"
            ]
        }
    }
} 


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
