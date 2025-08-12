import pygame

#Classe de botões, para criar botões na interface
class Botao:
    #Inicializa o botão e seus parâmetros
    def __init__(self, x, y, largura, altura, texto, fonte, texto_cor, fundo_cor, hover_cor):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.fonte = fonte
        self.hover_cor = hover_cor
        self.texto_cor = texto_cor
        self.fundo_cor = fundo_cor

    #Desenha o botão na tela
    def draw_button(self, superficie):
        mouse_pos = pygame.mouse.get_pos()
        cor = self.hover_cor if self.rect.collidepoint(mouse_pos) else self.fundo_cor
        pygame.draw.rect(superficie, cor, self.rect)

        texto_renderizado = self.fonte.render(self.texto, True, self.texto_cor)
        texto_rect = texto_renderizado.get_rect(center=self.rect.center)
        superficie.blit(texto_renderizado, texto_rect)

    #Registra se o botão foi clicado
    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )

class caixaDeTexto:
    def __init__(self, x, y, a, l, fonte, cor, texto=''):
        self.rect = pygame.Rect(x, y, a, l)
        self.cor = cor
        self.texto = texto
        self.fonte = fonte
        self.txt_surface = fonte.render(texto, True, self.cor)
        self.ativa = False

    def draw(self, tela):
        tela.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(tela, self.cor, self.rect, 2)


