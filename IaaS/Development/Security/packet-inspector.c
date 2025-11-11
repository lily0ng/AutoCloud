#include <stdio.h>

void inspect_packet(const char* packet, int size) {
    printf("🔍 Inspecting packet (%d bytes)\n", size);
    printf("  Protocol: TCP\n");
    printf("  Flags: SYN\n");
}

int main() {
    inspect_packet("packet_data", 1500);
    return 0;
}
