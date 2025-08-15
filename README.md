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

## Como Executar a Aplicação

A aplicação deve ser executada por dois jogadores em máquinas diferentes (ou na mesma máquina usando o endereço de loopback para o endereço de IP). Um jogador será o Host (que cria a sala) e o outro será o Cliente (que se conecta à sala). Para testar na mesma máquina, basta executar duas instâncias da aplicação.

### Para o Jogador Que Será o Host:

1. Execute o arquivo `main.py` a partir da linha de comando:
```bash
python main.py
```
2. No primeiro menu, selecione **"CRIAR SALA"**.
3. Escolha o protocolo de rede desejado: **TCP** ou **UDP**.
4. Escolha o tipo de IP: **IPV4** ou **IPV6**.
5. Digite o número da porta que será usada para a conexão (ex: `12345`) e clique em **"CONFIRMAR"**.
6. Uma tela de **"Aguardando conexão..."** será exibida. Após o cliente se conectar, o botão **"COMEÇAR"** ficará disponível. Clique nele para iniciar a partida.

### Para o Jogador Que Será o Cliente:

1. Execute o arquivo `main.py` a partir da linha de comando:
```bash
python main.py
```
2. Escolha o mesmo protocolo de rede que o host selecionou (**TCP** ou **UDP**).
3. Escolha o mesmo tipo de IP que o host está utilizando (**IPV4** ou **IPV6**).
4. Digite a mesma porta que o host definiu e clique em **"CONFIRMAR"**.
5. Digite o endereço de IP do host e clique em **"CONFIRMAR"**.
6. Aguarde na tela de espera até que o host inicie a partida.

## Protocolo da Camada de Aplicação

O jogo utiliza um protocolo de comunicação simples, baseado na troca de mensagens no formato JSON, para sincronizar o estado do jogo entre o host e o cliente. A responsabilidade pela lógica do jogo, como a movimentação da bola e a detecção de colisões, é centralizada no host, que atua como a autoridade da partida.

### Estrutura das Mensagens

As mensagens são dicionários Python serializados em formato JSON e enviados pela rede. A estrutura das mensagens varia dependendo do remetente (host ou cliente).

### Mensagens Enviadas pelo Host para o Cliente:

O host envia periodicamente (a uma taxa de 60Hz) o estado completo e autoritativo do jogo.

```bash
JSON
{
  "y": int,
  "bolax": int,
  "bolay": int,
  "score_jogador": int,
  "score_oponente": int
}
```

* `y:` A posição vertical (eixo Y) da raquete do host.
* `bolax:` A posição horizontal (eixo X) da bola. Importante: O valor é invertido (LARGURA - bola_x) para que a perspectiva do cliente seja espelhada corretamente.
* `bolay:` A posição vertical (eixo Y) da bola.
* `score_jogador:` A pontuação do host.
* `score_oponente:` A pontuação do cliente.

### Mensagens Enviadas pelo Cliente para o Host:

O cliente envia apenas as informações essenciais sobre suas ações, especificamente a posição de sua raquete.

```bash
JSON
{
  "y": 250
}
```

* `y:` A posição vertical (eixo Y) da raquete do cliente.

### Mensagens de Controle

Além das atualizações de estado, o protocolo define mensagens de controle para gerenciar o ciclo de vida da partida.

* **Início do Jogo:** Após a conexão ser estabelecida, o host envia uma mensagem de "start" para sinalizar ao cliente que a partida começou.

    ```bash
    JSON
    {
      "controle": "start"
    }
    ```

* **Fim do Jogo:** Quando um jogador fecha a janela ou a partida termina, uma mensagem de "sair" é enviada para notificar o outro jogador, permitindo que ambas as aplicações encerrem a conexão e o jogo de forma limpa.

    ```bash
    JSON
    {
      "controle": "sair"
    }
    ```

### Sincronização e Fluxo de Dados

1. **Conexão:** O cliente inicia a conexão com o host. Com UDP, o cliente envia uma mensagem inicial para que o host conheça seu endereço.

2. **Início da Partida:** O host aguarda a conexão e, uma vez estabelecida, espera o clique no botão "COMEÇAR". Ao clicar, ele envia a mensagem {"controle": "start"}.

3. **Durante o Jogo:**

    * O host calcula toda a física do jogo (movimento da bola, colisões, pontuação), atualiza seu próprio estado e envia o estado completo para o cliente a cada quadro.

    * O cliente recebe o estado do jogo do host e atualiza sua tela de acordo. Ele apenas lê a posição de sua própria raquete e a envia para o host.

4. **Fim da Partida:** Se a janela do jogo for fechada ou a pontuação máxima for atingida, o lado que encerrou a partida envia a mensagem {"controle": "sair"} para o oponente.