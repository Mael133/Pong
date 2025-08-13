import socket
from ipaddress import IPv4Address, IPv6Address, ip_address
import json

# cria e retorna uma referência a um socket
# do tipo especificado
def criarSocket(ip, protocolo):
    
    try: # checa o tipo de ip usado e seleciona o tipo de socket apropriado
        if isinstance(ip_address(ip), IPv4Address):
            tipoIP = socket.AF_INET
        elif isinstance(ip_address(ip), IPv6Address):
            tipoIP = socket.AF_INET6
    except ValueError:
        raise ValueError(f"IP inválido: {ip}")
    
    # checa o protocolo usado e seleciona o tipo de socket apropriado
    if protocolo == "tcp":
        tipoSocket = socket.SOCK_STREAM
    else:
        tipoSocket = socket.SOCK_DGRAM

    # cria o socket de acordo com os parâmetros passados
    sock = socket.socket(tipoIP, tipoSocket)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return sock

# envia um dicionário em formato de JSON serializado pela rede
def enviarDados(sock, dados, protocolo, oponente_addr=None):
    # cria um JSON com o dicionário em utf-8
    dados = json.dumps(dados).encode("utf-8")

    # manda os dados pela rede usando o protocolo correto
    try:
        if protocolo == "tcp":
            sock.sendall(dados)
        else:
            if oponente_addr: # só manda por UDP se um endereço foi passado
                sock.sendto(dados, oponente_addr)
    except socket.error as e:
        print(f"Erro ao enviar dados: {e}")

# recebe e desserializa um dicionário em formato de JSON pela rede
def receberDados(sock, protocolo, buffer=1024):

    # essa função retorna o endereço do outro lado da conexão
    # porque o protocolo UDP não faz esse controle automaticamente,
    # então a aplicação tem que lidar com essa limitação e guardar o 
    # IP do computador conectado para conseguir mandar mensagens de 
    # volta.

    # recebe o JSON usando o protocolo correto
    try:
        if protocolo == 'tcp':
            payload = sock.recv(buffer)
            if not payload:
                return None, None
            oponente_addr = None
        else:
            payload, oponente_addr = sock.recvfrom(buffer)

        # decodifica o JSON em um dicionário python
        dados = json.loads(payload.decode('utf-8'))
        return dados, oponente_addr
    except (socket.error, json.JSONDecodeError, ConnectionResetError) as e:
        print(f"Erro ao receber dados. {e}")
        return None, None