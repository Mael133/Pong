# Pong Online

## Descrição

Pong Online é uma implementação multiplayer do clássico jogo de arcade Pong. O projeto utiliza soquetes de rede para permitir que dois jogadores compitam um contra o outro em uma conexão P2P (Peer-to-Peer). Um jogador atua como o "host" da partida, enquanto o outro se conecta como "cliente".

O jogo é construído em Python com a biblioteca Pygame para a interface gráfica e manipulação de eventos, e a biblioteca NumPy para cálculos vetoriais da física da bola. Ele oferece a flexibilidade de escolher entre os protocolos de transporte TCP e UDP, além de suportar tanto IPv4 quanto IPv6 para a conexão de rede.

## Equipe

| Nome Completo | Matrícula |
| :--- | :--- |
| Israel Moura Higino | 20231054010010 |
| Ryan Vitor Maia Lemos | 20231054010011 |
| Eliezio Maldini da Silva Tavares | 20231054010008 |
| Thiago Cayron Alves Saraiva | 20231054010004 |
| Francisco Kennedy Nascimento Fonseca | 20231054010031 |

## Instalação de Dependências

Para executar este projeto, você precisará ter o Python 3 instalado. Além disso, são necessárias as bibliotecas `pygame` e `numpy`. Você pode instalá-las utilizando o gerenciador de pacotes `pip`:

```bash
pip install pygame numpy
```