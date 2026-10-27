/*
 * Copyright (c) 2026 Clifford Swartz. MIT License (see LICENSE).
 */

    .syntax unified
    .cpu cortex-m4
    .thumb

    .section .vectors, "a"
    .global __vectors
__vectors:
    .word 0x2000C000
    .word reset_handler + 1
    .word 0
    .word 0
    .word 0
    .word 0
    .word 0
    .size __vectors, . - __vectors

    .section .text
    .global reset_handler
    .thumb_func
reset_handler:
    ldr r0, =main
    blx r0
    b .

    .global main
