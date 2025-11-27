# Demo 6: Kafka Connect JDBC Sink com UPSERT

Esta demo demonstra como usar o **Kafka Connect** para persistir automaticamente dados do Kafka em um banco de dados Postgres, usando o modo **UPSERT** (insert ou update).

## Conceito

Simula um sistema de e-commerce que gera pedidos continuamente. Os pedidos são enviados para um tópico Kafka e o Kafka Connect os persiste automaticamente no Postgres.

```
[Python Producer (Faker)] 
    ↓ (JSON)
[Tópico: demo-orders]
    ↓ (Connect consome)
[JDBC Sink Connector - UPSERT]
    ↓ (persiste)
[Tabela Postgres: orders]
```

## Pré-requisitos

1. Ambiente Docker rodando (com Postgres e Kafka Connect):
```bash
cd ../../aula_01
docker compose up -d
```

2. Aguarde ~30 segundos para o Kafka Connect instalar o plugin JDBC.

## Passo a Passo

### 1. Configurar o Ambiente

Execute o script de setup que cria o tópico e registra o conector:

```bash
bash setup.sh
```

**O que ele faz:**
- Cria o tópico `demo-orders` com 3 partições
- Aguarda o Kafka Connect estar pronto
- Registra o JDBC Sink Connector com configuração de UPSERT
- Mostra o status do conector

### 2. Iniciar o Gerador de Pedidos

Em um terminal separado, execute:

```bash
python order_generator.py
```

**O que acontece:**
- Gera 1 pedido a cada 2 segundos usando Faker
- Cada pedido tem: ID, nome do cliente, produto, valor, status e timestamps
- Os pedidos são enviados para o tópico `demo-orders`

### 3. Verificar os Dados no Postgres

Em outro terminal, execute:

```bash
bash verify.sh
```

**O que você verá:**
- Os 10 pedidos mais recentes
- Total de pedidos na tabela
- Distribuição de pedidos por status

## Testando o UPSERT

O modo UPSERT significa que se você enviar um pedido com um `order_id` que já existe, ele será **atualizado** em vez de duplicado.

**Teste:**
1. Deixe o producer rodando por ~30 segundos
2. Pare o producer (Ctrl+C)
3. Modifique o `order_generator.py` para gerar IDs fixos (ex: sempre `ORD-1000`)
4. Execute novamente
5. Rode `bash verify.sh` e veja que o contador não aumenta, mas o registro é atualizado

## Configuração do Conector

O arquivo `connector-config.json` define:

- **insert.mode: "upsert"** - Faz UPDATE se a chave primária já existir
- **pk.fields: "order_id"** - Define qual campo é a chave primária
- **auto.create: true** - Cria a tabela automaticamente se não existir
- **auto.evolve: true** - Adiciona colunas automaticamente se o schema mudar

## Limpeza

Para parar tudo:

```bash
# Parar o producer (Ctrl+C no terminal dele)

# Remover o conector
curl -X DELETE http://localhost:8083/connectors/jdbc-sink-orders-demo

# Parar os containers
cd ../../aula_01
docker compose down
```

## Troubleshooting

**Erro: "Connection refused" ao registrar conector**
- Aguarde mais tempo. O Kafka Connect demora ~30s para instalar o plugin JDBC.
- Verifique: `curl http://localhost:8083/`

**Tabela não está sendo criada**
- Verifique o status do conector: `curl http://localhost:8083/connectors/jdbc-sink-orders-demo/status`
- Veja os logs: `docker logs kafka-connect`

**Producer não conecta**
- Certifique-se que o Kafka está rodando: `docker ps | grep kafka`

