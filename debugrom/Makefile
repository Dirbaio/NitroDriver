#---------------------------------------------------------------------------------
.SUFFIXES:
#---------------------------------------------------------------------------------
ifeq ($(strip $(DEVKITARM)),)
$(error "Please set DEVKITARM in your environment. export DEVKITARM=<path to>devkitARM")
endif

export TARGET	:=	$(shell basename $(CURDIR))
export TOPDIR	:=	$(CURDIR)

include $(DEVKITARM)/ds_rules

.PHONY: checkarm7 checkarm9 clean

#---------------------------------------------------------------------------------
# main targets
#---------------------------------------------------------------------------------
all: checkarm7 checkarm9 $(TARGET).bin

#---------------------------------------------------------------------------------
checkarm7:
	$(MAKE) -C arm7

#---------------------------------------------------------------------------------
checkarm9:
	$(MAKE) -C arm9

#---------------------------------------------------------------------------------
$(TARGET).bin	: arm7/$(TARGET).elf arm9/$(TARGET).elf
	arm-none-eabi-objcopy -O binary arm9/$(TARGET).elf arm9.bin
	arm-none-eabi-objcopy -O binary arm7/$(TARGET).elf arm7.bin
	dd if=/dev/zero of=$(TARGET).bin bs=1 count=131072
	dd if=header.bin of=$(TARGET).bin bs=1 conv=notrunc
	dd if=arm9.bin of=$(TARGET).bin bs=1 conv=notrunc seek=4096
	dd if=arm7.bin of=$(TARGET).bin bs=1 conv=notrunc seek=65536

#---------------------------------------------------------------------------------
arm7/$(TARGET).elf:
	$(MAKE) -C arm7

#---------------------------------------------------------------------------------
arm9/$(TARGET).elf:
	$(MAKE) -C arm9

#---------------------------------------------------------------------------------
clean:
	$(MAKE) -C arm9 clean
	$(MAKE) -C arm7 clean
	rm -f $(TARGET).bin $(TARGET).arm7 $(TARGET).arm9 arm9.bin arm7.bin
