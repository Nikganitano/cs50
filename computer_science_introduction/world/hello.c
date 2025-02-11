// Hello world program in C - Problem set 1 (1/3)

#include <cs50.h>
#include <stdio.h>

int main(void)
{
    string name = get_string("What is your name? ");
    printf("Hello, %s\n", name);
}
