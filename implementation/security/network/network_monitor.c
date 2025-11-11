#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_CONNECTIONS 1000

typedef struct {
    char src_ip[16];
    char dst_ip[16];
    int src_port;
    int dst_port;
    time_t timestamp;
    long bytes_sent;
    long bytes_received;
} Connection;

typedef struct {
    Connection connections[MAX_CONNECTIONS];
    int count;
    long total_bytes;
} NetworkMonitor;

void init_monitor(NetworkMonitor *mon) {
    mon->count = 0;
    mon->total_bytes = 0;
}

void add_connection(NetworkMonitor *mon, const char *src, const char *dst, 
                   int sport, int dport, long bytes_sent, long bytes_recv) {
    if (mon->count >= MAX_CONNECTIONS) return;
    
    Connection *conn = &mon->connections[mon->count];
    strncpy(conn->src_ip, src, 15);
    strncpy(conn->dst_ip, dst, 15);
    conn->src_port = sport;
    conn->dst_port = dport;
    conn->timestamp = time(NULL);
    conn->bytes_sent = bytes_sent;
    conn->bytes_received = bytes_recv;
    
    mon->total_bytes += bytes_sent + bytes_recv;
    mon->count++;
}

void print_statistics(NetworkMonitor *mon) {
    printf("\n=== Network Statistics ===\n");
    printf("Total Connections: %d\n", mon->count);
    printf("Total Bytes: %ld\n", mon->total_bytes);
}

int main() {
    NetworkMonitor monitor;
    init_monitor(&monitor);
    
    add_connection(&monitor, "192.168.1.1", "10.0.0.1", 5000, 80, 1024, 2048);
    add_connection(&monitor, "192.168.1.2", "10.0.0.2", 5001, 443, 2048, 4096);
    
    print_statistics(&monitor);
    return 0;
}
