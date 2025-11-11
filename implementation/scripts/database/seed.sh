#!/bin/bash
# Database Seeding Script

set -e

DB_HOST=${DB_HOST:-localhost}
DB_PORT=${DB_PORT:-5432}
DB_NAME=${DB_NAME:-appdb}
DB_USER=${DB_USER:-admin}

echo "========================================="
echo "Seeding Database"
echo "========================================="

# Create sample users
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME <<EOF
INSERT INTO users (username, email, password_hash, role) VALUES
('admin', 'admin@autocloud.com', '\$2b\$12\$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIiLiKpAWK', 'admin'),
('user1', 'user1@autocloud.com', '\$2b\$12\$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIiLiKpAWK', 'user'),
('user2', 'user2@autocloud.com', '\$2b\$12\$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIiLiKpAWK', 'user')
ON CONFLICT (username) DO NOTHING;

-- Create sample transactions
INSERT INTO transactions (user_id, transaction_type, amount, status) VALUES
(1, 'payment', 100.00, 'processed'),
(1, 'refund', 50.00, 'processed'),
(2, 'payment', 200.00, 'pending'),
(2, 'payment', 150.00, 'processed'),
(3, 'payment', 75.00, 'processed')
ON CONFLICT DO NOTHING;

-- Create audit logs
INSERT INTO audit_logs (user_id, action, resource, ip_address) VALUES
(1, 'login', '/auth/login', '192.168.1.1'),
(1, 'create', '/api/transactions', '192.168.1.1'),
(2, 'login', '/auth/login', '192.168.1.2'),
(2, 'read', '/api/users', '192.168.1.2')
ON CONFLICT DO NOTHING;
EOF

echo ""
echo "✓ Database seeded successfully"
echo "========================================="
