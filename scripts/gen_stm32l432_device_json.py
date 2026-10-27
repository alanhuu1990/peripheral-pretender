#!/usr/bin/env python3
# Copyright (c) 2026 Clifford Swartz. MIT License (see LICENSE).
"""Regenerate devices/stm32l432kc.json from CMSIS IRQ names."""

from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path

CMSIS = (
    "https://raw.githubusercontent.com/STMicroelectronics/cmsis_device_l4/"
    "master/Include/stm32l432xx.h"
)
OUT = Path(__file__).resolve().parents[1] / "devices" / "stm32l432kc.json"


def main() -> None:
    text = urllib.request.urlopen(CMSIS, timeout=30).read().decode()
    irqs = []
    for m in re.finditer(r"^\s+([A-Z0-9_]+_IRQn)\s*=\s*(\d+)", text, re.M):
        line = int(m.group(2))
        if line > 82:
            continue
        name = m.group(1).replace("_IRQn", "")
        irqs.append({"line": line, "name": name})
    irqs.sort(key=lambda x: x["line"])
    dev = {
        "schema": "pp-device-stm32/1",
        "generated_by": "scripts/gen_stm32l432_device_json.py",
        "source": {"cmsis": "stm32l432xx.h", "reference": "RM0394"},
        "device": {
            "name": "STM32L432KC",
            "architecture": "CORTEX-M4F",
            "family": "STM32L4",
            "series": "STM32L432",
        },
        "core": {"num_irq": 83, "nvic_prio_bits": 4},
        "memory": [
            {
                "name": "FLASH",
                "base": 0x08000000,
                "size": 262144,
                "type": "flash",
                "exec": True,
            },
            {
                "name": "SRAM1",
                "base": 0x20000000,
                "size": 49152,
                "type": "ram",
            },
            {
                "name": "SRAM2",
                "base": 0x10000000,
                "size": 16384,
                "type": "ram",
            },
        ],
        "interrupts": irqs,
    }
    OUT.write_text(json.dumps(dev, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {OUT} ({len(irqs)} interrupts)")


if __name__ == "__main__":
    main()
