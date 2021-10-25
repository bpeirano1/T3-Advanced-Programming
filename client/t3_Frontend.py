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
from t3_Frontend2 import GameWindow, SalaWindow, LabelLineaV, LabelLineaH

window_name, base_class = uic.loadUiType("mainwindow.ui")


class MainWindow(window_name, base_class):

    servidor_signal = pyqtSignal(dict)
    terminar_conexion_signal = pyqtSignal()
    chat_update_signal = pyqtSignal(str)
    enter_pressed = pyqtSignal()
    sala_update_signal = pyqtSignal(list)
    chao_signal = pyqtSignal()
    registro_signal = pyqtSignal(bool)
    ingreso_signal = pyqtSignal(list)
    sala_lider_signal = pyqtSignal(list)
    filtro_update_signal = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.nombre_usuario = ""
        # Ventana Sala
        self.ventana_sala = SalaWindow(self.servidor_signal,
                                       self.terminar_conexion_signal)
        self.ventana_sala.envio_sala_signal.connect(self.envio_sala)
        # Ventana Chat
        self.ventana_juego = GameWindow(self.servidor_signal,
                                        self.terminar_conexion_signal,
                                        self.chat_update_signal)
        # conectando botones
        self.Bregistrar.clicked.connect(self.manejo_boton_registar)
        self.Bingresar.clicked.connect(self.manejo_boton_ingresar)
        self.enter_pressed.connect(self.manejo_boton_ingresar)

        # señal conectada para actaulizar las salas
        self.sala_update_signal.connect(
            self.ventana_sala.actualizar_grilla_salas)
        # señal conectada para el chao y hacer el juego de ventanas
        self.chao_signal.connect(self.ventana_juego.hide)
        self.chao_signal.connect(self.ventana_sala.show)
        self.chao_signal.connect(self.ventana_juego.borrar_chat)
        # conecto señal para recibir la respuesta del registro y del ingreso
        self.registro_signal.connect(self.qbox_registro)
        self.ingreso_signal.connect(self.qbox_ingreso)
        self.sala_lider_signal.connect(self.ventana_juego.actualizar_sala_lider)
        # conecto señal para actualizar foto de la ventana de la sala y juego
        self.filtro_update_signal.connect(self.update_foto_con_filtro)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.enter_pressed.emit()

    def manejo_boton_registar(self):
        if not len(self.lineEditReg_us.text()):
            QMessageBox.warning(self, "",
                                "Ingrese nombre de usuario para registro")
        elif not len(self.lineEditReg_con.text()):
            QMessageBox.warning(self, "",
                                "Ingrese contraseña para registro")
        else:
            nuevo_usuario = self.lineEditReg_us.text()
            nueva_contra = self.lineEditReg_con.text()
            msj = {"status": "registrar_usuario", "usuario": nuevo_usuario,
                   "contrasena": nueva_contra}
            self.servidor_signal.emit(msj)
            self.lineEditReg_us.setText("")
            self.lineEditReg_con.setText("")

    def manejo_boton_ingresar(self):
        if not len(self.lineEditUsuario.text()):
            QMessageBox.warning(self, "",
                                "Ingrese nombre de usuario")
        elif not len(self.lineEditContrasena.text()):
            QMessageBox.warning(self, "", "Ingrese contraseña")
        else:
            usuario_ingresado = self.lineEditUsuario.text()
            contrasena_ingresado = self.lineEditContrasena.text()
            msj = {"status": "verificar_usuario", "usuario": usuario_ingresado,
                   "contrasena": contrasena_ingresado}
            self.servidor_signal.emit(msj)

    def envio_sala(self, estado):
        self.ventana_sala.hide()
        mensaje = {"status": "nuevo_usuario", "data": self.nombre_usuario,
                   "sala": estado}
        self.servidor_signal.emit(mensaje)
        self.hide()
        self.ventana_juego.show()

    def qbox_registro(self, booleano):
        msgb = QMessageBox()
        if booleano:
            msgb = QMessageBox(self)
            msgb.setText("El usuario se registro correctamente")
            msgb.exec()
        else:
            msgb.warning(self, "", "El usario ya existe, no se puedo registrar")

    def qbox_ingreso(self, lista):
        msgb = QMessageBox()
        if lista == [False, False]:
            msgb.warning(self, "", "Nombre o Contraseña Incorrectas")
        elif lista == [True, False]:
            msgb.warning(self, "", "Usurio ya conectado... "
                                   "Posible hacker tratando de meterse")

        # En el caso de que el usario sea correcto me retorna a diferncia de los
        # otros casos una lista de 3 elementos [True, True, str de bytes de la
        # imagen de perfil si es que tiene]
        elif lista[0] and lista[1]:
            nombre = self.lineEditUsuario.text()
            self.nombre_usuario = nombre
            self.ventana_juego.nombre_usuario = nombre
            self.ventana_juego.nombre_usuario_label.setText(f"Usuario: {nombre}"
                                                            f"")
            self.ventana_sala.nombre_usuario_label.setText(f"Usuario: {nombre}")
            self.hide()
            self.ventana_sala.show()
            # Aqui pongo la foto de perfil que se guardo la ultima vez,
            # si es hay
            if lista[2]:
                imagen_64 = lista[2].encode("utf-8")
                bytes_foto = base64.b64decode(imagen_64)
                # creo el Qpixmap con bytes
                pixmap = QPixmap()
                pixmap.loadFromData(bytes_foto)
                self.ventana_sala.foto_perfil_label.setPixmap(pixmap.scaled(80,
                                                                            80))
                self.ventana_juego.foto_perfil.setPixmap(pixmap.scaled(80, 80))

        else:
            self.label_error.setText("Error de ingreso")
        self.lineEditUsuario.setText("")
        self.lineEditContrasena.setText("")

    def update_foto_con_filtro(self, string_foto):
        str_foto = string_foto
        bytes_foto_64 = str_foto.encode("utf-8")
        bytes_original = base64.b64decode(bytes_foto_64)
        pixmap2 = QPixmap()
        pixmap2.loadFromData(bytes_original)
        self.ventana_sala.foto_perfil_label.setPixmap(pixmap2.scaled(80, 80))
        self.ventana_juego.foto_perfil.setPixmap(pixmap2.scaled(80, 80))
