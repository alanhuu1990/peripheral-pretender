# Onboarding an STM32 Nucleo board

STM32 boards do not use the ATDF generator. Bring-up follows the upstream
STM32L4x5 QEMU models in `pp-qemu`, extended with Peripheral Pretender
SoC variants, board machines, and optional `pp-trace` wiring.

## Prerequisites

- `arm-none-eabi-gcc` (same toolchain as `firmware/hello`)
- Built `pp-qemu` (`qemu/setup.sh`) with the STM32 patches applied
- RM0394 (L4x1/L4x2) or RM0351 (L4x5) for memory map and NVIC
- STM32Cube firmware or a minimal register-level image ending in `PP:EXIT`

## Steps

1. **SoC** — Add or extend an `stm32l4x2-soc` / `stm32l4x1-soc` class with
   correct flash, SRAM, GPIO port set, USART instances, and EXTI/NVIC tables
   from the reference manual (do not copy L475 tables blindly).
2. **Board machine** — Map ST-LINK VCOM USART pins to `serial_hd(0)`, on-board
   LED and buttons to GPIO, and set `.interfaces = arm_machine_interfaces`
   on the machine type so `qemu-system-arm` lists it.
3. **Firmware** — Place a project under `firmware/stm32-hello/` (or Cube export)
   and verify with `python -m tools.pp run … -M <machine>`.
4. **Metadata** — Add `devices/<part>.json` (IRQ names for the web timeline)
   and `tools/pp_web/boards/<id>/board.json` when the web bench should show the kit.
5. **Regression** — Keep upstream `stm32l4x5_*` qtests green; add board-specific
   qtests cloned from the L4x5 GPIO/USART templates.

## Reference implementation

- Machine `nucleo-l432kc`, SoC `stm32l4x2kc-soc`, firmware
  `firmware/stm32-hello/build/stm32l432kc/hello.elf`
- Machine `nucleo-l431rb`, SoC `stm32l4x1rb-soc` (extra GPIO and USART3)
