help:
	@echo "Welcome to Espressif IDF build system. Some useful make targets:"
	@echo ""
	@echo "make menuconfig - Configure IDF project"
	@echo "make defconfig - Set defaults for all new configuration options"
	@echo ""
	@echo "make all - Build app, bootloader, partition table"
	@echo "make flash - Flash app, bootloader, partition table to a chip"
	@echo "make clean-all - Remove all build output"
	@echo "make size - Display the static memory footprint of the app"
	@echo "make size-components, size-files - Finer-grained memory footprints"
	@echo "make size-symbols - Per symbol memory footprint. Requires COMPONENT=<component>"
	@echo "make erase_flash - Erase entire flash contents"
	@echo "make erase_otadata - Erase ota_data partition; First bootable partition (factory or OTAx) will be used on next boot."
	@echo "                     This assumes this project's partition table is the one flashed on the device."
	@echo "make monitor - Run idf_monitor tool to monitor serial output from app"
	@echo "make simple_monitor - Monitor serial output on terminal console"
	@echo "make list-components - List all components in the project"
	@echo ""
	@echo "make app - Build just the app"
	@echo "make app-flash - Flash just the app"
	@echo "make app-clean - Clean just the app"
	@echo "make print_flash_cmd - Print the arguments for esptool when flash"
	@echo "make check_python_dependencies - Check that the required python packages are installed"
	@echo ""
	@echo "See also 'make bootloader', 'make bootloader-flash', 'make bootloader-clean', "
	@echo "'make partition_table', etc, etc."

clean-all:
	make -f esp_idf_project.mk clean

app: $(TARGETS)

bootloader: $(BOOTLOADER)

bootloader-clean:
	@echo 'rm -rf $(dir $(BOOTLOADER))'
	rm -rf $(dir $(BOOTLOADER))

app-clean:
	rm -rf $(TARGET) $(TARGET_BIN)

FORWARD_TARS += menuconfig
FORWARD_TARS += defconfig
FORWARD_TARS += erase_flash
FORWARD_TARS += erase_otadata
FORWARD_TARS += monitor
FORWARD_TARS += simple_monitor

$(FORWARD_TARS):
	make -f esp_idf_project.mk $@

FORWARD_TOOL += flash
FORWARD_TOOL += size
FORWARD_TOOL += size-components
FORWARD_TOOL += size-symbols
FORWARD_TOOL += list-components
FORWARD_TOOL += app-flash
FORWARD_TOOL += print_flash_cmd
FORWARD_TOOL += check_python_dependencies
FORWARD_TOOL += bootloader-flash

$(FORWARD_TOOL): $(TARGET_BIN)
	make -f esp_idf_project.mk $@
