# Copyright (c) 2026 Clifford Swartz. MIT License (see LICENSE).
"""STM32L432 NUCLEO twin smoke test (requires pp-qemu with nucleo-l432kc)."""

from pathlib import Path

import pytest

from tools.pp import RunOptions, run
from tools.pp.qemu import QemuNotFound, find_qemu, list_machines

pytestmark = pytest.mark.qemu

ROOT = Path(__file__).resolve().parents[1]
MACHINE = "nucleo-l432kc"
ELF = ROOT / "firmware" / "stm32-hello" / "build" / "stm32l432kc" / "hello.elf"


@pytest.fixture(scope="module")
def qemu_arm():
    try:
        qemu = find_qemu(target="arm")
    except QemuNotFound as exc:
        pytest.skip(str(exc))
    names = {m.name for m in list_machines(qemu)}
    if MACHINE not in names:
        pytest.skip(f"{qemu} has no {MACHINE} machine")
    return qemu


def test_stm32_hello_reaches_pp_exit(qemu_arm):
    if not ELF.is_file():
        pytest.skip(f"{ELF} not built (make -C firmware/stm32-hello)")
    result = run(RunOptions(elf=ELF, machine=MACHINE, qemu=qemu_arm, timeout_s=20))
    assert result.firmware_exit == 0, result.detail
    assert "PP:EXIT 0" in result.uart
