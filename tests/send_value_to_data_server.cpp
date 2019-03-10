#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>


#include <cstring>
#include <iostream>

#define LITTLE_ENDIAN_LOCAL 0
#define HEADER_SIZE 2

/**
 * This function is assuming that the message can fit in out and that out is filled with \0
 * Therefore size of out must be at least the size of name + 2 (header) + 4 (value)
 * @param name
 *      value name
 * @param val
 *      value
 * @param out
 *      message to be filled
 * @return message size
 */
unsigned int make_float_msg(char* name, float val, char* out)
{
    unsigned char name_len = strlen(name);
    out[0] = name_len;
    out[1] = 1;
    strncpy(out + HEADER_SIZE, name, name_len);
    int val_offset = HEADER_SIZE + name_len;
#if LITTLE_ENDIAN_LOCAL
    memcpy(out + val_offset, &val, 4);
#else
#ifdef __cplusplus
    char* val_chars = reinterpret_cast<char*>(&val);
#else
    char* val_chars = (unsigned char*)val;
#endif
    for (int i = 0; i < sizeof(float); ++i)
    {
        out[val_offset + i] = val_chars[sizeof(float) - (i + 1)];
    }
#endif
    return HEADER_SIZE + name_len + sizeof(float);
}

/**
 * This function is assuming that the message can fit in out and that out is filled with \0
 * Therefore size of out must be at least the size of name + 2 (header) + 4 (value)
 * @param name
 *      value name
 * @param val
 *      value
 * @param out
 *      message to be filled
 * @return message size
 */
unsigned int make_int_msg(char* name, int val, char* out)
{
    unsigned char name_len = strlen(name);
    out[0] = name_len;
    out[1] = 1;
    strncpy(out + HEADER_SIZE, name, name_len);
    int val_offset = HEADER_SIZE + name_len;
#if LITTLE_ENDIAN_LOCAL
    memcpy(out + val_offset, &val, 4);
#else
#ifdef __cplusplus
    char* val_chars = reinterpret_cast<char*>(&val);
#else
    char* val_chars = (unsigned char*)val;
#endif
    for (int i = 0; i < sizeof(int); ++i)
    {
        out[val_offset + i] = val_chars[sizeof(int) - (i + 1)];
    }
#endif
    return HEADER_SIZE + name_len + sizeof(int);
}

int main()
{
    const unsigned int PORT = 8080;

    int sockfd, connfd;
    sockaddr_in servaddr, cli;

    // socket create and varification
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd == -1) {
        printf("socket creation failed...\n");
        exit(0);
    }
    else
        printf("Socket successfully created..\n");
    bzero(&servaddr, sizeof(servaddr));

    // assign IP, PORT
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = inet_addr("192.168.0.101");
    servaddr.sin_port = htons(PORT);

    // connect the client socket to server socket
    if (connect(sockfd, (sockaddr*)&servaddr, sizeof(servaddr)) != 0) {
        printf("connection with the server failed...\n");
        exit(0);
    }
    else{
        printf("connected to the server..\n");
    }

    const int BUFF_SIZE = 1028;
    char buff[BUFF_SIZE];
    char* name =  "arduino_3";
    bzero(buff, BUFF_SIZE);
    unsigned int buff_len = make_int_msg(name, 4, buff);

    write(sockfd, buff, buff_len);
    sleep(2);
    write(sockfd, buff, buff_len);
    sleep(2);
    write(sockfd, buff, buff_len);
    sleep(2);
    write(sockfd, buff, buff_len);
}