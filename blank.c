#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void){
    int donuts, events;
    scanf("%i", &donuts);
    scanf("%i", &events);

    char *made;


    made = malloc(events + 1);

    for (int i = 0; i < events; i++){
        int number, number2;
        scanf("%s", made);

        if (*made == 43){
            scanf("%i", &number);
            donuts = donuts + number;
        }
        else{
            scanf("%i", &number2);
            donuts = donuts - number2;
        }
    }
    printf("%d", donuts);

}
