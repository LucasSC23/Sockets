#include <fcntl.h>
#include <unistd.h>

#define BUFFER_SIZE 1024 #definimos el tamño de nuestro buffer para recibir los bytes

int main(int argc, char *argv[]) { 
    if (argc < 2) {
        char error_msg[] = "Error: Debes proporcionar el nombre de un archivo.\n";
        write(2, error_msg, sizeof(error_msg) - 1);
        return 1;
    }

    int fd = open(argv[1], O_RDONLY);
    if (fd == -1) {
        char error_open[] = "Error al abrir el archivo.\n";
        write(2, error_open, sizeof(error_open) - 1);
        return 1;
    }

    char buffer[BUFFER_SIZE];
    ssize_t bytes_leidos;

    while ((bytes_leidos = read(fd, buffer, BUFFER_SIZE)) > 0) {
        write(1, buffer, bytes_leidos);
    }

    if (bytes_leidos == -1) {
        char error_read[] = "Error al leer el archivo.\n";
        write(2, error_read, sizeof(error_read) - 1);
        close(fd);
        return 1;
    }

    close(fd);
    return 0;
}