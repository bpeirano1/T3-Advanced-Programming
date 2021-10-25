import sys
import threading as th
import socket
import json
from t3_Frontend import MainWindow
from PyQt5.QtWidgets import QApplication, QFileDialog
from datetime import datetime

with open("parametros.json", "r") as file:
    data = json.load(file)

Host = data["Host"]
Port = data["Port"]


class Cliente:

    def __init__(self):
        print("Inicializando cliente...")
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.host = Host
        self.port = Port

        self.lock = th.Lock()
        self.lock2 = th.Lock()

        self.frontend = MainWindow()
        self.frontend.show()
        # conecto señals paera evitar modelacion circular
        self.frontend.servidor_signal.connect(self.send)
        self.frontend.terminar_conexion_signal.connect(self.terminar_conexion)

        try:
            self.socket_cliente.connect((self.host, self.port))
            print("Cliente conectado exitosamente al servidor")

            self.conectado = True

            escuchar_servidor = th.Thread(target=self.escuchar, daemon=True)
            escuchar_servidor.start()
            print("Escuchando al servidor...")

        except ConnectionRefusedError:
            self.terminar_conexion()

    def escuchar(self):
        '''
        Este método es usado en el thread y la idea es que reciba lo que
        envía el servidor. Implementa el protocolo de agregar los primeros
        4 bytes, que indican el largo del mensaje
        '''

        while self.conectado:
            try:
                # Recibimos los 4 bytes del largo
                tamano_mensaje_bytes = self.socket_cliente.recv(4)
                tamano_mensaje = int.from_bytes(tamano_mensaje_bytes,
                                                byteorder="big")

                contenido_mensaje_bytes = bytearray()

                # Recibimos el resto de los datos
                while len(contenido_mensaje_bytes) < tamano_mensaje:
                    contenido_mensaje_bytes += self.socket_cliente.recv(
                        min(256, tamano_mensaje))

                print("pase el while")
                # Decodificamos y pasamos a JSON el mensaje
                contenido_mensaje = contenido_mensaje_bytes.decode("utf-8")
                mensaje_decodificado = json.loads(contenido_mensaje)

                # Manejamos el mensaje
                with self.lock:
                    self.manejar_comando(mensaje_decodificado)

            except ConnectionResetError:
                self.terminar_conexion()

    def manejar_comando(self, diccionario):
        '''
        Este método toma el mensaje decodificado de la forma:
        {"status": tipo del mensaje, "data": información}
        '''

        print(f"Mensaje recibido: {diccionario}")

        if diccionario["status"] == "mensaje":
            data = diccionario["data"]
            usuario = data["usuario"]
            contenido = data["contenido"]
            usuario = f"({datetime.now().hour}:{datetime.now().minute}) " \
                f"{usuario}"
            self.frontend.ventana_juego.chat_update_signal.emit(
                f"{usuario}: {contenido}")
            if diccionario["cerrar"]:
                self.frontend.chao_signal.emit()

                # self.frontend.ventana_sala.show()

        elif diccionario["status"] == "salas_actualizadas":
            data = diccionario["data"]
            self.frontend.sala_update_signal.emit(data)

        elif diccionario["status"] == "respuesta_registro":
            booleano = diccionario['registro']
            "mando la señal"
            self.frontend.registro_signal.emit(booleano)

        elif diccionario["status"] == "respuesta_ingreso":
            # en el caso de que haya foto de perfil la lista tiene un elemeto
            # extra con la foto
            lista = diccionario["comprobacion"]
            print(lista)
            self.frontend.ingreso_signal.emit(lista)

        elif diccionario["status"] == "salir":
            self.frontend.chao_signal.emit()
        elif diccionario["status"] == "sala_lider":
            self.frontend.sala_lider_signal.emit(diccionario["data"])

        elif diccionario["status"] == "juego":
            if diccionario["tipo"] == "empezar":
                self.frontend.ventana_juego.empezar_juego_signal.emit()

            elif diccionario["tipo"] == "cambio label":
                data2 = diccionario["data"]
                data3 = diccionario["cuadrados_marcados"]
                self.frontend.ventana_juego.actualizar_label_signal.emit(data2)
                self.frontend.ventana_juego.cuadrado_completo_signal.emit(data3)

        elif diccionario["status"] == "respuesta_filtro":
            self.frontend.filtro_update_signal.emit(diccionario["data"])

        elif diccionario["status"] == "actualizar_posiciones":
            # ahora aqui abajo voy a mandar la señal para mostrar a los
            # jugadores de la partida, pos= posiciones
            lista_pos = diccionario["pos"]
            self.frontend.ventana_juego.pos_update_signal.emit(lista_pos)
        elif diccionario["status"] == "tam_tablero":
            self.frontend.ventana_juego.tam_m_signal.emit(diccionario["m"])
            self.frontend.ventana_juego.tam_n_signal.emit(diccionario["n"])

    def send(self, mensaje):
        '''
        Este método envía la información al servidor. Recibe un mensaje del tipo
        {"status": tipo del mensaje, "data": información}
        '''

        # Codificamos y pasamos a bytes
        mensaje_codificado = json.dumps(mensaje)
        contenido_mensaje_bytes = mensaje_codificado.encode("utf-8")

        # Tomamos el largo del mensaje y creamos 4 bytes de esto
        tamano_mensaje_bytes = len(contenido_mensaje_bytes
                                   ).to_bytes(4, byteorder="big")

        # Enviamos al servidor
        self.socket_cliente.send(tamano_mensaje_bytes + contenido_mensaje_bytes)

    def terminar_conexion(self):
        print("Conexión terminada")
        self.connected = False
        self.socket_cliente.close()
        exit()


if __name__ == "__main__":
    def hook(type, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook
    app = QApplication([])
    cliente = Cliente()
    sys.exit(app.exec_())
