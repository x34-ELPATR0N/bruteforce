#include <stdio.h>
#include <string.h>
#include <unistd.h>

//.
//.
int attempt_ssh(const char* host, const char* user, const char* password) {
    printf("[C ENGINE] Probing SSH: %s@%s with pass: %s\n", user, host, password);
    fflush(stdout); //.
    
    //.
    if (strcmp(password, "admin123") == 0) {
        return 1; // Sucesso
    }
    usleep(50000); //.e
    return 0; // Falha
}

//.
//.
int attempt_imap(const char* host, const char* user, const char* password) {
    printf("[C ENGINE] Probing IMAP: %s on %s with pass: %s\n", user, host, password);
    fflush(stdout);
    
    //.
    if (strcmp(password, "password123") == 0) {
        return 1; // Sucesso
    }
    usleep(50000);
    return 0; // Falha
}
