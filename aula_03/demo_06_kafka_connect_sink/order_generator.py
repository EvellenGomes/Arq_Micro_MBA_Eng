from confluent_kafka import Producer
from faker import Faker
import json
import time
import random
from datetime import datetime

# Configuração
fake = Faker('pt_BR')
producer = Producer({'bootstrap.servers': 'localhost:9092'})
topic = 'demo-orders'

statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
products = [
    'Notebook Dell Inspiron', 'Mouse Logitech MX', 'Teclado Mecânico',
    'Monitor LG 27"', 'Webcam Full HD', 'Headset Gamer',
    'SSD Samsung 1TB', 'Memória RAM 16GB', 'Placa de Vídeo RTX'
]

def delivery_callback(err, msg):
    if err:
        print(f'❌ Erro: {err}')
    else:
        print(f'✅ Pedido enviado: {msg.value().decode("utf-8")[:80]}...')

print(f"🚀 Iniciando gerador de pedidos para o tópico '{topic}'...")
print("   Gerando 1 pedido a cada 2 segundos")
print("   Pressione Ctrl+C para parar\n")

order_counter = 1000

try:
    while True:
        # Gera pedido
        order_id = f"ORD-{order_counter}"
        order = {
            "order_id": order_id,
            "customer_name": fake.name(),
            "product": random.choice(products),
            "amount": round(random.uniform(50.0, 5000.0), 2),
            "status": random.choice(statuses),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Envia para Kafka
        producer.produce(
            topic,
            value=json.dumps(order),
            callback=delivery_callback
        )
        producer.poll(0)
        
        order_counter += 1
        time.sleep(2)

except KeyboardInterrupt:
    print("\n\n🛑 Parando gerador...")
finally:
    producer.flush()
    print("✅ Todas as mensagens foram enviadas!")

