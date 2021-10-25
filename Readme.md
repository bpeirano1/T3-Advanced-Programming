# Tarea 3: Timbirichi
Bartolomé Peirano, sección 3

## Consideraciones generales :octocat:
1. En primer lugar mi juego tiene contraseñas, para ello he creado 3 jugadores guardados bart, tom y jp, los cuales sus contraseñas son 1,2,3 respectivamente. Se pueden registrar usuarios, pero estos seran borrados si es que el server se vuelve a correr, por tanto alfinal cada vez que se corra este, se vuelve a las condiciones iniciales con las tres cuentas menciandas anteriormente. Para evitar que sean borrados los usuarios nuevos se debe eliminar las lineas de la 17 a la 19 del archivo "server/main.py". El único problema de esto último, es que mi juego no tiene implentado el cerrar_ventana o desconectar un socket por lo que el estado de un jugador despues de ingresar siempre va a a aparecer conectado, aunque este ya no lo este. Para solucionar esto, cada vez que se quiera correr el server. se deberá acceder antes al archivo "server/basededatos/usuario.json" y cambiar el primer elemento de cada lista de True a False. Así no habra problemas para conectarse cada vez que se corra el servidor.
En base a esto último, mi unica linea que pasa los 80 caracteres es la 18, la cual es la que se usa para sobreescribir el archivo "server/basededatos/usuario.json" cada vez que el server se corre y así siempre volver a las mismos usuarios iniciales, así que agradecería se es que no me descuentan por eso, ya que lo hice por un tema de logisica para ir probando la tarea. De hecho también puede ser util para ti, si es que quieres registrar más usuarios y no quieres que se te borren cada vez que corras el servidor, ni tampoco quieres estar cambiando el estado de conexion de cada jugador (en el caso de que borraras las lineas), para ello, debes correr una vez el servidor, luego correr un cliente, despues registrar a todos los usuarios que quieres, luego vayas a "server/basededatos/usuario.json" copies el diccionario y posteriormente lo pegues en la linea 18 de "server/main.py". Espero que no haya sido muy enredado lo anterior, pero eso era lo mas dificil de explicar, ahora podré ser mas conciso.

2. Como ya dije no implemente el close de la ventana y por tanto no se desconecta de la mejor manera el socket ( no lo hice porque no me alcanzo el tiempo, lo tenia presente :) ), ni el cambio de estado de conectado a desconectado de la base de datos para el ingreso. Tampoco implemente la cuenta regresiva de cada turno, que se avise al ganador de la partida, que se pueda jugar una segunda partida, que se bloquen las salas en las que ya partió una partida(por lo que jugadores pueden entrar a salas que ya partieron su juego).

3. También pueden haber problemas con salir de una sala y reingresar a otra cuando la partida ya empezo, porque el tablero que se les meustra es el de la partida anterior. (ojo que con esto hay un supuesto más adelante en las consideraciones generales de que no se puede salir durante una partida de la sala).

4. En el lado derecho de la interfaz de la ventana de juego se pueden ver los jugadores conectados de la forma Nombre[identifiacdor]: puntos.

5. Los turnos de cada partida estan dados por el orden de llegada a la sala, digo esto porque en la interfaz no te muestra explicitamente de quien es el turno, así que tienes que saber el orden para saber a quien le toca. Una manera facil de ver esto es fijarse en los identificadores de cada jugador ya que son letras del abcedario, por lo que el primero en jugar va a ser el quu tenga la "A", el segundo la "B", el tercero la "C" y así sucesivamente. (ojo que esto ultimo no nos permite ver el orden si es que alguien salio de la sala, ya que ahí se desordenan el orden de los identificadores).

