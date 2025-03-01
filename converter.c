#include <stdio.h>
#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>

void help(char* curbin) {
    fprintf(stderr, "%s x86_bin arm64_output\n", curbin);
}

int main(int argc, char** argv) {
    printf("this will sigbus but the bin might be valid\n");
    if (argc < 3) {
        help(argv[0]);
        return 1;
    }

    int x86fd = open(argv[1], O_RDONLY);
    if (x86fd < 0) {
        perror("x86fd");
        return 2;
    }

    int armfd = open(argv[2], O_CREAT | O_WRONLY, 0755);
    if (armfd < 0) {
        perror("armfd");
        return 2;
    }

    char* x86fdstr = calloc(2048, 1);
    char* armfdstr = calloc(2048, 1);

    sprintf(x86fdstr, "%d", x86fd);
    sprintf(armfdstr, "%d", armfd);
    
    char* args[] = {
        "oahd-helper",
        x86fdstr,
        armfdstr,
        NULL,
    };

    execv("/usr/libexec/rosetta/oahd-helper", args);
    perror("execve");
}