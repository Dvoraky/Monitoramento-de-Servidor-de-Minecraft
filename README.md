# Monitoramento-de-Servidor-de-Minecraft
Monitoramento de um servidor de Minecraft utilizando do Crafty, Kafka e Spark.

## Rodando o Servidor Kafka

Use:

```bash
docker compose up
```

## Rodando as Aplicações Python

Crie o ambiente virtual na pasta App:

```bash
python3 -m venv App/venv
```

Ative o ambiente:
- Em Linux:
```bash
source App/vnev/bin/activate
```
- Em Windows:
```bash
cd App/venv/Scripts/
activate
```

Instale as dependências:

```bash
pip install -r <caminhoAtéRequirements.txt>
```

Rodando o consumidor:
```bash
python App/consumer.py
```

Rodando o produtor:
```bash
python App/producer.py
```

Desativando o ambiente virtual:
```bash
deactivate
```