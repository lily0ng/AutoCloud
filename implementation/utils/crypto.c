#include <stdio.h>
#include <string.h>
#include <openssl/sha.h>
#include <openssl/md5.h>

void sha256_hash(const char *input, char *output) {
    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256_CTX sha256;
    SHA256_Init(&sha256);
    SHA256_Update(&sha256, input, strlen(input));
    SHA256_Final(hash, &sha256);
    
    for(int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
        sprintf(output + (i * 2), "%02x", hash[i]);
    }
    output[64] = 0;
}

void md5_hash(const char *input, char *output) {
    unsigned char hash[MD5_DIGEST_LENGTH];
    MD5_CTX md5;
    MD5_Init(&md5);
    MD5_Update(&md5, input, strlen(input));
    MD5_Final(hash, &md5);
    
    for(int i = 0; i < MD5_DIGEST_LENGTH; i++) {
        sprintf(output + (i * 2), "%02x", hash[i]);
    }
    output[32] = 0;
}

int verify_hash(const char *input, const char *expected_hash) {
    char calculated[65];
    sha256_hash(input, calculated);
    return strcmp(calculated, expected_hash) == 0;
}

int main() {
    const char *data = "Hello, World!";
    char sha256_output[65];
    char md5_output[33];
    
    sha256_hash(data, sha256_output);
    printf("SHA256: %s\n", sha256_output);
    
    md5_hash(data, md5_output);
    printf("MD5: %s\n", md5_output);
    
    printf("Verification: %s\n", verify_hash(data, sha256_output) ? "PASS" : "FAIL");
    
    return 0;
}
