#!/bin/bash

#################################################
#Installs the main library modules required on the Pi to run the RFID reader
#################################################

#Update the Raspberry Pi
apt install update && apt install -y upgrade

#Enable the SPI interface
if [ !cat /boot/config.txt | grep -i "dtparam=spi=on" ]
then
  echo "dtparam=spi=on" >> /boot/config.txt
  ##Prompt to restart after enabling SPI
  echo "A restart is required after enabling the SPI interface."
  echo "Would you like to restart now? (Y/N)" answer
  if [ $answer == 'Y' ] || [ $answer == 'y' ]
  then
    echo "Raspberry Pi will reboot now."
    reboot
  else
    echo "Action cancelled. Please restart later to complete the initialization."
  fi
# Confirm that SPI is enabled
else
  echo "SPI interface enabled in the configuration file."
  if [ lsmod | grep -i "spi_bcm" ]
  then
    # Install the Python SPI wrapper
    apt install -y python-dev python3-dev
    apt install -y python-spidev python3-spidev
    cd ~ && git clone https://github.com/Gadgetoid/py-spidev.git | cd py-spidev
    python setup.py install && python3 setup.py install
    cd ~
