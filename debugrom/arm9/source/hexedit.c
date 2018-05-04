#include <nds.h>

#include "hex.h"

void clearMap() {
    u16* map1D = (u16*) 0x06000800;
    for(int i = 0; i < 32*32; i++)
        map1D[i] = 0;
}

void waitVblank() {
    while(REG_VCOUNT < 200);
    while(REG_VCOUNT > 200);
}

int hexedit(void) {
    REG_POWERCNT = 0x03;
    REG_DISPCNT = 0x00010100;
    REG_BG0CNT = 0x0100;
    REG_BG0HOFS = 0;
    REG_BG0VOFS = 0;
    VRAM_A_CR = VRAM_ENABLE | VRAM_A_MAIN_BG;
    BG_PALETTE[0] = 0x3c00;
    BG_PALETTE[1] = 0x7fff;
    BG_PALETTE[16] = 0x7c00;
    BG_PALETTE[17] = 0x03f0;
    BG_PALETTE[32] = 0x7c00;
    BG_PALETTE[33] = 0x0aff;

    u16* tiles = (u16*) 0x06000000;
    memcpy(tiles, hexTiles, hexTilesLen);
    u16 (*map) [32] = (u16(*)[32]) 0x06000800;

    clearMap();

    uint ptr = 0x02000000;
    int digit = 0;

    u16 keys = REG_KEYINPUT;

    int writesize = 4;

	while(1) {
        waitVblank();

        u16 keys2 = REG_KEYINPUT;
        u16 keysDown = keys & ~keys2;
        keys = keys2;

        if (keysDown & KEY_UP) ptr += 1 << (digit * 4);
        if (keysDown & KEY_DOWN) ptr -= 1 << (digit * 4);
        if (keysDown & KEY_LEFT) digit++;
        if (keysDown & KEY_RIGHT) digit--;
        if (keysDown & KEY_SELECT) break;

        if(digit < 0) digit = 0;
        if(digit > 7) digit = 7;

        for(int i = 0; i < 8; i++)
            map[1][7-i] = (digit == i ? 17 : 0) | TILE_PALETTE(2);

        map[1][30] = writesize + 1;
        if (keysDown & KEY_R) {
            if(writesize == 1) writesize = 2;
            else if (writesize == 2) writesize = 4;
            else writesize = 1;
        }

        if (keysDown & KEY_A) {
            clearMap();

            uint32 val;
            if(writesize == 1) val = *(uint8*)ptr;
            else if(writesize == 2) val = *(uint16*)ptr;
            else val = *(uint32*)ptr;

            uint32 val_orig = val;
            int write_digit = 0;

            while(1) {
                waitVblank();

                keys2 = REG_KEYINPUT;
                keysDown = keys & ~keys2;
                keys = keys2;

                if (keysDown & KEY_UP) val += 1 << (write_digit * 4);
                if (keysDown & KEY_DOWN) val -= 1 << (write_digit * 4);
                if (keysDown & KEY_LEFT) write_digit++;
                if (keysDown & KEY_RIGHT) write_digit--;
                if(write_digit < 0) write_digit = 0;
                if(write_digit > writesize * 2 - 1) write_digit = writesize*2 - 1;

                for(int j = 0; j < 8; j++)
                    map[5][10-j] = (((ptr >> (4*j)) & 0xF) + 1) | TILE_PALETTE(1);
                for(int j = 0; j < 8; j++)
                    map[4][21-j] = (write_digit == j ? 17 : 0) | TILE_PALETTE(2);
                for(int j = 0; j < writesize*2; j++)
                    map[5][21-j] = (((val >> (4*j)) & 0xF) + 1) | TILE_PALETTE(0);
                for(int j = 0; j < writesize*2; j++)
                    map[6][21-j] = (((val_orig >> (4*j)) & 0xF) + 1) | TILE_PALETTE(2);

                if (keysDown & KEY_B) {
                    clearMap();
                    break;
                }
                if (keysDown & KEY_A) {
                    if(writesize == 1) *(uint8*)ptr = (uint8) val;
                    if(writesize == 2) *(uint16*)ptr = (uint16) val;
                    if(writesize == 4) *(uint32*)ptr = (uint32) val;
                    clearMap();
                    break;
                }
            }

        }

        for(int i = 0; i < 22; i++) {
            int addr = ptr + i*8;
            for(int j = 0; j < 8; j++)
                map[i+2][7-j] = (((addr >> (4*j)) & 0xF) + 1) | TILE_PALETTE(1);
            for(int j = 0; j < 8; j++) {
                uint8 b = *((uint8*)(addr + j));
                map[i+2][9 + j*3]     = (((b >> 4) & 0xF) + 1) | TILE_PALETTE(j % 2 ? 2 : 0);
                map[i+2][9 + j*3 + 1] = ((b & 0xF) + 1) | TILE_PALETTE(j % 2 ? 2 : 0);
            }
        }
	}

	return 0;
}
