.section .entrypoint

.globl _entrypoint
_entrypoint:
    mov r12, lr

    // Reset FIQ counter
    ldr r1, =0x02600024
    mov r2, #0
    str r2, [r1]

    // Set debug entrypoint
    ldr r1, =0x0380FFDC
    ldr r2, =_debug_entrypoint
    str r2, [r1]

    // Notify we're alive
    ldr r1, =0x02600000
    ldr r2, =0x12345678
    str r2, [r1]

    // Enable FIQ
    mov R0, #0x1f
    msr CPSR_cf, R0

    // Go!
    mov r0, #0
    mov r1, #0
    mov r2, #0
    mov r3, #0
    bx r12


_debug_entrypoint:
    // Increase FIQ counter
    ldr r8, =0x02600024
    ldr r9, [r8]
    add r9, r9, #1
    str r9, [r8]

    // Bye
    bx lr
