import os
import time
import requests
import urllib3
import html
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from dotenv import load_dotenv
from threading import Thread

load_dotenv()

BASE_URL = os.getenv('BASE_URL')
TOKEN = os.getenv('TOKEN')
SERVER_ID = os.getenv('SERVER_ID')

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PROIBIDO = ["fdp", "corno", "desgraçado"]

jogadores_online = {}
tempo_total_jogadores = {}

def send_command_to_server(command):
    url = f"{BASE_URL}/servers/{SERVER_ID}/stdin"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "text/plain",
    }

    try:
        print(f"Enviando comando: {command}") 
        response = requests.post(url, headers=headers, data=command, verify=False)

        if response.status_code == 200:
            print(f"Comando enviado com sucesso: {command}")
        else:
            print(f"Erro ao enviar comando: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")

def monitor_server_logs():
    url = f"{BASE_URL}/servers/{SERVER_ID}/logs"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
    }

    ultimo_log = set()

    while True:
        try:
            response = requests.get(url, headers=headers, verify=False)

            if response.status_code == 200:
                logs = response.json().get("data", [])
                novos_logs = [log for log in logs if log not in ultimo_log]

                for log in novos_logs:
                    log_decoded = html.unescape(log)  
                    ultimo_log.add(log)
                    print(log_decoded)

                    if "joined the game" in log_decoded.lower():
                        jogador = extrair_jogador_entrada(log_decoded)
                        if jogador:
                            jogadores_online[jogador] = datetime.now()
                            if jogador not in tempo_total_jogadores:
                                tempo_total_jogadores[jogador] = 0

                    elif "left the game" in log_decoded.lower():
                        jogador = extrair_jogador_saida(log_decoded)
                        if jogador and jogador in jogadores_online:
                            tempo_logado = (datetime.now() - jogadores_online.pop(jogador)).total_seconds()
                            tempo_total_jogadores[jogador] += tempo_logado

                    elif "<" in log_decoded and ">" in log_decoded:
                        mensagem = extrair_mensagem_chat(log_decoded)
                        jogador = extrair_jogador_chat(log_decoded)

                        if jogador and mensagem:
                            for palavra in PROIBIDO:
                                if palavra in mensagem.lower():
                                    print(f"Jogador {jogador} usou uma palavra proibida: {palavra}")
                                    send_command_to_server(f"kick {jogador} Uso de linguagem/procedimento proibido")
            else:
                print(f"Erro ao obter logs: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
        
        time.sleep(2)

def extrair_jogador_entrada(log):
    if "joined the game" in log.lower():
        partes = log.split()
        if len(partes) > 2:
            return partes[2]
    return None

def extrair_jogador_saida(log):
    if "left the game" in log.lower():
        partes = log.split()
        if len(partes) > 2:
            return partes[2]
    return None

def extrair_jogador_chat(log):
    if "<" in log and ">" in log:
        partes = log.split()
        for parte in partes:
            if parte.startswith("<") and parte.endswith(">"):
                return parte.strip("<>")
    return None

def extrair_mensagem_chat(log):
    if "<" in log and ">" in log:
        partes = log.split(">", 1)
        if len(partes) > 1:
            return partes[1].strip()
    return None

def atualizar_grafico(frame):
    jogadores = list(tempo_total_jogadores.keys())
    tempos = [
        tempo_total_jogadores[jogador] +
        ((datetime.now() - jogadores_online[jogador]).total_seconds() if jogador in jogadores_online else 0)
        for jogador in jogadores
    ]

    ax.clear()
    ax.barh(jogadores, tempos, color="pink")
    ax.set_xlabel("Tempo logado (segundos)")
    ax.set_title("Tempo logado dos jogadores")
    ax.set_xlim(0, max(tempos) + 10 if tempos else 10)

fig, ax = plt.subplots()
ani = FuncAnimation(fig, atualizar_grafico, interval=2000)

if __name__ == "__main__":
    print("Monitorando logs do servidor e exibindo gráfico...")
    Thread(target=monitor_server_logs, daemon=True).start()
    plt.show()
