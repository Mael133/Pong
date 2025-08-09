import pygame
import numpy as np

LARGURA, ALTURA = 800, 600
COR_FUNDO = pygame.Color('grey12')
BRANCO = (255, 255, 255)
RAQUETE_LARGURA, RAQUETE_ALTURA = 20, 100
BOLA_RAIO = 7
VELOCIDADE_RAQUETE = 6
VELOCIDADE_INICIAL_BOLA = 7

class circulo:
    def __init__(self, x, y, raio):
        self.x = x
        self.y = y
        self.raio = raio

class retangulo:
    def __init__(self, x, y, largura, altura):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.rect = (x, y, largura, altura)

def colisao(circulo, ret):

    print(f"DEBUG: Tipo de circulo.x = {type(circulo.x)}, Valor = {circulo.x}")
    print(f"DEBUG: Tipo de ret.x = {type(ret.x)}, Valor = {ret.x}")

    centroRet = [0,0]
    distancia = [0,0]
    centroRet[0] = ret.x + ret.largura/2
    centroRet[1] = ret.y + ret.altura/2
    distancia[0] = abs(circulo.x - centroRet[0])
    distancia[1] = abs(circulo.y - centroRet[1])

    if distancia[0] > (ret.largura/2 + circulo.raio): return False
    if distancia[1] > (ret.altura/2 + circulo.raio): return False

    if (distancia[0] <= (ret.largura/2)): return True 
    if (distancia[1] <= (ret.altura/2)): return True

    distanciaCantoQ = (distancia[0] - ret.largura/2)**2 + (distancia[1] - ret.altura/2)**2

    return (distanciaCantoQ <= (circulo.raio**2))

