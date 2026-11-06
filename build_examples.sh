#!/bin/sh

set -xe

riscv32-linux-gnu-gcc -ffreestanding -nostdlib -march=rv32i -mabi=ilp32 -c -o asm/hello.o asm/hello.s
riscv32-linux-gnu-gcc -ffreestanding -nostdlib -T flatbin.ld -o asm/hello.elf asm/hello.o
riscv32-linux-gnu-objcopy -Obinary asm/hello.elf asm/hello.bin

riscv32-linux-gnu-gcc -ffreestanding -nostdlib -march=rv32i -mabi=ilp32 -c -o c/start.o c/start.s
riscv32-linux-gnu-gcc -ffreestanding -nostdlib -march=rv32i -mabi=ilp32 -c -o c/hello.o c/hello.c
riscv32-linux-gnu-gcc -ffreestanding -nostdlib -T flatbin.ld -o c/hello.elf c/start.o c/hello.o
riscv32-linux-gnu-objcopy -Obinary c/hello.elf c/hello.bin
