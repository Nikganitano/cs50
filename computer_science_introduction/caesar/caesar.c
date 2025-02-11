// Encrypts messages using Caesar’s cipher - Problem set 2 (3/3)

#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <string.h>

char rotate(char c, int key, char base)
{
    return (c - base + key) % 26 + base;
}

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Error: Invalid number of arguments\n");
        return 1;
    }

    for (int i = 0; argv[1][i]; i++)
    {
        if (!isdigit(argv[1][i]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }

    int key = atoi(argv[1]);

    printf("plaintext:  ");
    char plaintext[256];
    fgets(plaintext, sizeof(plaintext), stdin);

    printf("ciphertext: ");
    for (int i = 0, len = strlen(plaintext); i < len; i++)
    {
        char c = plaintext[i];
        if (isupper(c))
        {
            putchar(rotate(c, key, 'A'));
        }
        else if (islower(c))
        {
            putchar(rotate(c, key, 'a'));
        }
        else
        {
            putchar(c);
        }
    }

    printf("\n");
    return 0;
}
