#include <cs50.h>
#include <stdio.h>

void print_row(int spaces, int bricks1, int bricks2);
int height;

int main(void)
{
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    for (int i = 0; i < height; i++)
    {
        print_row(i + 1, i + 1, i + 1);
    }
}

void print_row(int spaces, int bricks1, int bricks2)
{
    for (int i = height; i > spaces; i--)
    {
        printf(" ");
    }
    for (int i = 0; i < bricks1; i++)
    {
        printf("#");
    }
    printf("  ");
    for (int i = 0; i < bricks2; i++)
    {
        printf("#");
    }
    printf("\n");
}
