# ucryptoauthlib

Lightweight driver for Microchip Crypto Authentication secure elements written in pure python for micropython.

WARNING: this project is in beta stage and is subject to changes of the
code-base, including project-wide name changes and API changes.

Features
---------------------

- Allows PyBoard to control Microchip Crypto Authentication secure elements
- The API are the same of the [Library](https://github.com/MicrochipTech/cryptoauthlib) wrote by Microchip

Usage
---------------------

- PyBoard basic connection:

</br>
<img src="https://raw.githubusercontent.com/dmazzella/ucryptoauthlib/master/docs/PYBOARD_ATECCX08A_bb.png" width="80%" height="80%" alt="PYBOARD plus ATECCX08A"/>
</br>


- BASIC

```python
MicroPython v1.9.4-754-g5146e7949-dirty on 2018-12-13; PYBv1.1 with STM32F405RG
Type "help()" for more information.
>>> from cryptoauthlib.device import ATECCX08A
>>> device = ATECCX08A()
>>> print(device)
<ATECC608A address=0x60 retries=20>
>>>
```

- TESTS:

```python
MicroPython v1.9.4-754-g5146e7949-dirty on 2018-12-13; PYBv1.1 with STM32F405RG
Type "help()" for more information.
>>> import ateccX08a; ateccX08a.test()
INFO:ateccX08a <ATECC608A address=0x60 retries=20>
INFO:ateccX08a INFO SUCCEDED
INFO:ateccX08a SHA SUCCEDED
INFO:ateccX08a RANDOM SUCCEDED
INFO:ateccX08a NONCE SUCCEDED
INFO:ateccX08a READ SUCCEDED
INFO:ateccX08a WRITE SUCCEDED
INFO:ateccX08a LOCK SKIPPED
INFO:ateccX08a VERIFY SUCCEDED
INFO:ateccX08a SIGN SUCCEDED
>>> 
```

Enable DEBUG:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

External dependencies
---------------------

Only for tests:
'logging' already available into folder 'micropython-lib' of this repository

Install 'cryptoauthlib' into the PyBoard
---------------------

1. Copy 'cryptoauthlib' into PyBoard's filesystem
2. Freeze package using FROZEN_MPY_DIR (1)

   (1) Into the file cryptoauthlib/packet.py:
     - comment optimized method ```at_crc``` decorated with ```@micropython.viper```
     - uncomment generic method ```at_crc```

Software
---------------------

Currently supported commands are:

* INFO
* LOCK
* NONCE
* RANDOM
* READ (1)
* SHA (1)
* WRITE (1)
* VERIFY (1)
* GENKEY
* SIGN

  (1) Not all features are implemented, see follow list for details

Currently implemented methods are:

![API Implemented](http://progressed.io/bar/59)

- [x] atcab_version()
- [x] atcab_get_addr(zone, slot=0, block=0, offset=0)
- [x] atcab_get_zone_size(zone, slot=0)
- [ ] atcab_checkmac(mode, key_id, challenge, response,  other_data)
- [ ] atcab_counter(mode, counter_id)
- [ ] atcab_counter_increment(counter_id)
- [ ] atcab_counter_read(counter_id)
- [ ] atcab_derivekey(mode, key_id, mac)
- [ ] atcab_ecdh_base(mode, key_id, public_key)
- [ ] atcab_ecdh(key_id, public_key)
- [ ] atcab_ecdh_enc(key_id, public_key, read_key, read_key_id)
- [ ] atcab_ecdh_ioenc(key_id, public_key, io_key)
- [ ] atcab_ecdh_tempkey(public_key)
- [ ] atcab_ecdh_tempkey_ioenc(public_key, io_key)
- [ ] atcab_gendig(zone, key_id, other_data)
- [x] atcab_genkey_base(mode, key_id, other_data=None)
- [x] atcab_genkey(key_id)
- [x] atcab_get_pubkey(key_id)
- [ ] atcab_hmac(mode, key_id)
- [x] atcab_info_base(mode=0)
- [x] atcab_info()
- [ ] atcab_kdf(mode, key_id, details, message)
- [x] atcab_lock(mode, crc=0)
- [x] atcab_lock_config_zone()
- [x] atcab_lock_config_zone_crc(crc)
- [x] atcab_lock_data_zone()
- [x] atcab_lock_data_zone_crc(crc)
- [x] atcab_lock_data_slot(slot)
- [ ] atcab_mac(mode, key_id, challenge)
- [x] atcab_nonce_base(mode, zero=0, numbers=None)
- [x] atcab_nonce(numbers=None)
- [x] atcab_nonce_load(target, numbers=None)
- [x] atcab_nonce_rand(numbers=None)
- [x] atcab_challenge(numbers=None)
- [x] atcab_challenge_seed_update(numbers=None)
- [ ] atcab_priv_write(key_id, priv_key, write_key_id, write_key)
- [x] atcab_random()
- [x] atcab_read_zone(zone, slot=0, block=0, offset=0, length=0)
- [x] atcab_read_serial_number()
- [x] atcab_read_bytes_zone(zone, slot=0, block=0, offset=0, length=0)
- [x] atcab_is_slot_locked(slot)
- [x] atcab_is_locked(zone)
- [x] atcab_read_config_zone()
- [ ] atcab_read_enc(key_id, block, data, enc_key, enc_key_id)
- [ ] atcab_cmp_config_zone(config_data)
- [ ] atcab_read_sig(slot)
- [x] atcab_read_pubkey(slot)
- [ ] atcab_secureboot(mode, param2, digest, signature)
- [ ] atcab_secureboot_mac(mode, digest, signature, num_in, io_key)
- [ ] atcab_selftest(mode, param2)
- [x] atcab_sha_base(mode=0, data=b'', key_slot=None)
- [x] atcab_sha(data)
- [ ] atcab_sha_hmac(data, key_slot, target)
- [x] atcab_sign_base(mode, key_id)
- [x] atcab_sign(key_id, message)
- [x] atcab_sign_internal(key_id, is_invalidate=False, is_full_sn=False)
- [x] atcab_updateextra(mode, value)
- [x] atcab_verify(mode, key_id, signature, public_key=None, other_data=None, mac=None)
- [x] atcab_verify_extern(message, signature, public_key)
- [ ] atcab_verify_extern_mac(message, signature, public_key, num_in, io_key, is_verified)
- [x] atcab_verify_stored(message, signature, key_id)
- [ ] atcab_verify_stored_mac(message, signature, key_id, num_in, io_key, is_verified)
- [ ] atcab_verify_validate( key_id, signature, other_data, is_verified)
- [ ] atcab_verify_invalidate( key_id, signature, other_data, is_verified)
- [x] atcab_write(zone, address, value=None, mac=None)
- [x] atcab_write_zone(zone, slot=0, block=0, offset=0, data=None)
- [x] atcab_write_bytes_zone(zone, slot=0, offset=0, data=None)
- [x] atcab_write_pubkey(slot, public_key)
- [x] atcab_write_config_zone(config_data)
- [ ] atcab_write_enc(key_id, block, data, enc_key, enc_key_id)
- [ ] atcab_write_config_counter(counter_id, counter_value)

Hardware
---------------------

Currently supported devices are:

- [ATECC508A](http://www.microchip.com/ATECC508A)
- [ATECC608A](http://www.microchip.com/ATECC608A)
