#include <stdio.h>

int check_firewall(int port, const char* protocol) {
    printf("🔥 Checking firewall: %s/%d\n", protocol, port);
    if (port == 22 || port == 443) {
        printf("  ✅ Allowed\n");
        return 1;
    }
    printf("  ❌ Blocked\n");
    return 0;
}

int main() {
    check_firewall(22, "tcp");
    check_firewall(1234, "tcp");
    return 0;
}
