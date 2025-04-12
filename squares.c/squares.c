#include <stdio.h>

int main (){
    int m = 0;
    int n = 0;
    int ways = 0;

    scanf("%i", &m);
    scanf("%i", &n);

    for (int i = 0; i < m; i++){
        for (int j = 0; j < n; j++){
            if (m + n == 10){
                ways += 1;
            }
        }
    }

    if (ways == 0 || ways > 1){
        printf("There is %i ways to get the sum 10", ways);
    }
    else{
        printf("There is %i way to get the sum 10", ways);
    }
}
