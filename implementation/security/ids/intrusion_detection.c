#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_SIGNATURES 100
#define MAX_EVENTS 1000

typedef struct {
    char pattern[256];
    int severity;
    char description[256];
} Signature;

typedef struct {
    time_t timestamp;
    char source_ip[16];
    char event_type[64];
    int severity;
} SecurityEvent;

typedef struct {
    Signature signatures[MAX_SIGNATURES];
    int signature_count;
    SecurityEvent events[MAX_EVENTS];
    int event_count;
} IDS;

void init_ids(IDS *ids) {
    ids->signature_count = 0;
    ids->event_count = 0;
}

void add_signature(IDS *ids, const char *pattern, int severity, const char *desc) {
    if (ids->signature_count >= MAX_SIGNATURES) return;
    
    Signature *sig = &ids->signatures[ids->signature_count];
    strncpy(sig->pattern, pattern, sizeof(sig->pattern) - 1);
    sig->severity = severity;
    strncpy(sig->description, desc, sizeof(sig->description) - 1);
    
    ids->signature_count++;
}

void log_event(IDS *ids, const char *source_ip, const char *event_type, int severity) {
    if (ids->event_count >= MAX_EVENTS) return;
    
    SecurityEvent *event = &ids->events[ids->event_count];
    event->timestamp = time(NULL);
    strncpy(event->source_ip, source_ip, sizeof(event->source_ip) - 1);
    strncpy(event->event_type, event_type, sizeof(event->event_type) - 1);
    event->severity = severity;
    
    ids->event_count++;
    
    printf("[IDS] Alert: %s from %s (Severity: %d)\n", event_type, source_ip, severity);
}

int analyze_traffic(IDS *ids, const char *data, const char *source_ip) {
    for (int i = 0; i < ids->signature_count; i++) {
        if (strstr(data, ids->signatures[i].pattern) != NULL) {
            log_event(ids, source_ip, ids->signatures[i].description, ids->signatures[i].severity);
            return 1;
        }
    }
    return 0;
}

void print_statistics(IDS *ids) {
    printf("\n=== IDS Statistics ===\n");
    printf("Total Signatures: %d\n", ids->signature_count);
    printf("Total Events: %d\n", ids->event_count);
    
    int critical = 0, high = 0, medium = 0, low = 0;
    for (int i = 0; i < ids->event_count; i++) {
        switch (ids->events[i].severity) {
            case 4: critical++; break;
            case 3: high++; break;
            case 2: medium++; break;
            case 1: low++; break;
        }
    }
    
    printf("Critical: %d, High: %d, Medium: %d, Low: %d\n", critical, high, medium, low);
}

int main() {
    IDS ids;
    init_ids(&ids);
    
    add_signature(&ids, "DROP TABLE", 4, "SQL Injection Attempt");
    add_signature(&ids, "<script>", 3, "XSS Attempt");
    add_signature(&ids, "../", 3, "Path Traversal Attempt");
    add_signature(&ids, "cmd.exe", 4, "Command Injection");
    
    analyze_traffic(&ids, "SELECT * FROM users WHERE id=1 OR 1=1", "192.168.1.100");
    analyze_traffic(&ids, "<script>alert('xss')</script>", "192.168.1.101");
    analyze_traffic(&ids, "GET /../../../etc/passwd", "192.168.1.102");
    
    print_statistics(&ids);
    
    return 0;
}
