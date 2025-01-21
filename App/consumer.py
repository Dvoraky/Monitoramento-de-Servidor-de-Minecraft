from quixstreams import Application
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import json
import threading

app = Application(broker_address="localhost:9092", loglevel="DEBUG")

dados_kafka_tempo_de_jogo = {"jogadores": [], "tempos": []}
dados_kafka_conquistas = {"jogadores" : [], "conquistas" : []}

def gerar_grafico_tempo_de_jogo(frame):
    global dados_kafka_tempo_de_jogo

    jogadores = dados_kafka_tempo_de_jogo["jogadores"]
    tempos = dados_kafka_tempo_de_jogo["tempos"]

    ax.clear()
    ax.barh(jogadores, tempos, color="pink")
    ax.set_xlabel("Tempo logado (segundos)")
    ax.set_title("Tempo logado dos jogadores")
    ax.set_xlim(0, max(tempos) + 1 if tempos else 1)

def gerar_grafico_conquista(frame):
    global dados_kafka_conquistas

    jogadores = dados_kafka_conquistas["jogadores"]
    conquistas = dados_kafka_conquistas["conquistas"]

    ax2.clear()
    ax2.barh(jogadores, conquistas)
    ax2.set_xlabel("Número de conquistas")
    ax2.set_title("Número de conquista dos jogadores")
    ax2.set_xlim(0, max(conquistas) + 10 if conquistas else 10)


fig, ax = plt.subplots()
ani = FuncAnimation(fig, gerar_grafico_tempo_de_jogo, interval=2000, cache_frame_data=False)

fig2, ax2 = plt.subplots()
ani2 = FuncAnimation(fig2, gerar_grafico_conquista, interval=2000, cache_frame_data=False)

def consumir_mensagens():
    global dados_kafka_tempo_de_jogo 
    global dados_kafka_conquistas

    with app.get_consumer() as consumer:
        consumer.subscribe(["tempo_logado", "conquista"])
        while True:
            msg = consumer.poll(1)
            if msg:
                if msg.error() is None:
                    print("Mensagem recebida do Kafka:", msg.value())
                    if msg.topic() == "tempo_logado":
                        dados_kafka_tempo_de_jogo = json.loads(msg.value()) 
                    elif msg.topic() == "conquista":
                        dados_kafka_conquistas = json.loads(msg.value()) 

threading.Thread(target=consumir_mensagens, daemon=True).start()
plt.show()
