# -*- coding: utf-8 -*-
from cryptoauthlib import constant as ATCA_CONSTANTS
from cryptoauthlib import status as ATCA_STATUS
from cryptoauthlib.packet import ATCAPacket


class ATECCBasic(object):
    """ ATECCBasic """

    def execute(self, packet):
        """ Abstract execute method """
        raise NotImplementedError()

    def is_error(self, data):
        if data[0] == 0x04:  # error packets are always 4 bytes long
            return ATCA_STATUS.decode_error(data[1])
        else:
            return ATCA_STATUS.ATCA_SUCCESS, "Success"

    def atcab_get_addr(self, zone, slot=0, block=0, offset=0):
        mem_zone = zone & ATCA_CONSTANTS.ATCA_ZONE_MASK
        if mem_zone not in (
            ATCA_CONSTANTS.ATCA_ZONE_CONFIG,
            ATCA_CONSTANTS.ATCA_ZONE_DATA,
            ATCA_CONSTANTS.ATCA_ZONE_OTP
        ):
            raise ValueError("bad params")

        if slot < 0 or slot > 15:
            raise ValueError("bad params")

        addr = 0
        offset = offset & 0x07
        if mem_zone in (
            ATCA_CONSTANTS.ATCA_ZONE_CONFIG,
            ATCA_CONSTANTS.ATCA_ZONE_OTP
        ):
            addr = block << 3
            addr = addr | offset
        elif mem_zone == ATCA_CONSTANTS.ATCA_ZONE_DATA:
            addr = slot << 3
            addr = addr | offset
            addr = addr | block << 8

        return addr

    def atcab_get_zone_size(self, zone, slot=0):
        if zone not in (
            ATCA_CONSTANTS.ATCA_ZONE_CONFIG,
            ATCA_CONSTANTS.ATCA_ZONE_DATA,
            ATCA_CONSTANTS.ATCA_ZONE_OTP
        ):
            raise ValueError("bad params")

        if slot < 0 or slot > 15:
            raise ValueError("bad params")

        if zone == ATCA_CONSTANTS.ATCA_ZONE_CONFIG:
            return 128
        elif zone == ATCA_CONSTANTS.ATCA_ZONE_OTP:
            return 64
        elif zone == ATCA_CONSTANTS.ATCA_ZONE_DATA:
            if slot < 8:
                return 36
            elif slot == 8:
                return 412
            elif slot < 16:
                return 72

    ###########################################################################
    #          CryptoAuthLib Basic API methods for CheckMAC command           #
    ###########################################################################

    ###########################################################################
    #           CryptoAuthLib Basic API methods for Counter command           #
    ###########################################################################

    ###########################################################################
    #          CryptoAuthLib Basic API methods for DeriveKey command          #
    ###########################################################################

    ###########################################################################
    #            CryptoAuthLib Basic API methods for ECDH command             #
    ###########################################################################

    ###########################################################################
    #           CryptoAuthLib Basic API methods for GenDig command            #
    ###########################################################################

    ###########################################################################
    #           CryptoAuthLib Basic API methods for GenKey command            #
    ###########################################################################

    ###########################################################################
    #            CryptoAuthLib Basic API methods for HMAC command             #
    ###########################################################################

    ###########################################################################
    #            CryptoAuthLib Basic API methods for Info command             #
    ###########################################################################

    def atcab_info_base(self, mode=0):
        packet = ATCAPacket(
            opcode=ATCA_CONSTANTS.ATCA_INFO,
            param1=mode
        )
        self.execute(packet)
        return packet

    def atcab_info(self):
        return self.atcab_info_base(ATCA_CONSTANTS.INFO_MODE_REVISION)

    ###########################################################################
    #             CryptoAuthLib Basic API methods for KDF command             #
    ###########################################################################

    ###########################################################################
    #             CryptoAuthLib Basic API methods for Lock command            #
    ###########################################################################

    ###########################################################################
    #             CryptoAuthLib Basic API methods for MAC command             #
    ###########################################################################

    ###########################################################################
    #            CryptoAuthLib Basic API methods for Nonce command            #
    ###########################################################################

    def atcab_nonce_base(self, mode, zero=0, numbers=None):
        nonce_mode = mode & ATCA_CONSTANTS.NONCE_MODE_MASK
        if nonce_mode not in (
            ATCA_CONSTANTS.NONCE_MODE_SEED_UPDATE,
            ATCA_CONSTANTS.NONCE_MODE_NO_SEED_UPDATE,
            ATCA_CONSTANTS.NONCE_MODE_PASSTHROUGH
        ):
            raise ValueError("bad params")

        if not isinstance(numbers, (bytes, bytearray, memoryview)):
            raise ValueError("bad params")

        txsize = 0
        if nonce_mode in (
            ATCA_CONSTANTS.NONCE_MODE_SEED_UPDATE,
            ATCA_CONSTANTS.NONCE_MODE_NO_SEED_UPDATE
        ):
            txsize = ATCA_CONSTANTS.NONCE_COUNT_SHORT
        elif nonce_mode == ATCA_CONSTANTS.NONCE_MODE_PASSTHROUGH:
            nonce_mode_input = mode & ATCA_CONSTANTS.NONCE_MODE_INPUT_LEN_MASK
            if nonce_mode_input == ATCA_CONSTANTS.NONCE_MODE_INPUT_LEN_64:
                txsize = ATCA_CONSTANTS.NONCE_COUNT_LONG_64
            else:
                txsize = ATCA_CONSTANTS.NONCE_COUNT_LONG
        else:
            raise ValueError("bad params")

        n_mv = memoryview(numbers)
        if len(n_mv) < txsize-ATCA_CONSTANTS.ATCA_CMD_SIZE_MIN:
            raise ValueError("bad params")

        packet = ATCAPacket(
            txsize=txsize,
            opcode=ATCA_CONSTANTS.ATCA_NONCE,
            param1=mode,
            param2=zero,
            request_data=n_mv[:txsize-ATCA_CONSTANTS.ATCA_CMD_SIZE_MIN]
        )

        self.execute(packet)
        return packet

    def atcab_nonce(self, numbers=None):
        return self.atcab_nonce_base(
            ATCA_CONSTANTS.NONCE_MODE_PASSTHROUGH,
            numbers=numbers
        )

    def atcab_nonce_load(self, target, numbers=None):
        if not isinstance(numbers, (bytes, bytearray, memoryview)):
            raise ValueError("bad params")

        mode = ATCA_CONSTANTS.NONCE_MODE_PASSTHROUGH
        mode = mode | (ATCA_CONSTANTS.NONCE_MODE_TARGET_MASK & target)

        if len(numbers) == 32:
            mode = mode | ATCA_CONSTANTS.NONCE_MODE_INPUT_LEN_32
        elif len(numbers) == 64:
            mode = mode | ATCA_CONSTANTS.NONCE_MODE_INPUT_LEN_64
        else:
            raise ValueError("bad params")

        return self.atcab_nonce_base(mode, numbers=numbers)

    def atcab_nonce_rand(self, numbers=None):
        return self.atcab_nonce_base(
            ATCA_CONSTANTS.NONCE_MODE_SEED_UPDATE,
            numbers=numbers
        )

    def atcab_challenge(self, numbers=None):
        return self.atcab_nonce_base(
            ATCA_CONSTANTS.NONCE_MODE_PASSTHROUGH,
            numbers=numbers
        )

    def atcab_challenge_seed_update(self, numbers=None):
        return self.atcab_nonce_base(
            ATCA_CONSTANTS.NONCE_MODE_SEED_UPDATE,
            numbers=numbers
        )

    ###########################################################################
    #          CryptoAuthLib Basic API methods for PrivWrite command          #
    ###########################################################################

    ###########################################################################
    #           CryptoAuthLib Basic API methods for Random command            #
    ###########################################################################

    def atcab_random(self):
        packet = ATCAPacket(
            opcode=ATCA_CONSTANTS.ATCA_RANDOM,
            param1=ATCA_CONSTANTS.RANDOM_SEED_UPDATE,
        )
        self.execute(packet)
        return packet

    ###########################################################################
    #             CryptoAuthLib Basic API methods for Read command            #
    ###########################################################################

    def atcab_read_zone(self, zone, slot=0, block=0, offset=0, length=0):
        if length not in (
            ATCA_CONSTANTS.ATCA_WORD_SIZE,
            ATCA_CONSTANTS.ATCA_BLOCK_SIZE
        ):
            raise ValueError("bad params")

        addr = self.atcab_get_addr(zone, slot=slot, block=block, offset=offset)

        if length == ATCA_CONSTANTS.ATCA_BLOCK_SIZE:
            zone = zone | ATCA_CONSTANTS.ATCA_ZONE_READWRITE_32

        packet = ATCAPacket(
            opcode=ATCA_CONSTANTS.ATCA_READ,
            param1=zone,
            param2=addr
        )
        self.execute(packet)
        return packet

    def atcab_read_bytes_zone(self, zone, slot=0, block=0, offset=0, length=0):
        zone_size = self.atcab_get_zone_size(zone, slot=slot)

        if offset + length > zone_size:
            raise ValueError("bad params")

        packets = []

        BS = ATCA_CONSTANTS.ATCA_BLOCK_SIZE
        WS = ATCA_CONSTANTS.ATCA_WORD_SIZE

        r_sz = BS
        d_idx = r_idx = r_of = c_blk = c_of = 0
        c_blk = offset // BS
        while d_idx < length:
            if r_sz == BS and zone_size - c_blk * BS < BS:
                r_sz = WS
                c_of = ((d_idx + offset) // WS) % (BS // WS)

            packet = self.atcab_read_zone(
                zone,
                slot=slot,
                block=c_blk,
                offset=c_of,
                length=r_sz
            )
            packets.append(packet)

            r_of = c_blk * BS + c_of * WS
            r_idx = offset - r_of if r_of < offset else 0
            d_idx += length - d_idx if length - d_idx < r_sz - r_idx else r_sz - r_idx

            if r_sz == BS:
                c_blk += 1
            else:
                c_of += 1

        return packets

    def atcab_is_slot_locked(self, slot):
        # Read the word with the lock bytes
        # ( SlotLock[2], RFU[2] ) ( config block = 2, word offset = 6 )
        return self.atcab_read_zone(
            ATCA_CONSTANTS.ATCA_ZONE_CONFIG,
            slot=0,
            block=2,
            offset=6,
            length=ATCA_CONSTANTS.ATCA_WORD_SIZE
        )

    def atcab_is_locked(self, zone):
        if zone not in (
            ATCA_CONSTANTS.LOCK_ZONE_CONFIG,
            ATCA_CONSTANTS.LOCK_ZONE_DATA
        ):
            raise ValueError("bad params")

        # Read the word with the lock bytes
        # (UserExtra, Selector, LockValue, LockConfig) (config block = 2, word offset = 5)
        return self.atcab_read_zone(
            ATCA_CONSTANTS.ATCA_ZONE_CONFIG,
            slot=0,
            block=2,
            offset=5,
            length=ATCA_CONSTANTS.ATCA_WORD_SIZE
        )

    def atcab_read_config_zone(self):
        return self.atcab_read_bytes_zone(
            ATCA_CONSTANTS.ATCA_ZONE_CONFIG,
            length=ATCA_CONSTANTS.ATCA_ECC_CONFIG_SIZE
        )

    def atcab_read_serial_number(self):
        return self.atcab_read_zone(
            ATCA_CONSTANTS.ATCA_ZONE_CONFIG,
            length=ATCA_CONSTANTS.ATCA_BLOCK_SIZE
        )

    ###########################################################################
    #          CryptoAuthLib Basic API methods for SecureBoot command         #
    ###########################################################################

    ###########################################################################
    #           CryptoAuthLib Basic API methods for SelfTest command          #
    ###########################################################################

    ###########################################################################
    #            CryptoAuthLib Basic API methods for SHA command              #
    ###########################################################################

    def atcab_sha_base(self, mode=0, data=b''):
        if not isinstance(data, (bytes, bytearray, memoryview)):
            raise ValueError("bad params")

        txsize = 0
        cmd_mode = mode & ATCA_CONSTANTS.SHA_MODE_MASK
        if cmd_mode in (
            ATCA_CONSTANTS.SHA_MODE_SHA256_START,
            ATCA_CONSTANTS.SHA_MODE_HMAC_START,
            ATCA_CONSTANTS.SHA_MODE_SHA256_PUBLIC
        ):
            txsize = ATCA_CONSTANTS.ATCA_CMD_SIZE_MIN
        elif cmd_mode in (
            ATCA_CONSTANTS.SHA_MODE_SHA256_UPDATE,
            ATCA_CONSTANTS.SHA_MODE_SHA256_END,
            ATCA_CONSTANTS.SHA_MODE_HMAC_END
        ):
            txsize = ATCA_CONSTANTS.ATCA_CMD_SIZE_MIN + len(data)
        else:
            raise ValueError("bad params")

        packet = ATCAPacket(
            txsize=txsize,
            opcode=ATCA_CONSTANTS.ATCA_SHA,
            param1=mode,
            param2=len(data),
            request_data=data
        )
        self.execute(packet)
        return packet

    def atcab_sha(self, data):
        bs = ATCA_CONSTANTS.ATCA_SHA256_BLOCK_SIZE
        d_mv = memoryview(data)
        packet = self.atcab_sha_base(ATCA_CONSTANTS.SHA_MODE_SHA256_START)
        chunks, rest = divmod(len(d_mv), bs)
        for chunk in range(chunks):
            m = ATCA_CONSTANTS.SHA_MODE_SHA256_UPDATE
            b = d_mv[chunk:chunk + bs]
            packet = self.atcab_sha_base(m, b)
        m = ATCA_CONSTANTS.SHA_MODE_SHA256_END
        b = d_mv[chunks * bs:chunks * bs + rest]
        packet = self.atcab_sha_base(m, b)
        return packet

    ###########################################################################
    #            CryptoAuthLib Basic API methods for Sign command             #
    ###########################################################################

    ###########################################################################
    #         CryptoAuthLib Basic API methods for UpdateExtra command         #
    ###########################################################################

    def atcab_updateextra(self, mode, value):
        packet = ATCAPacket(
            opcode=ATCA_CONSTANTS.ATCA_UPDATE_EXTRA,
            param1=mode,
            param2=value
        )
        self.execute(packet)
        return packet

    ###########################################################################
    #            CryptoAuthLib Basic API methods for Verify command           #
    ###########################################################################

    ###########################################################################
    #            CryptoAuthLib Basic API methods for Write command            #
    ###########################################################################