#Função para executar o menu
def menu_principal(tela, largura):
    fonte = pygame.font.Font(None, 40)
    fonte_titulo = pygame.font.Font(None, 80)

    titulo = "PONG ONLINE"
    titulo_cor = (255, 255, 255)
    titulo_superficie = fonte_titulo.render(titulo, True, titulo_cor)

    titulo_rect = titulo_superficie.get_rect()
    titulo_rect.center = (largura//2, 150)

    # Criar botões
    botao_host = Botao(300, 250, 200, 50, "CRIAR SALA", fonte, (255, 255, 255), (0, 0, 0), (148, 236, 162))
    botao_conect = Botao(300, 350, 200, 50, "CONECTAR", fonte, (255, 255, 255), (0, 0, 0), (148, 193, 236))
    botao_sair = Botao(300, 450, 200, 50, "SAIR", fonte, (255, 255, 255), (0, 0, 0), (236, 148, 148))

    
    while True:
        tela.fill((30, 30, 30))  # Fundo
        tela.blit(titulo_superficie, titulo_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if botao_host.is_clicked(event):
                return "host"

            if botao_conect.is_clicked(event):
                return "cliente"

            if botao_sair.is_clicked(event):
                pygame.quit()
                exit()

        #Desenha os botões
        botao_conect.draw_button(tela)
        botao_sair.draw_button(tela)
        botao_host.draw_button(tela)

        pygame.display.flip()

#Menu de conexão
def menu_protocolo(tela, largura, altura):
    fonte = pygame.font.Font(None, 40)
    fonte_titulo = pygame.font.Font(None, 76)

    titulo = "QUAL O TIPO DE CONEXÃO?"
    titulo_superficie = fonte_titulo.render(titulo, True, (255, 255, 255))

    titulo_rect = titulo_superficie.get_rect()
    titulo_rect.center = (largura//2, altura//4)

    # Criar botões
    botao_TCP = Botao(150, 250, 200, 50, "TCP", fonte, (255, 255, 255), (0, 0, 0), (148, 193, 236))
    botao_UDP = Botao(450, 250, 200, 50, "UDP", fonte, (255, 255, 255), (0, 0, 0), (148, 193, 236))

    
    while True:
        tela.fill((30, 30, 30))  # Fundo
        tela.blit(titulo_superficie, titulo_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if botao_TCP.is_clicked(event):
                return "tcp"

            if botao_UDP.is_clicked(event):
                return "udp"

        #Desenha os botões
        botao_TCP.draw_button(tela)
        botao_UDP.draw_button(tela)

        pygame.display.flip()

def menu_tipo_ip(tela, largura, altura):
    fonte = pygame.font.Font(None, 40)
    fonte_titulo = pygame.font.Font(None, 80)

    titulo = "QUAL O TIPO DE IP USADO?"
    titulo_superficie = fonte_titulo.render(titulo, True, (255, 255, 255))

    titulo_rect = titulo_superficie.get_rect()
    titulo_rect.center = (largura//2, altura//4)

    # Criar botões
    botao_ipv4 = Botao(150, 250, 200, 50, "IPV4", fonte, (255, 255, 255), (0, 0, 0), (148, 193, 236))
    botao_ipv6 = Botao(450, 250, 200, 50, "IPV6", fonte, (255, 255, 255), (0, 0, 0), (148, 193, 236))

    
    while True:
        tela.fill((30, 30, 30))  # Fundo
        tela.blit(titulo_superficie, titulo_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if botao_ipv4.is_clicked(event):
                return "ipv4"

            if botao_ipv6.is_clicked(event):
                return "ipv6"

        #Desenha os botões
        botao_ipv4.draw_button(tela)
        botao_ipv6.draw_button(tela)

        pygame.display.flip()

def menu_porta(tela, largura, altura):
    fonte = pygame.font.Font(None, 40)
    fonte_titulo = pygame.font.Font(None, 80)

    titulo = "QUAL A PORTA DA SALA?"
    titulo_superficie = fonte_titulo.render(titulo, True, (255, 255, 255))

    titulo_rect = titulo_superficie.get_rect()
    titulo_rect.center = (largura//2, altura//4)

    # Criar botões
    botao_confirmar = Botao(300, 350, 200, 50, "CONFIRMAR", fonte, (255, 255, 255), (0, 0, 0), (148, 193, 236))
    caixa_texto = caixaDeTexto(150, 250, 500, 50, fonte, (255, 255, 255))

    while True:
        tela.fill((30, 30, 30))  # Fundo
        tela.blit(titulo_superficie, titulo_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return caixa_texto.texto
                if event.key == pygame.K_BACKSPACE:
                    caixa_texto.texto = caixa_texto.texto[:-1]
                else:
                    caixa_texto.texto += event.unicode
                # redesenha o texto
                caixa_texto.txt_surface = caixa_texto.fonte.render(caixa_texto.texto, True, caixa_texto.cor)


            if botao_confirmar.is_clicked(event):
                return caixa_texto.texto
            
        #Desenha os botões
        botao_confirmar.draw_button(tela)
        caixa_texto.draw(tela)

        pygame.display.flip()

def menu_ip(tela, largura, altura):
    fonte = pygame.font.Font(None, 40)
    fonte_titulo = pygame.font.Font(None, 80)

    titulo = "QUAL O IP DA SALA?"
    titulo_superficie = fonte_titulo.render(titulo, True, (255, 255, 255))

    titulo_rect = titulo_superficie.get_rect()
    titulo_rect.center = (largura//2, altura//4)

    # Criar botões
    botao_confirmar = Botao(300, 350, 200, 50, "CONFIRMAR", fonte, (255, 255, 255), (0, 0, 0), (148, 193, 236))
    caixa_texto = caixaDeTexto(150, 250, 500, 50, fonte, (255, 255, 255))

    while True:
        tela.fill((30, 30, 30))  # Fundo
        tela.blit(titulo_superficie, titulo_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return caixa_texto.texto
                if event.key == pygame.K_BACKSPACE:
                    caixa_texto.texto = caixa_texto.texto[:-1]
                else:
                    caixa_texto.texto += event.unicode
                # redesenha o texto
                caixa_texto.txt_surface = caixa_texto.fonte.render(caixa_texto.texto, True, caixa_texto.cor)


            if botao_confirmar.is_clicked(event):
                return caixa_texto.texto
            
        #Desenha os botões
        botao_confirmar.draw_button(tela)
        caixa_texto.draw(tela)

        pygame.display.flip()
