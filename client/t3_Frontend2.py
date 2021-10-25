from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout,\
    QFileDialog, QMessageBox
from PyQt5.QtWidgets import QPushButton, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from emojis import emojis
from PyQt5.QtWidgets import (QLabel, QWidget)
from PyQt5.QtCore import pyqtSignal
import base64
import random
import time


window_name2, base_class2 = uic.loadUiType("gamewindow.ui")
window_name3, base_class3 = uic.loadUiType("salawindow.ui")


class GameWindow(window_name2, base_class2):

    enter_pressed = pyqtSignal()
    empezar_juego_signal = pyqtSignal()
    actualizar_label_signal = pyqtSignal(list)
    cuadrado_completo_signal = pyqtSignal(list)
    pos_update_signal = pyqtSignal(list)
    tam_m_signal = pyqtSignal(int)
    tam_n_signal = pyqtSignal(int)

    def __init__(self, servidor_signal, terminar_conexion_signal,
                 chat_update_signal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        # Datos de la partida
        self.nro_sala = None
        self.lider_sala = None
        self.nombre_usuario = None
        self.m = None
        self.n = None

        # Señales
        self.servidor_signal = servidor_signal
        self.terminar_conexion_signal = terminar_conexion_signal
        self.chat_update_signal = chat_update_signal

        # Conectando estas señales
        self.chat_update_signal.connect(self.actualizar_chat)

        # Log
        self.chat_log = ""

        # Label del log
        self.chat_log_label = QLabel("", self)
        chat_log_label_font = self.chat_log_label.font()
        chat_log_label_font.setPointSize(12)
        self.chat_log_label.setFont(chat_log_label_font)
        self.chat_log_label.setStyleSheet("color: darkblue")

        self.BEnviar.clicked.connect(self.manejo_boton)
        self.enter_pressed.connect(self.manejo_boton)
        self.Bsalir.clicked.connect(self.boton_salir)

        # instancio foto de perfil incognita
        self.foto_perfil.setPixmap(QPixmap("foto_incognito.png").scaled(80, 80))
        self.init_setup()
        self.init_setup_emojis()

        # del juego
        self.label_juego = []
        self.label_horizontal = []
        self.label_vertical = []
        self.indicadores_label = {}

        # conectando señales del juego
        self.empezar_juego_signal.connect(self.empezar_juego)
        self.actualizar_label_signal.connect(self.cambiar_estado_label)
        self.cuadrado_completo_signal.connect(self.label_cuadrado_completado)
        self.pos_update_signal.connect(self.update_pos)
        self.tam_m_signal.connect(self.tam_m)
        self.tam_n_signal.connect(self.tam_n)

        # diccioonario con los labels de las posiciones
        self.dict_pos = {1: self.pos_1, 2: self.pos_2, 3: self.pos_3,
                         4: self.pos_4, 5: self.pos_5, 6: self.pos_6,
                         7: self.pos_7, 8: self.pos_8, 9: self.pos_9,
                         10: self.pos_10, 11: self.pos_11, 12: self.pos_12,
                         13: self.pos_13, 14: self.pos_14, 15: self.pos_15}

    def init_setup(self):

        self.chat_log_label.setGeometry(560, 260, 230, 220)
        self.users_scroll.setWidget(self.chat_log_label)
        self.chat_log_label.setAlignment(Qt.AlignTop)

    def init_setup_emojis(self):
        self.Bemoji1.setText("\U0001f603")
        self.Bemoji2.setText("\U0001F4A9")
        self.Bemoji3.setText("\U0001F44B")
        self.Bemoji4.setText("\U0001F618")
        self.Bemoji5.setText("\U0001F622")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.enter_pressed.emit()

    def manejo_boton(self):
        mensaje = {"status": "mensaje",
                   "data": {"usuario": self.nombre_usuario,
                            "contenido": self.lineEditChat.text()}}
        self.servidor_signal.emit(mensaje)
        self.lineEditChat.setText("")

    def actualizar_chat(self, contenido):
        print(contenido)
        self.chat_log += f"{contenido}\n"
        for llave in emojis.keys():
            self.chat_log = self.chat_log.replace(llave, emojis[llave])
        self.chat_log_label.setText(self.chat_log)

    def crear_tablero(self, m, n):
        px, py, tam, rect, l_gen, pos_id = algoritmo(m, n)
        # lista que se usara para crear los labels de al medio para los
        # identificadores
        lista = [x for x in range(1, (n-1)*(m-1)+1)]
        # esto crea los puntos
        for j in range(m):
            for i in range(n):
                lab = QLabel(self)
                lab.setGeometry(px + l_gen*i, py + l_gen*j, tam, tam)
                lab.setPixmap(QPixmap("dot.png").scaled(tam, tam))
                self.label_juego.append(lab)
                lab.show()
        # esto crea los labels horizontales
        for j in range(m):
            for i in range(n-1):
                lab2 = LabelLineaH(self)
                lab2.move((px + tam) + l_gen*i, (py + tam/4) + l_gen*j)
                lab2.inicio = (i, j)
                lab2.final = (i+1, j)
                lab2.horizontal_signal.connect(self.avisar_cambio_label)
                self.label_horizontal.append(lab2)
        # esto crea los label vericales
        for j in range(m-1):
            for i in range(n):
                lab3 = LabelLineaV(self)
                lab3.move((px + tam/4) + l_gen*i, (py + tam) + l_gen*j)
                lab3.inicio = (i, j)
                lab3.final = (i, j + 1)
                lab3.vertical_signal.connect(self.avisar_cambio_label)
                self.label_vertical.append(lab3)
        for j in range(m-1):
            for i in range(n-1):
                ide = lista.pop(0)
                id_label = QLabel(self)
                id_label.setAlignment(Qt.AlignCenter)
                id_label.setGeometry((px + l_gen * i) + pos_id, (py + l_gen * j)
                                     + pos_id, tam, tam)
                self.indicadores_label[ide] = id_label
                id_label.show()

    def boton_salir(self):
        mensaje = {"status": "salir_sala"}
        self.servidor_signal.emit(mensaje)

    def borrar_chat(self):
        self.chat_log = ""
        self.chat_log_label.setText(self.chat_log)

    def actualizar_sala_lider(self, lista):
        self.nro_sala = lista[0]
        self.lider_sala = lista[1]
        self.nro_sala_label.setText(f"Sala: {self.nro_sala}")
        self.lider_sala_label.setText(f"Jefe: {self.lider_sala}")
        if self.nombre_usuario == self.lider_sala:
            self.empezar_juego_boton.setEnabled(True)
            # self.empezar_juego_boton.clicked.connect(self.empezar_juego)
            self.empezar_juego_boton.clicked.connect(self.avisar_comienzo_juego)
        elif self.nombre_usuario != self.lider_sala:
            self.empezar_juego_boton.setEnabled(False)

    def empezar_juego(self):
        self.crear_tablero(self.m, self.n)
        self.empezar_juego_boton.setEnabled(False)

    def avisar_comienzo_juego(self):
        time.sleep(0.01)
        mensaje = {"status": "juego", "tipo": "empezar"}
        self.servidor_signal.emit(mensaje)

    def avisar_cambio_label(self, lista):
        mensaje = {"status": "juego", "tipo": "cambio label", "data": lista}
        self.servidor_signal.emit(mensaje)

    def cambiar_estado_label(self, lista):
        # lista es de la forma [tupla posicion inicio, tupla posicion final]
        for label in self.label_horizontal:
            if label.inicio == tuple(lista[0]) and \
                    label.final == tuple(lista[1]):
                label.actualizar_label()
        for label in self.label_vertical:
            if label.inicio == tuple(lista[0]) and \
                    label.final == tuple(lista[1]):
                label.actualizar_label()

    def label_cuadrado_completado(self, lista):
        if lista[0]:
            for elemento in lista[1]:
                label = self.indicadores_label[elemento]
                label.setText(f"{lista[3]}")
        if lista[2]:
            print(lista[2])
            txt = self.pos_1.text()
            txt = txt[2:]
            lista = txt.split("[")
            QMessageBox.warning(self,
                                "fin juego", f" se acabo el juego{lista[0]}")

    def update_pos(self, lista):
        for i in range(15):
            label = self.dict_pos[i + 1]
            label.setText(f"{i + 1})")
        for i in range(len(lista)):
            label = self.dict_pos[i+1]
            elemento = lista[i]
            label.setText(f"{i+1}) [{elemento['id']}]{elemento['nombre']}: "
                          f"{elemento['puntos']}")
        self.conectados.setText(f'conectados: {len(lista)}')

    def tam_m(self, num):
        self.m = num

    def tam_n(self, num):
        self.n = num


class SalaWindow(window_name3, base_class3):

    envio_sala_signal = pyqtSignal(str)

    def __init__(self, servidor_signal, terminar_conexion_signal, *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.servidor_signal = servidor_signal
        self.terminar_conexion_signal = terminar_conexion_signal
        # aquie estan los botones conectados
        self.Bnueva_sala.clicked.connect(self.crear_sala)
        self.Bselect_foto.clicked.connect(self.select_foto)
        self.Bfiltro.clicked.connect(self.bfiltro_clickeado)
        # esto es para crear los botones dinamicos de las salas los instancio
        # antes para no tener atributos dinamicos
        self.boton = None
        self.foto_perfil = ""
        self.foto_perfil_label.setPixmap(
            QPixmap("foto_incognito.png").scaled(80, 80))
        self.limpiar_grilla()
        self.filtro_actual = "normal"

    def crear_sala(self):
        # envia señal a un metodo de la ventana principal para crear la sala e
        # ingresar
        self.envio_sala_signal.emit("nueva_sala")

    def ingresar_sala_existente(self, elemento):
        # ingresa a una sala ya exixstente
        self.envio_sala_signal.emit(elemento)

    def actualizar_grilla_salas(self, lista):
        self.limpiar_grilla()
        self.crear_botones(lista)

    def boton_clickeado(self):
        boton = self.sender()
        texto = boton.text().split()
        self.ingresar_sala_existente(texto[1])

    def select_foto(self):
        self.foto_perfil = QFileDialog.getOpenFileName()
        self.foto_perfil = self.foto_perfil[0]
        with open(self.foto_perfil, "rb") as file:
            data = file.read()
        data1 = bytearray(data)
        qp = QPixmap()
        qp.loadFromData(data1, "PNG")
        lista_nombre = self.nombre_usuario_label.text().split()
        user_name = lista_nombre[1]
        self.foto_perfil_label.setPixmap(qp.scaled(80, 80))
        imagen_64 = base64.b64encode(data)
        imagen_str = imagen_64.decode("utf-8")
        msj = {"status": "nueva_foto_perfil", "nombre": user_name,
               "data": imagen_str}
        self.servidor_signal.emit(msj)

    def crear_botones(self, lista):
        for elemento in lista:
            nro = elemento[0]
            ingresados = elemento[1]
            self.boton = QPushButton(f'Sala {nro} | {ingresados}/15')
            # aqui hago que se bloque la sala si son mas de 3 ingresados/
            # cambiar a 15
            if ingresados >= 3:
                self.boton.setEnabled(False)
            self.vlay.addWidget(self.boton)
            self.boton.clicked.connect(self.boton_clickeado)
        self.vlay.setSpacing(0)

    def limpiar_grilla(self):
        # https://stackoverflow.com/questions/4528347/clear-all-
        # widgets-in-a-layout-in-pyqt
        for i in reversed(range(self.vlay.count())):
            widgetToRemove = self.vlay.itemAt(i).widget()
            # remove it from the layout list
            self.vlay.removeWidget(widgetToRemove)
            # remove it from the gui
            widgetToRemove.setParent(None)

    def bfiltro_clickeado(self):
        # uso self.filtro_actual para no enviar señales si es que el filtro que
        # se quiere aplicar ya esta en la foto
        tipo = ""
        if self.f_normal.isChecked() and self.filtro_actual == "dibujo":
            tipo = "normal"
            self.filtro_actual = "normal"
        elif self.f_dibujo.isChecked() and self.filtro_actual == "normal":
            tipo = "dibujo"
            self.filtro_actual = "dibujo"
        if tipo in ["normal", "dibujo"]:
            lista_nombre2 = self.nombre_usuario_label.text().split()
            user_name2 = lista_nombre2[1]
            msj8 = {"status": "aplicar_filtro",
                    "tipo": tipo, "nombre": user_name2}
            self.servidor_signal.emit(msj8)


class LabelLineaH(QLabel):

    horizontal_signal = pyqtSignal(list)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.activado = False
        self.inicio = None
        self.final = None
        self.setText(20*"- ")
        self.show()
        self.setGeometry(2, 2, 80, 10)

    def mousePressEvent(self, event):
        if not self.activado:
            # self.setStyleSheet("background-color: black;")
            self.activado = False
            # lsita de tuplas con las posiciones que unen
            lista = [self.inicio, self.final]
            self.horizontal_signal.emit(lista)

    def actualizar_label(self):
        self.activado = True
        self.setStyleSheet("background-color: black;")


class LabelLineaV(QLabel):

    vertical_signal = pyqtSignal(list)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.activado = False
        self.inicio = None
        self.final = None
        self.setText(20*"|\n")
        self.show()
        self.setGeometry(2, 2, 10, 80)

    def mousePressEvent(self, event):
        if not self.activado:
            # self.setStyleSheet("background-color: black;")
            self.activado = False
            # lsita de tuplas con las posiciones que unen
            lista = [self.inicio, self.final]
            self.vertical_signal.emit(lista)

    def actualizar_label(self):
        self.activado = True
        self.setStyleSheet("background-color: black;")


def algoritmo(m, n):
    tam = 20
    rect = 80
    largo_general = tam + rect
    largo_x = n*tam + (n-1)*rect
    largo_y = m*tam + (m-1)*rect

    pix = (551 - largo_x)/2
    piy = (581 - largo_y)/2

    pos_id = (tam + rect + tam)/2 - (tam/2)
    return pix, piy, tam, rect, largo_general, pos_id
