#include <stdio.h>
#include <string.h>
#include <unistd.h>

// Função de ataque para SSH (simulada)
// Em um motor real, usaria-se uma biblioteca como a libssh2
int attempt_ssh(const char* host, const char* user, const char* password) {
    printf("[C ENGINE] Probing SSH: %s@%s with pass: %s\n", user, host, password);
    fflush(stdout); // Garante que a saída seja vista pelo Python
    
    // Simulação: Sucesso se a senha for "admin123"
    if (strcmp(password, "admin123") == 0) {
        return 1; // Sucesso
    }
    usleep(50000); // Pequeno delay para simular a latência da rede
    return 0; // Falha
}

// Função de ataque para IMAP (simulada)
// Em um motor real, usaria-se sockets e comandos IMAP
int attempt_imap(const char* host, const char* user, const char* password) {
    printf("[C ENGINE] Probing IMAP: %s on %s with pass: %s\n", user, host, password);
    fflush(stdout);
    
    // Simulação: Sucesso se a senha for "password123"
    if (strcmp(password, "password123") == 0) {
        return 1; // Sucesso
    }
    usleep(50000);
    return 0; // Falha
}
