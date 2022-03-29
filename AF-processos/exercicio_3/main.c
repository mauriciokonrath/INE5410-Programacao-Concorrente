#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <stdio.h>
#include <string.h>

//        (pai)
//          |
//      +---+---+
//      |       |
//     sed    grep

// ~~~ printfs  ~~~
//        sed (ao iniciar): "sed PID %d iniciado\n"
//       grep (ao iniciar): "grep PID %d iniciado\n"
//          pai (ao iniciar): "Processo pai iniciado\n"
// pai (após filho terminar): "grep retornou com código %d,%s encontrou adamantium\n"
//                            , onde %s é
//                              - ""    , se filho saiu com código 0
//                              - " não" , caso contrário

// Obs:
// - processo pai deve esperar pelo filho
// - 1º filho, após o término do 1º deve trocar seu binário para executar
//   sed -i /silver/axamantium/g;s/adamantium/silver/g;s/axamantium/adamantium/g text
//   + dica: leia as dicas do grep
// - 2º filho deve trocar seu binário para executar "grep adamantium text"
//   + dica: use execlp(char*, char*...)
//   + dica: em "grep adamantium text",  argv = {"grep", "adamantium", "text"}

void sed() {
    pid_t sed = fork();
    
    if (sed == 0)
    {
        printf("sed PID %d iniciado\n", getpid());
        fflush(stdout);
        execlp("/bin/sed", "sed", "-i", "-e", "s/silver/axamantium/g;s/adamantium/silver/g;s/axamantium/adamantium/g", "text", NULL);
        exit(0);
    }
}

void grep() {
    pid_t grep = fork();

    if (grep == 0)
    {
        printf("grep PID %d iniciado\n", getpid());
        fflush(stdout);
        execlp("/bin/grep", "grep", "adamantium", "text", NULL);
        exit(0);
    }
}
/*************************************************
     * Dicas:                                        *
     * 1. Leia as intruções antes do main().         *
     * 2. Faça os prints exatamente como solicitado. *
     * 3. Espere o término dos filhos                *
     *************************************************/

int main(int argc, char** argv) {
    printf("Processo pai iniciado\n");
    
    sed();
    wait(NULL);

    grep();
    int grep_exit;
    wait(&grep_exit);
    int grep_status = WEXITSTATUS(grep_exit);

    if (!grep_status)
    {
        printf("grep retornou com código 0, encontrou adamantium\n");        
    } else {
        printf("grep retornou com código %d, não encontrou adamantium\n", grep_status);
    }

    return 0;
}