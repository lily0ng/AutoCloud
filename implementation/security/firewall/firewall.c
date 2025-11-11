#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>

#define MAX_RULES 100
#define IP_LEN 16

typedef enum {
    ALLOW,
    DENY
} Action;

typedef struct {
    char source_ip[IP_LEN];
    char dest_ip[IP_LEN];
    int port;
    Action action;
    int active;
} FirewallRule;

typedef struct {
    FirewallRule rules[MAX_RULES];
    int rule_count;
} Firewall;

void init_firewall(Firewall *fw) {
    fw->rule_count = 0;
    memset(fw->rules, 0, sizeof(fw->rules));
}

int add_rule(Firewall *fw, const char *src_ip, const char *dst_ip, int port, Action action) {
    if (fw->rule_count >= MAX_RULES) {
        return -1;
    }
    
    FirewallRule *rule = &fw->rules[fw->rule_count];
    strncpy(rule->source_ip, src_ip, IP_LEN - 1);
    strncpy(rule->dest_ip, dst_ip, IP_LEN - 1);
    rule->port = port;
    rule->action = action;
    rule->active = 1;
    
    fw->rule_count++;
    return 0;
}

int check_packet(Firewall *fw, const char *src_ip, const char *dst_ip, int port) {
    for (int i = 0; i < fw->rule_count; i++) {
        FirewallRule *rule = &fw->rules[i];
        if (!rule->active) continue;
        
        if ((strcmp(rule->source_ip, "*") == 0 || strcmp(rule->source_ip, src_ip) == 0) &&
            (strcmp(rule->dest_ip, "*") == 0 || strcmp(rule->dest_ip, dst_ip) == 0) &&
            (rule->port == 0 || rule->port == port)) {
            return rule->action;
        }
    }
    return DENY;
}

void print_rules(Firewall *fw) {
    printf("\n=== Firewall Rules ===\n");
    for (int i = 0; i < fw->rule_count; i++) {
        FirewallRule *rule = &fw->rules[i];
        printf("Rule %d: %s -> %s:%d [%s]\n", 
               i + 1, rule->source_ip, rule->dest_ip, rule->port,
               rule->action == ALLOW ? "ALLOW" : "DENY");
    }
}

int main() {
    Firewall fw;
    init_firewall(&fw);
    
    add_rule(&fw, "*", "*", 80, ALLOW);
    add_rule(&fw, "*", "*", 443, ALLOW);
    add_rule(&fw, "192.168.1.100", "*", 0, DENY);
    add_rule(&fw, "*", "*", 22, ALLOW);
    
    print_rules(&fw);
    
    printf("\nTesting packets:\n");
    printf("192.168.1.1:80 -> %s\n", check_packet(&fw, "192.168.1.1", "10.0.0.1", 80) == ALLOW ? "ALLOWED" : "DENIED");
    printf("192.168.1.100:80 -> %s\n", check_packet(&fw, "192.168.1.100", "10.0.0.1", 80) == ALLOW ? "ALLOWED" : "DENIED");
    
    return 0;
}
