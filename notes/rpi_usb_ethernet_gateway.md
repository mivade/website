Raspberry Pi as a USB to Ethernet Gateway
=========================================

Introduction
------------

One of the most convenient ways of communicating with experimental
devices (such as oscilloscopes, frequency generators, pulse
generators, etc.) is via ethernet. The advantages of this over other
forms of communication such as GPIB, RS-232 serial ports, etc., is
that, provided the device receives a fixed IP address, it doesn't
matter where it is located and specialty cabling can be kept to a
minimum. Luckily, most of these devices, even if they are not equipped
with ethernet capability, can be made to work over ethernet with some
sort of device server (e.g., there are device servers such as those
made by [Moxa][] which can "convert" RS-232 serial port communications
to ethernet).

A lot of modern devices come equipped with a USB port on the back
which complies with the [USBTMC][] (USB test and measurement class)
specifications. Even fairly inexpensive equipment which lacks an
ethernet port are likely to have a USB port for USBTMC communications
(e.g., the popular and inexpensive [Rigol DS1000D series][rigol scope]
digital oscilloscopes). There exists a USBTMC Linux
[kernel module][usbtmc module] which allows for communication with
USBTMC devices via /dev/usbtmcNNN device files. This module, coupled
with the versatile `socat` command, can thus allow for transparent
communications over ethernet with a USBTMC device as if it were
connected via ethernet itself. The rest of this note describes the
process for using a Raspberry Pi as a USBTMC to ethernet adapter.

[Moxa]: http://www.moxa.com/product/Serial_Device_Servers.htm
[USBTMC]: http://www.usb.org/developers/devclass_docs
[rigol scope]: http://www.rigolna.com/products/digital-oscilloscopes/ds1000d/
[usbtmc module]: http://www.home.agilent.com/upload/cmc_upload/All/usbtmc.html

Compiling the RPi kernel
------------------------

The RPi's default kernel does not include USBTMC support as a module
or built into the kernel. This requires building from scratch, the
full details of which can be found [here][rpi kernel]. The basic idea
is to grab the RPi kernel source on a fast computer and cross compile
it with the USBTMC kernel module [1][] (or build into the kernel if
you prefer).

[rpi kernel]: http://elinux.org/RPi_Kernel_Compilation

Other notes
-----------

It turns out that it is not necessary to use the kernel module to talk
to USBTMC devices. So And So 

### Footnotes ###

[1] In the `make menuconfig` configuration menus, the option can be
    found under `Device Drivers > USB support > USB Test and
    Measurement Class support`.
