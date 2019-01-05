# -*- coding: utf-8 -*-
# pylint: disable=E1101
import gc
gc.threshold((gc.mem_alloc() + gc.mem_free()) // 10)

import logging
from cryptoauthlib.device import ATECCX08A

from ateccX08a import tests_info
from ateccX08a import tests_sha
from ateccX08a import tests_random
from ateccX08a import tests_nonce
from ateccX08a import tests_read
from ateccX08a import tests_write
from ateccX08a import tests_lock

log = logging.getLogger("ateccX08a")

TEST_CONFIG_DATA = {
    "ATECC508A": bytes([
        0x01, 0x23, 0x00, 0x00, 0x00, 0x00, 0x50, 0x00, 0x04, 0x05, 0x06, 0x07, 0xEE, 0x00, 0x01, 0x00, # 15
        0xC0, 0x00, 0x55, 0x00, 0x8F, 0x2F, 0xC4, 0x44, 0x87, 0x20, 0xC4, 0xF4, 0x8F, 0x0F, 0x8F, 0x8F, # 31, 5
        0x9F, 0x8F, 0x83, 0x64, 0xC4, 0x44, 0xC4, 0x64, 0x0F, 0x0F, 0x0F, 0x0F, 0x0F, 0x0F, 0x0F, 0x0F, # 47
        0x0F, 0x0F, 0x0F, 0x0F, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, # 63
        0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, # 79
        0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, # 95
        0x33, 0x00, 0x1C, 0x00, 0x13, 0x00, 0x1C, 0x00, 0x3C, 0x00, 0x1C, 0x00, 0x1C, 0x00, 0x33, 0x00, # 111
        0x1C, 0x00, 0x1C, 0x00, 0x3C, 0x00, 0x30, 0x00, 0x3C, 0x00, 0x3C, 0x00, 0x32, 0x00, 0x30, 0x00  # 127
    ]),
    "ATECC608A": bytes([
        0x01, 0x23, 0x00, 0x00, 0x00, 0x00, 0x60, 0x00, 0x04, 0x05, 0x06, 0x07, 0xEE, 0x01, 0x01, 0x00,  # 15
        0xC0, 0x00, 0xA1, 0x00, 0xAF, 0x2F, 0xC4, 0x44, 0x87, 0x20, 0xC4, 0xF4, 0x8F, 0x0F, 0x0F, 0x0F,  # 31, 5
        0x9F, 0x8F, 0x83, 0x64, 0xC4, 0x44, 0xC4, 0x64, 0x0F, 0x0F, 0x0F, 0x0F, 0x0F, 0x0F, 0x0F, 0x0F,  # 47
        0x0F, 0x0F, 0x0F, 0x0F, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF,  # 63
        0x00, 0x00, 0x00, 0x00, 0xFF, 0x84, 0x03, 0xBC, 0x09, 0x69, 0x76, 0x00, 0x00, 0x00, 0x00, 0x00,  # 79
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0x0E, 0x40, 0x00, 0x00, 0x00, 0x00,  # 95
        0x33, 0x00, 0x1C, 0x00, 0x13, 0x00, 0x1C, 0x00, 0x3C, 0x00, 0x3E, 0x00, 0x1C, 0x00, 0x33, 0x00,  # 111
        0x1C, 0x00, 0x1C, 0x00, 0x38, 0x10, 0x30, 0x00, 0x3C, 0x00, 0x3C, 0x00, 0x32, 0x00, 0x30, 0x00   # 127
    ])
}

def test(name="ATECC608A", exclude=['write', 'lock']):
    device = ATECCX08A(device=name)
    log.info("%s", device)

    if 'info' not in exclude:
        tests_info.run(device)
        log.info("INFO SUCCEDED")
    else:
        log.info("INFO SKIPPED")

    if 'sha' not in exclude:
        tests_sha.run(device)
        log.info("SHA SUCCEDED")
    else:
        log.info("SHA SKIPPED")

    if 'random' not in exclude:
        tests_random.run(device)
        log.info("RANDOM SUCCEDED")
    else:
        log.info("RANDOM SKIPPED")

    if 'nonce' not in exclude:
        tests_nonce.run(device)
        log.info("NONCE SUCCEDED")
    else:
        log.info("NONCE SKIPPED")

    if 'read' not in exclude:
        tests_read.run(device)
        log.info("READ SUCCEDED")
    else:
        log.info("READ SKIPPED")

    if 'write' not in exclude:
        tests_write.run(device)
        log.info("WRITE SUCCEDED")
    else:
        log.info("WRITE SKIPPED")

    if 'lock' not in exclude:
        tests_lock.run(device)
        log.info("LOCK SUCCEDED")
    else:
        log.info("LOCK SKIPPED")

# import logging
# logging.basicConfig(level=logging.DEBUG)

# import ateccX08a; ateccX08a.test("ATECC508A")
# import ateccX08a; ateccX08a.test("ATECC608A")
