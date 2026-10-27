/*
 * Minimal STM32L432KC test firmware for nucleo-l432kc (USART2 VCOM, LED PB3).
 *
 * Copyright (c) 2026 Clifford Swartz. MIT License (see LICENSE).
 */

#include <stdint.h>

#define RCC_BASE        0x40021000U
#define GPIOB_BASE      0x48000400U
#define USART2_BASE     0x40004400U

#define RCC_AHB2ENR     (*(volatile uint32_t *)(RCC_BASE + 0x4CU))
#define RCC_APB1ENR1    (*(volatile uint32_t *)(RCC_BASE + 0x58U))

#define GPIOB_MODER     (*(volatile uint32_t *)(GPIOB_BASE + 0x00U))
#define GPIOB_ODR       (*(volatile uint32_t *)(GPIOB_BASE + 0x14U))

#define USART2_CR1      (*(volatile uint32_t *)(USART2_BASE + 0x00U))
#define USART2_BRR      (*(volatile uint32_t *)(USART2_BASE + 0x0CU))
#define USART2_ISR      (*(volatile uint32_t *)(USART2_BASE + 0x1CU))
#define USART2_TDR      (*(volatile uint32_t *)(USART2_BASE + 0x28U))

static void uart_putc(char c)
{
    while (!(USART2_ISR & (1U << 7))) {
    }
    USART2_TDR = (uint32_t)c;
}

static void uart_puts(const char *s)
{
    while (*s) {
        uart_putc(*s++);
    }
}

int main(void)
{
    /* MSI on by default; enable GPIOB and USART2 clocks. */
    RCC_AHB2ENR |= (1U << 1);
    RCC_APB1ENR1 |= (1U << 17);

    /* PB3 output (user LED LD3). */
    GPIOB_MODER = (GPIOB_MODER & ~(3U << 6)) | (1U << 6);

    /* USART2: 115200 8N1 from 4 MHz MSI (BRR = 4e6 / 115200). */
    USART2_CR1 = 0;
    USART2_BRR = 35;
    USART2_CR1 = (1U << 0) | (1U << 3); /* UE | TE */

    uart_puts("PP:STM32 hello\r\n");

    for (volatile int i = 0; i < 3; i++) {
        GPIOB_ODR ^= (1U << 3);
        for (volatile int d = 0; d < 200000; d++) {
        }
    }

    uart_puts("PP:EXIT 0\r\n");
    return 0;
}
