.section .entrypoint

.globl _entrypoint
_entrypoint:

    ldr r0, =0x04000130
    ldrh r0, [r0]
    tst r0, #1<<3  // Start button
    bleq hexedit

    mov r0, #0
    mov r1, #0
    mov r2, #0
    mov r3, #0
    bx lr
