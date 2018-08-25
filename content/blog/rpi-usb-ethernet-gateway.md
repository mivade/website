title: Raspberry Pi as a USB to Ethernet Gateway
date: 2014-03-08 15:32
modified: 2014-06-10 10:59
tags: raspberrypi, python
---

Introduction
------------

One of the most convenient ways of communicating with experimental
devices (such as oscilloscopes, frequency generators, pulse
generators, etc.) is via ethernet. The advantages of this over other
forms of communication such as GPIB, RS-232 serial ports, etc., is
that, provided the device receives a fixed IP address or some sort of
dynamic DNS service is used, it doesn't matter where it is located and
specialty cabling can be kept to a minimum. Luckily, most of these
devices, even if they are not equipped with ethernet capability, can
be made to work over ethernet with some sort of device server (e.g.,
there are device servers such as those made by [Moxa][] which can
"convert" RS-232 serial port communications to ethernet).

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
it with the USBTMC kernel module[^1] (or build into the kernel if
you prefer).

[rpi kernel]: http://elinux.org/RPi_Kernel_Compilation

There are a few caveats and pitfalls, so the following provides the
step-by-step approach that worked for me. To get started on a 64-bit
Linux machine, make sure you have the 32-bit libraries
installed. [On Debian and derivatives][Debguide]:

[Debguide]: https://groups.google.com/d/msg/comp.sys.raspberry-pi/ONzkoIV9ab8/E4wejOI51WwJ

```
sudo  dpkg  --add-architecture  i386 # enable multi-arch
sudo  apt-get  update
sudo  apt-get  install  ia32-libs
```

Once this is done, the following steps will get things working:

### Get the RPi kernel source:

```
git init
git clone --depth 1 git://github.com/raspberrypi/linux.git
```

### Get the compiler for cross-compiling:

`git clone git://github.com/raspberrypi/tools.git`

* Compile the kernel

In the kernel source directory, do:

`make mrproper`

Next, copy the default configuration file:

`cp arch/arm/configs/bcmrpi_defconfig .config`

Select the appropriate compiler to use by defining an environment
variable that points to the right place (TODO: put the right thing
here):

`export CCPREFIX=/path/to/your/compiler/binary/prefix-of-binary-`

Pre-configure everything and [accept the defaults][kdefaults]:

`yes "" | make oldconfig`

[kdefaults]: http://serverfault.com/a/116317

Now we can enable building of the usbtmc kernel module. Run `make
menuconfig`.

Navigate to `Device Drivers > USB support > USB Test and Measurement
Class support` and make sure it is marked `M` to build a module. Save
the configuration file, then exit. Now build the kernel:

`make ARCH=arm CROSS_COMPILE=${CCPREFIX} -jN`

where `N` is the number of CPU cores + 1 (e.g., if there are 4 cores,
N = 5). This step will take several minutes on a reasonably fast
computer. Next build the modules:

`make ARCH=arm CROSS_COMPILE=${CCPREFIX} modules`

### Transferring the kernel:

First copy to the RPi:

`scp arch/arm/boot/Image pi@yourpi:kernel_someuniqueid.img`

Then on the RPi, copy this over to `/boot`:

`sudo cp kernel_someuniqueid.img /boot`

Edit the bootloader configuration file to use the new kernel by making
sure the following line appears:

`kernel=kernel_someuniqueid.img`

and comment out any other `kernel=...` lines.

### Transferring the kernel modules:

On the build machine, make a temporary directory to install modules
to:

```
mkdir ~/modules
export MODULES_TEMP=~/modules
```

In the build directory:

`make ARCH=arm CROSS_COMPILE=${CCPREFIX}
INSTALL_MOD_PATH=${MODULES_TEMP} modules_install`

Now in the temporary directory, there should be a `lib` directory. We
don't need the source/headers, so remove them (otherwise you might run
out of space on the RPi SD card!). Transfer these over to the RPi:

`scp -r lib pi@yourpi:`

On the RPi, copy and overwrite the contents of `lib` into `/lib`:

`sudo cp -f lib/* /lib`

*Only do this step while running a different version of the kernel
 than what you compiled!*

### Reboot.

### Load the module:

`sudo modprobe usbtmc`

### Connect the USB device.

There should now be a device named `/dev/usbtmc0`.

Talking to the device
---------------------

A Python script for piping data to and from a USBTMC device can be
found [here](https://gist.github.com/mivade/112ef2087238662441ab). It
should be run through `socat` which does the more difficult work of
properly transferring packets. The `socat` command I use is

```
socat tcp-listen:5025,fork,reuseaddr,crnl,tcpwrap=script\
	EXEC:"python usbtmc_pipe.py",su-d=pi,pty,echo=0
```

Other notes
-----------

It turns out that it is not necessary to use the kernel module to talk
to USBTMC devices. A [pure Python][] implementation of using the
USBTMC protocol also exists. This has the advantage of not requiring a
custom kernel for the RPi, but it adds the slight complexity of
needing to specify vendor and product IDs.

[pure Python]: http://alexforencich.com/wiki/en/python-usbtmc/start

### Footnotes ###

[^1]: In the `make menuconfig` configuration menus, the option can be
	  found under `Device Drivers > USB support > USB Test and
	  Measurement Class support`.
