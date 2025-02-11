// Pyramid of hashtags with a height of the user's choice - Problem set 1 (2/3)

#include <cs50.h>
#include <stdio.h>

void print_row(int length, int height);

int main(void)
{
    int height = get_int("Height: ");
    for (int i = 0; i < height; i++)
    {
        print_row(i + 1, height);
    }
}

void print_row(int length, int height)
{
    for (int i = 0; i < height - length; i++)
    {
        printf(" ");
    }
    for (int i = 0; i < length; i++)
    {
        printf("#");
    }
    printf("\n");
}
