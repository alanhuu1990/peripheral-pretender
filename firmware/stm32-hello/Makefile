# Copyright (c) 2026 Clifford Swartz. MIT License (see LICENSE).

BOARD ?= stm32l432kc
BUILD = build/$(BOARD)

CC = arm-none-eabi-gcc
OBJCOPY = arm-none-eabi-objcopy

CFLAGS = -mcpu=cortex-m4 -mthumb -std=c11 -Wall -Wextra -Os \
         -ffunction-sections -fdata-sections
LDFLAGS = -T stm32l432kc.ld -nostartfiles -Wl,--gc-sections

OBJS = $(BUILD)/startup.o $(BUILD)/main.o

.PHONY: all clean

all: $(BUILD)/hello.elf

$(BUILD)/hello.elf: $(OBJS)
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $(OBJS)

$(BUILD)/%.o: %.S
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -c -o $@ $<

$(BUILD)/%.o: %.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -c -o $@ $<

clean:
	rm -rf build
