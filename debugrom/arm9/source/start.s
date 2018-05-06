.section .entrypoint

.globl _entrypoint
_entrypoint:
    mov r12, lr

    // Reset FIQ counter
    ldr r1, =0x02600020
    mov r2, #0
    str r2, [r1]

    // Set debug entrypoint
    ldr r1, =0x027FFD9C
    ldr r2, =_debug_entrypoint
    str r2, [r1]

    // Enable FIQ
    mov R0, #0x1f
    msr CPSR_cf, R0

    // Hex edit if START held down
    ldr r0, =0x04000130
    ldrh r0, [r0]
    tst r0, #1<<3  // Start button
    bleq hexedit

    // Go!
    mov r0, #0
    mov r1, #0
    mov r2, #0
    mov r3, #0
    bx r12

_debug_entrypoint:
    // Increase FIQ counter
    ldr r8, =0x02600020
    ldr r9, [r8]
    add r9, r9, #1
    str r9, [r8]

    // Bye
    bx lr
