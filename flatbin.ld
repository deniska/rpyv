SECTIONS {
    . = 0x0;
    .text : {
        *(.text)
    }
    . = ALIGN(4);
    .data : {
        *(.rodata)
        *(.rodata.*)
        *(.data)
    }
    . = ALIGN(4);
    .bss : {
        *(.bss)
    }
    . +=  1048576;
    . = ALIGN(4);
    _stack_top = .;
}
