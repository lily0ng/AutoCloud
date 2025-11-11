#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/aes.h>
#include <openssl/rand.h>

#define AES_KEY_SIZE 256
#define AES_BLOCK_SIZE 16

typedef struct {
    unsigned char key[32];
    unsigned char iv[AES_BLOCK_SIZE];
} EncryptionContext;

void generate_key(EncryptionContext *ctx) {
    RAND_bytes(ctx->key, sizeof(ctx->key));
    RAND_bytes(ctx->iv, sizeof(ctx->iv));
}

int encrypt_data(EncryptionContext *ctx, const unsigned char *plaintext, 
                 int plaintext_len, unsigned char *ciphertext) {
    AES_KEY enc_key;
    AES_set_encrypt_key(ctx->key, AES_KEY_SIZE, &enc_key);
    
    unsigned char iv_copy[AES_BLOCK_SIZE];
    memcpy(iv_copy, ctx->iv, AES_BLOCK_SIZE);
    
    AES_cbc_encrypt(plaintext, ciphertext, plaintext_len, &enc_key, iv_copy, AES_ENCRYPT);
    return plaintext_len;
}

int decrypt_data(EncryptionContext *ctx, const unsigned char *ciphertext,
                 int ciphertext_len, unsigned char *plaintext) {
    AES_KEY dec_key;
    AES_set_decrypt_key(ctx->key, AES_KEY_SIZE, &dec_key);
    
    unsigned char iv_copy[AES_BLOCK_SIZE];
    memcpy(iv_copy, ctx->iv, AES_BLOCK_SIZE);
    
    AES_cbc_encrypt(ciphertext, plaintext, ciphertext_len, &dec_key, iv_copy, AES_DECRYPT);
    return ciphertext_len;
}

int main() {
    EncryptionContext ctx;
    generate_key(&ctx);
    
    const char *message = "Sensitive data to encrypt";
    unsigned char ciphertext[128];
    unsigned char decrypted[128];
    
    int len = strlen(message);
    int padded_len = ((len / AES_BLOCK_SIZE) + 1) * AES_BLOCK_SIZE;
    
    encrypt_data(&ctx, (unsigned char *)message, padded_len, ciphertext);
    printf("Data encrypted successfully\n");
    
    decrypt_data(&ctx, ciphertext, padded_len, decrypted);
    printf("Decrypted: %s\n", decrypted);
    
    return 0;
}
