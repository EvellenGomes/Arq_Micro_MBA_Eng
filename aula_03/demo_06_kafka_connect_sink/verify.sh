#!/bin/bash

echo "🔍 Verificando dados no Postgres..."
echo ""

docker exec postgres psql -U postgres -d demo_db -c "
SELECT 
    order_id,
    customer_name,
    product,
    amount,
    status,
    created_at
FROM orders
ORDER BY created_at DESC
LIMIT 10;
"

echo ""
echo "📊 Total de pedidos:"
docker exec postgres psql -U postgres -d demo_db -c "
SELECT COUNT(*) as total_orders FROM orders;
"

echo ""
echo "📈 Pedidos por status:"
docker exec postgres psql -U postgres -d demo_db -c "
SELECT status, COUNT(*) as count
FROM orders
GROUP BY status
ORDER BY count DESC;
"

