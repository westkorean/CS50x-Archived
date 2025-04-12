#include <cs50.h>
#include <stdio.h>

long get_credit_number(void);
long checksum(long credit_number);
void finalcheck(long check_sum, long credit_number);


int main(void)
{
    long credit_number = get_credit_number();
    long check_sum = checksum(credit_number);
    finalcheck(check_sum, credit_number);
}



//Credit card number?
long get_credit_number(void)
{
    long credit_num;
    do
    {
        credit_num = get_long("Number: ");
    }
    while (credit_num <= 0);
    return credit_num;
}


//Luhm algorithm
long checksum(long credit_number)
{
    long sum = 0;
    long last_digit;
    long credit_card_number = credit_number;
    // Luhm's algorithm 1
    while (credit_card_number > 0)
    {
        last_digit = credit_card_number % 10;
        sum = sum + last_digit ;
        credit_card_number = credit_card_number / 100;
    }

    credit_card_number = credit_number / 10;
    long two_times;
    // Luhm's algorithm 2
    while (credit_card_number > 0)
    {
        last_digit = credit_card_number % 10;
        two_times = 2 * last_digit;
        sum = sum + (two_times % 10) + (two_times / 10);
        credit_card_number = credit_card_number / 100;
    }
    sum = sum % 10;
    //0?
    if (sum == 0)
    {
        return 1;
    }
    else
    {
        return 0;
    }
}

//Final check
void finalcheck(long check_sum, long credit_number)
{
    long valid_cc = credit_number;
    int length = 0;
    long divisor = 10;
    int first_digit;
    int first_twodigit;

    if (check_sum == 1)
    {
        //length of credit card #
        while (valid_cc > 0)
        {
            valid_cc = valid_cc / 10;
            length++;
        }

        //1st two digits of credit card #
        valid_cc = credit_number;
        for (int i = 0; i < (length - 2); i++)
        {
            divisor = divisor * 10;
        }

        first_digit = valid_cc / divisor;
        first_twodigit = valid_cc / (divisor / 10);

        //AMEX
        if (length == 15 && (first_twodigit == 34 || first_twodigit ==
        37))
        {
            printf("AMEX\n");
        }
        //MASTERCARD
        else if (length == 16 && (first_twodigit == 50 || first_twodigit == 51 || first_twodigit == 52 || first_twodigit == 53 || first_twodigit == 54 || first_twodigit == 55))
        {
            printf("MASTERCARD\n");
        }
        //VISA
        else if ((length == 13 || length == 16) && first_digit == 4)
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}
