"""
Esta es el modulo que incluye la clase
del reproductor de musica
"""


class Player:
    """"
    Esta clase crea un reproductor
    de musica
    """

    def play(self, song):
        """
        Reproduce la cancion que recibio
        como parametro

        Parameters:
        song(str): este es un string con el path de
        la cancion

        Returns:
        int: devuelve 1 si reproduce con exito, en caso de
        fracaso devuelve 0 
        """
        print(f"Reproduciendo cancion: {song}")

    def stop(self):
        print("Deteniendo musica")
