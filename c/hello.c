volatile char* IO_PORT;

void putchar(char ch) {
    *IO_PORT = ch;
}

void puts(char* s) {
    while (*s != 0) {
        putchar(*s);
        s++;
    }
}

void _start() {
    IO_PORT = (char*) 40000000;
    puts("Hello world!\n");
}
