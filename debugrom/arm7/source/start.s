.section .entrypoint

.globl _entrypoint
_entrypoint:
    ldr r1, =0x027ffff0
    ldr r2, =0x12345678
    str r2, [r1]

    mov r0, #0
    mov r1, #0
    mov r2, #0
    mov r3, #0

    bx lr

loop:
    mov r0, #4096
    bl wramSleep
    b loop


wramSleep:
    STMFD   SP!, {R4,R5,LR}
    LDR     R2, =0x380FFD0
    LDR     R4, [R2]
    LDR     R5, [R2,#4]

    LDR     R1, =0xDCFD3801
    STR     R1, [R2]
    LDR     R1, =0x4770
    STR     R1, [R2,#4]

    ORR     R2, R2, #1
    MOV     R0, R0,LSL#4
    MOV     LR, PC
    BX      R2

    STR     R4, [R2]
    STR     R5, [R2,#4]

    LDMFD   SP!, {R4,R5,PC}
