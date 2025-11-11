#include <stdio.h>
#include <string.h>

int detect_threat(const char* traffic) {
    if (strstr(traffic, "malicious") != NULL) {
        printf("🚨 Threat detected!\n");
        return 1;
    }
    return 0;
}

int main() {
    detect_threat("normal traffic");
    detect_threat("malicious payload");
    return 0;
}
