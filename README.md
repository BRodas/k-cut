k-cut
=====

El siguiente texto está dividido de la siguiente manera:
* Creación cuenta GitHub, para conseguir el material.
* Como usar GitHub de manera básica.
* Como usar los archivos contenidos en el repositorio.

Se da por hecho que se tiene instalado 'python'.

Creación cuenta GitHub
-------------------------------
(Pasos basados en la página 'https://help.github.com/articles/fork-a-repo')

1) Primero ir a 'https://github.com/' y crearse una cuenta.
2) Una vez creada la cuenta en el buscador de GitHub, buscar 'k-cut', y seleccionar el repositorio 'BRodas/k-cut'.
3) Seleccionado este realizar un "fork", esto presionando el boton "fork" en la zona superior derecha.

Hasta ahora se tiene creado un repositorio personal en GitHub, ahora hay que sincronizarlo con un directorio local en el computador de uno.

1) Abrir el terminal (Linea de comando).
2) Ir al directorio donde se quiere tener la carpeta con el repositorio, en este ejemplo se ocupa el escritorio, pero puede ser cualquier otro lugar:
```{bash}
cd ~/Desktop/
```
3) Clonar el repositorio de la página de GitHub:
```{bash}
git clone https://github.com/username/k-cut.git
```
Recordar reemplazar 'username' por el nombre de usuario con que se creó la cuenta en GitHub.

Como usar GitHub
-------------------------------

http://www.genbetadev.com/sistemas-de-control-de-versiones/aprende-a-usar-git-en-15-minutos


Como correr las aplicaciones
-------------------------------

Para ocupar la implementación en C ir al directorio 'pseudo_max/' y ejecutar:
```{bash}
bin/pseudo_fifo < data/sample.txt
```

Mientras que para ejecutar el heurística ir al directorio 'lib_python' y ejecutar:
```{bash}
python heuristica.py
```