6. Las personas que no tienen foto de perfil, se les pone por default la foto de un marciano como el de pac-man ("client/foto_incognito.png).

7. En "client/fotos_para_elegir" se pueden encontrar tres fotos en formato png que son las que uso para probar la foto de perfil y el filtro de dibujo. Estas son buenas para probar ya que no son muy pesadas por lo que mandarlas en bytes entre el servidor y el cliente no se demora y también se les puede aplicar el filtro sin problema.

8. Esta implementada la tecla Enter para enviar mensajes en el chat.

9. Los usuarios se guardan en "server/basededatos/usuarios.json y la foto de perfil normal y la del filtro de dibujo se guardan en el directorio "server/basededatos/fotos_perfil/{nombre de usuario}".

10. El archivo pixel_collector.py tiene que estar dentro de la carpeta del servidor.

11. Para que una foto se guarde en el usuario y esta se vea cada vez que ingresa, hay que seguir los pasos dichos en el punto 1 (linea 9-16 en el readme), sobre reescribir el diccionario de la linea 18, estoy hay que hacerlo cuando una persona ingresa su primera foto al sistema, ya que así se cambia la direccion que estaba vacía ("") por la direccion en que se guardo la foto en el servidor ("basededatos/foto_perfil/{nombre_jugador}/foto_normal.png"), este es el tercer elemento de la lista que esta asociado como valor de cada llave en el archivo "basededatos/usuarios.json" (que es un dict). Cabe destacar que una vez hecho lo anterior ya no es necesario hacer los pasos denuevo cada vez que un cliente seleccione una nueva foto, ya que despues cada vez que una foto se seleccione se sobreescribira el archivo png de la foto, por lo que no cambiaria el nombre de ese archivo y con ello tampoco cambiaria la direccion guradada en el diccionario del archivo "basededatos/usuarios.json".

12. Por ultimo, hay que hacer click en la linea punteada o sus alrededores cercanos para poder activar el qlabel de la linea.

### Cosas implementadas y no implementadas :white_check_mark: :x:

* Parte 2 Timbirichi99:
    * Parte 2.1 Formar un Cuadrado: Hecha completa, ojo que para cambiar el tamaño del tablero hay que cambiar los paramtros "n" y "m" del archivo "server/parametros.json". Mi juego esta seteado para partir en un tablero de 4x4, recomiendo llegar hasta 6x6 porque sino depsues se pueden sobreponer los elementos.
* Parte 4 Networking:
    * Parte 4.1 La conexión: Hecha completa
    * Parte 4.2 Arquitectura cliente-servidor: Hecha completa
    * Parte 4.2.1 Separación Funcional: Hecha completa
    * Parte 4.2.2 Roles: Hecha completa
* Parte 5 Interfaz Grafica:
    * Parte 5.1 Conexión con servidor: Hecha completa
    * Parte 5.2 Autentificación del Usuario: Hecha completa
    * Parte 5.3 Salas: Hecha completa, pero ojo en la parte de que se ingrsan maximo 15 personas por sala, mi programa solo permiete 3 por temas de logstica para revisar, para cambiarlo a 15 es cosa de ir al archivo "client/t3_Frontend2" y en la linea 301 cambiar el numeor 3 por un 15.
    * Parte 5.3.1 Creación de sala: Hecha Completa
    * Parte 5.3.2 Preparación de la partida: Hecha Casi completa, lo unico que podria fallar es reingresar a una sala despues de haber salido de una sala con la partida ya comenzada, ya que cuando ingrese a la nueva sala, su tablero va a estar activado según la sala anterior. Pero el caso de que el lider abandona la sala se maneja bien la situación ( a menos de que haya sido el caso explicado anterior) y también los botones de salas desaparcen cuando una sala no tiene integrantes.
    * Parte 5.3.3 Partida: Hecha casi completa, cumple con los requerimientos de nombre de usuario, puntajes, tablero, ciclo (el orden de los turnos esta dado por el numero en que ingreso, es decir el primero en ingresar tiene el primer turno, el segundo ....)( También si un jugador hace un cuadrado, este repite y juega una vez mas), identificadores, N y M en parametros.json (revisar el punto 2.1 para saber que valores darle a n y m). Pero NO cumple con la cuenta regresiva de cada turno y tampoco te avisa quien gana, ni te da la posibilidad de jugar otra partida.
            
    * Parte 5.4 Chat: Hecho completamente, lo unico que podría fallar es reingresar a una sala despues de haber sido expulsado de una sala con la partida ya comenzada, ya que cuando ingrese a la nueva sala, su tablero va a estar activado según la sala anterior.
    
* Parte 6 Filtro Dibujo: Hecha completa,  esto se puede ver en "server/filtro" en la funcion "filtro", la cual se encarga de realizar las respectivas operaciones matriciales sobre una foto y guardar la nueva foto con filto como un dibujo, en el directorio dado.

* Parte 7 Manejo de bytes: Hecha completa, las fotos con y sin filtro se guardan en el directorio "base de datos" del servidor según el nombre del usuario. También se puede apreciar el envio de los bytes de las imagenes como string entre el servidor y cliente, especificamente se pueden observar en el método "manejar_comando" ( del servidor y cliente), en donde el "status" del diccionario es "respuesta_filtro" o "nueva_foto_perfil" o "aplicar_filtro".

* Parte 8 .gitignore: Hecha completa. Cabe destacar que el archivo "pixel_collector.py" ( que fue ignorado) tiene que estar en la carpeta del server, para poder correr mi tarea.

* Parte 9 Avance Tarea: Se entrego completa y dentro de los plazos el avance.

* Parte 10 Bonus: Los bonus completos implementados fueron el de emojis y el de claves. 
     * Parte 10.1 Chat con Emojis: Para el de emojis esta el archivo "client/emojis.py" en donde se guarda el diccionario que tiene como llave el nombre del emoji (:nombre_emoji:) y el valor asociado a esa seria su Unicode. En este caso, implemente 5 emojis y que por temas de logistica ( para escribir mas rapido) su forma de escribirlo es :e1:, :e2:, ..., :e5: (no el nombre del emoji). Cabe destacar que para cambiar los emojis y sus nombre de acceso, basta con modificarlas llaves y valores del diccionario mencionado anteriormente.
     * Parte 10.4 Contraseñas: Para el bonus de las claves, estas son guardadas en el archivo "server/basededatos/usuarios.json" y verificadas por medio de encriptacion, utilizando bcrypt y sus respectivos métodos. Si se quiere revisar la clave encriptada, esta es el primer elemento de la lista de los valores asociados al diccionario del archivo mencionado anteriormente. La encriptacion y verifiación ocurren en las funciones de registro_usuario() y comprobar_usuario() del archivo "server/funciones.py".


## Ejecución :computer:
El módulo principal de la tarea a ejecutar, es primero el servidor el cual es "server/main.py" y posteriormente cada cliente se puede ejecutar con "client/main.py"


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```socket```-> ``` socket()```, ```socket.AF_INET```, ```socket.SOCK_STREAM```, ```connect()```, ``` reciv()```, ``` bind()```, ``` send()```, ``` listen()```, ``` accept()```
2. ```json```-> ```dump()```, ```dumps()```, ```load()```, ```loads()``` 
3. ```threading```-> ```Thread()``` , ```Lock()``` 
4. ```os```-> ```makedirs()```, ```path.join()``` ,
5. ```base64```-> ```b64decode()```, ```b64encode()```
6. ```time```-> ```sleep()``` 
7. ```sys```-> ```__excepthook__```, ```exit()``` 
8. ```PyQt5```-> ```QApplication() / QtWidgets```, ```QScrollArea() / QtWidgets```,```QPushButton() / QtWidgets```,```QMessagebox() / QtWidgets```,```QVBoxLayout() / QtWidgets```,```QLineEdit() / QtWidgets```, ```QLabel() / QtWidgets```, ```QWidget() / QtWidgets```, ```QFileDialog() / QtWidgets```, ```pyqtSignal() / QtCore```, ``` Qt/ QtCore```, ```uic```, ``` QPixmap()/ QtGui``` (debe instalarse)
9. ```datetime```-> ```now()``` 
10. ```bycrypt```-> ```bcrypt.hashpw()```, ```bcrypt.gensalt()```, ```bcrypt.checkpw``` (debe instalarse)
11. ```Pillow```-> ```Lo usa la función Pix_collector() que nos dan``` (debe instalarse)
12.  ```numpy```-> ```array()```, ```square()```, ```sqrt()```, ```add()```, ```subtract()```, ```einsum()```, ```lib.stride_tricks.as_strided``` (debe instalarse)
13.  ```zlib```-> ```crc32()```, ```compress()``` 

...

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```server/creador_parametros.py```-> Es un módulo que se encarga de crear el archivo "server/parametros.json", según el diccionario dado.
2. ```server/filtro.py```-> Contiene a la funcion "filtro(path_foto, path_donde_guardar_foto)" la cual se encarga de transformar una foto normal a un foto de dibujo y esta a su vez la guarda en el path que se le es dado.
3. ```server/funciones.py```-> Este módulo contiene funciones como "registar_usuario", "verificar_usuario", "guardar_foto", "enviar_foto_filtro", las cuales nos facilitan el acceder y guardar datos en la base de datos del programa.
4. ```server/Tablero.py```-> Contiene la clase "Tablero" la cual es instanciada en el main del servidor para poder controlar y verificar las movidas de los jugadores durante la partida.
5. ```client/t3_Frontend```-> Contiene la clase "MainWindow" la cual es la primera ventana del juego que se abre y que también se encarga de manipular las otras ventas abiertas (GameWinodw y SalaWindow).
6. ```client/t3_Frontend2```-> Contiene la clase GameWindow y SalaWindow.
7. ```client/creador_parametros.py```-> Es un módulo que se encarga de crear el archivo "client/parametros.json", según el diccionario dado.
8. ```client/emojis.py```-> Contiene al diccionario que tiene como valores los Unicodes de los emojis para el chat del juego.

...

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:
 
1. Se asume que cuando prueben mi tarea no se va a presionar le boton de salir en medio de una partida ya empezada, ya que en una issue lei que se podia salir antes o despues de una partida pero no durante. Igual cabe destacar que el unico problema que se tendría al salir en esta situacion, es que despues cuando se vuelva a meter a otra sala, su tablero va a seguir activado.
2. Se asume que solo se van a seleccionar fotos en formato de png para la foto de perfil, se dijo en una de las issues.
3. Cuando un usuario aplica el filtro de dibujo a su foto de perfil, esta se cambia por el juego, pero posteriormente cuando el jugador  se conecte denuevo para jugar, su foto de perfil va ha ser la normal (igual la foto de dibujo es guardada en la base de datos y se puede ver ahí), esto es válido ya que en el enunciado no se especifica como se debe hacer esta parte, y también le pregunte a un ayudante y me dijo que mientras guarde la foto de dibujo en alguna parte esta bien. 

...

-------

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. ( https://stackoverflow.com/questions/43086557/convolve2d-just-by-using-numpy): De aquí saque la funcion "conv2d()" la cual se encarga de hacer la convolucion de matrices 2d, utilizando funciones de la libreria "numpy". Está implementado en el archivo server/filtro.py en las líneas 166-170. Esta funcion la uso para la operaciones de matrices necesarias para hacer la parte del filtro de dibujo.
2. (https://www.programcreek.com/2013/09/convert-image-to-string-in-python/): De aquí saque la libreria base64 la cual me permite transformar los bytes de una foto a un string para así poder mandar las fotos entre el servidor y el cliente. Ej en server/funciones.py en la lineas 48-52.
3. (https://unicode.org/emoji/charts-12.0/full-emoji-list.html): De esta pagina saque los Unicodes de los emojies que uso. Estos se pueden ver en el archivo "client/emojis.py".
3. (https://stackoverflow.com/questions/4528347/clear-all-widgets-in-a-layout-in-pyqt): Esto limpia o saca todos los QWidgets que hay en un layout. Está implementado en el archivo "client/t3_Frontend2.py" en las líneas 307-315 y saca todo los botones de la sala de espera, antes de crear los nuevos botones con las actualiaciones de las salas.


