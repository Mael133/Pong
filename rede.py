import socket
from ipaddress import IPv4Address, IPv6Address, ip_address
import json

def criarSocket(ip, protocolo):
    try:
        if isinstance(ip_address(ip), IPv4Address):
            tipoIP = socket.AF_INET
        elif isinstance(ip_address(ip), IPv6Address):
            tipoIP = socket.AF_INET6
    except ValueError:
        raise ValueError(f"IP inválido: {ip}")
    
    if protocolo == "tcp":
        tipoSocket = socket.SOCK_STREAM
    else:
        tipoSocket = socket.SOCK_DGRAM

    sock = socket.socket(tipoIP, tipoSocket)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return sock

def enviarDados(sock, dados, protocolo, oponente_addr=None):
    dados = json.dumps(dados).encode('utf-8')
    try:
        if protocolo == 'tcp':
            sock.sendall(dados)
        else:
            if oponente_addr:
                sock.sendto(dados, oponente_addr)
    except socket.error as e:
        print(f"Erro ao enviar dados: {e}")

def receberDados(sock, protocolo, buffer=1024):
    try:
        if protocolo == 'tcp':
            payload = sock.recv(buffer)
            if not payload:
                return None, None
            oponente_addr = None
        else:
            payload, oponente_addr = sock.recvfrom(buffer)

        dados = json.loads(payload.decode('utf-8'))
        return dados, oponente_addr
    except (socket.error, json.JSONDecodeError, ConnectionResetError) as e:
        print(f"Erro ao receber dados. {e}")
        return None, None