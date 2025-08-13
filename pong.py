import pygame
import numpy as np

# Constantes que vão ser usadas, os nomes são bem sugestivos
LARGURA, ALTURA = 800, 600
COR_FUNDO = pygame.Color('grey12')
COR_OBJETOS = pygame.Color('white')
BRANCO = (255, 255, 255)
RAQUETE_LARGURA, RAQUETE_ALTURA = 20, 100
ESPACAMENTOPAREDE = 20
BOLA_RAIO = 7
VELOCIDADE_RAQUETE = 6
VELOCIDADE_INICIAL_BOLA = np.array([7,7])
velocidadeBola = np.array([7,7])

class circulo: 
    # define a estrutura com todos os dados
    # de um círculo
    def __init__(self, x, y, raio):
        self.x = x
        self.y = y
        self.raio = raio

class retangulo:
    # define a estrutura com todos os dados
    # de um retângulo
    def __init__(self, x, y, largura, altura):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura

def colisao(circulox, circuloy, ret, raio=BOLA_RAIO):
    # retornaverdadeiro se há uma intersecção entre o círculo
    # e o retângulo passados, e falso sen não houver

    # Diz Ryan que é matemática básica

    centroRet = [0,0]
    distancia = [0,0]
    centroRet[0] = ret.x + ret.largura/2
    centroRet[1] = ret.y + ret.altura/2
    distancia[0] = abs(circulox - centroRet[0])
    distancia[1] = abs(circuloy - centroRet[1])

    if distancia[0] > (ret.largura/2 + raio): return False
    if distancia[1] > (ret.altura/2 + raio): return False

    if (distancia[0] <= (ret.largura/2)): return True 
    if (distancia[1] <= (ret.altura/2)): return True

    distanciaCantoQ = (distancia[0] - ret.largura/2)**2 + (distancia[1] - ret.altura/2)**2

    return (distanciaCantoQ <= (raio**2))

