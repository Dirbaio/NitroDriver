
wram_sleep:
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
