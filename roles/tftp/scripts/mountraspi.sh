#!/usr/bin/env bash

kpartx -a -v 2021-05-07-raspios-buster-armhf-lite.img
mount /dev/mapper/loop0p1 /mnt/boot
mount /dev/mapper/loop0p2 /mnt/rpi
