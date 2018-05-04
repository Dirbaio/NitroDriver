# NitroDriver

Open source driver for the IS-NITRO-EMULATOR Nintendo DS Devkit.

For now, it can only load ROMs, but I hope to add debugging and more fancy features in the future.

## Building

You have to build the Debug ROM. You must have devkitPro installed for this

```
cd debugrom
make
```

This should give you a debugrom.bin file, and no errors.

## Running

Commercial ROMs must be encrypted for it to work. (Most commercial ROMs you'll find in the wild are decrypted).

Homebrew ROMs don't care if they're encrypted or not (they don't use the secure area at 0x02000000 - 0x02000800)

You can encrypt ROMs using the excellent devkitPro's ndstool:

```
ndstool -se myrom.nds
```

Once you have an encrypted ROM, run this:

```
python nitro.py myrom.nds
```

## Built-in hex editor

The debug ROM includes a RAM hex editor. Trigger it by holding down START when booting.

- D-pad to change the memory address
- R to change the write size
- A to start a memory write
    - D-pad to edit the value
    - A to write it
    - B to cancel
