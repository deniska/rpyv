.global _start
_start:
    la x3, hello_string
    li x4, 40000000
loop:
    lb x1, (x3)
    beq x1, zero, exit
    sb x1, (x4)
    addi x3, x3, 1
    j loop
exit:
    ebreak

hello_string:
    .asciz "Hello world!\n"
