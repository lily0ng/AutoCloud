interface Connection {
  id: string;
  name: string;
  type: 'vpn' | 'direct-connect' | 'express-route';
  onPremise: string;
  cloud: string;
  bandwidth: number;
  status: 'active' | 'inactive' | 'degraded';
}

class HybridConnector {
  private connections: Map<string, Connection> = new Map();

  createConnection(
    name: string,
    type: Connection['type'],
    onPremise: string,
    cloud: string,
    bandwidth: number
  ): Connection {
    const connection: Connection = {
      id: `conn-${Date.now()}`,
      name,
      type,
      onPremise,
      cloud,
      bandwidth,
      status: 'active',
    };

    this.connections.set(connection.id, connection);
    console.log(`🔗 Connection established: ${name} (${type})`);

    return connection;
  }

  monitorConnection(connectionId: string): void {
    const conn = this.connections.get(connectionId);
    if (!conn) {
      console.log(`❌ Connection not found: ${connectionId}`);
      return;
    }

    const latency = Math.random() * 100;
    const packetLoss = Math.random() * 5;

    console.log(`\n📊 Connection Monitor: ${conn.name}`);
    console.log(`   Status: ${conn.status}`);
    console.log(`   Latency: ${latency.toFixed(2)}ms`);
    console.log(`   Packet Loss: ${packetLoss.toFixed(2)}%`);
    console.log(`   Bandwidth: ${conn.bandwidth}Mbps`);

    if (latency > 50 || packetLoss > 2) {
      conn.status = 'degraded';
      console.log(`⚠️  Connection degraded: ${conn.name}`);
    }
  }

  listConnections(): Connection[] {
    return Array.from(this.connections.values());
  }

  testConnectivity(connectionId: string): boolean {
    const conn = this.connections.get(connectionId);
    if (!conn) {
      return false;
    }

    console.log(`🔍 Testing connectivity: ${conn.name}`);
    console.log(`   ${conn.onPremise} <-> ${conn.cloud}`);

    const success = Math.random() > 0.1;
    console.log(success ? '✅ Connection successful' : '❌ Connection failed');

    return success;
  }

  syncData(connectionId: string, data: string[]): void {
    const conn = this.connections.get(connectionId);
    if (!conn || conn.status !== 'active') {
      console.log('❌ Cannot sync: connection unavailable');
      return;
    }

    console.log(`🔄 Syncing data via ${conn.name}...`);
    data.forEach(item => {
      console.log(`   ✓ ${item}`);
    });
    console.log('✅ Data sync complete');
  }

  generateReport(): void {
    console.log('\n📋 Hybrid Cloud Connectivity Report');
    console.log('===================================');

    const connections = this.listConnections();
    const active = connections.filter(c => c.status === 'active').length;
    const degraded = connections.filter(c => c.status === 'degraded').length;

    console.log(`Total Connections: ${connections.length}`);
    console.log(`Active: ${active}`);
    console.log(`Degraded: ${degraded}`);

    console.log('\nConnection Details:');
    connections.forEach(conn => {
      const statusIcon = conn.status === 'active' ? '✅' : '⚠️';
      console.log(`${statusIcon} ${conn.name} (${conn.type}): ${conn.onPremise} <-> ${conn.cloud}`);
    });
  }
}

// Example usage
const connector = new HybridConnector();

connector.createConnection(
  'Primary VPN',
  'vpn',
  'on-prem-dc-1',
  'aws-vpc-us-east-1',
  1000
);

connector.createConnection(
  'Direct Connect',
  'direct-connect',
  'on-prem-dc-2',
  'aws-vpc-us-west-2',
  10000
);

connector.monitorConnection('conn-1');
connector.testConnectivity('conn-1');
connector.syncData('conn-1', ['database-backup.sql', 'logs.tar.gz']);

connector.generateReport();
