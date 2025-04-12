#include <ctype.h>
#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    // checks if only one command-line argument

    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");

        return 1;
    }
    // checks for argv[1] if it's a digit

    for (int k = 0; k < strlen(argv[1]); k++)
    {
        if (isalpha(argv[1][k]))
        {
        printf("Usage: ./caesar key\n");

        return 1;
        }
    }
    // argv[1] string -> int

    int k = atoi(argv[1]) % 26;

    // Prompt user for plaintext
    string plaintext = get_string("plaintext: ");

    printf("ciphertext: ");

    // For each character in the plaintext
    for (int i = 0, length = strlen(plaintext); i < length; i++)
    {
        if(!isalpha(plaintext[i]))
        {
            printf("%c", plaintext[i]);
            continue;
        }
        // Rotate the character if its a letter
        int check = isupper(plaintext[i]) ? 65 : 97;
        int p = plaintext[i] - check;
        int c = (p + k) % 26;

        printf("%c", c + check);
    }
    printf("\n");
    return 0;
}

