#!/usr/bin/env bash

PI_SERIAL=39d70ef3
PI_MAC=
KICKSTART_IP=10.20.30.243
echo "### Creating folders for ${PI_SERIAL} ###"
mkdir -p /srv/nfs/rpi4-${PI_SERIAL}
mkdir -p /srv/tftpboot/${PI_SERIAL}
echo "### Transferring Image ###"
cp -a /mnt/rpi/* /srv/nfs/rpi4-${PI_SERIAL}/
cp -a /mnt/boot/* /srv/nfs/rpi4-${PI_SERIAL}/boot/

echo "### Adding fstab bind and nfs config ###"
echo "/srv/nfs/rpi4-${PI_SERIAL}/boot /srv/tftpboot/${PI_SERIAL} none defaults,bind 0 0" >> /etc/fstab
echo "/srv/nfs/rpi4-${PI_SERIAL} *(rw,sync,no_subtree_check,no_root_squash)" >> /etc/exports

echo "### Mounting tftp boot for ${PI_SERIAL} ###"
mount /srv/tftpboot/${PI_SERIAL}/


echo "### Configuring image ###"
touch /srv/nfs/rpi4-${PI_SERIAL}/boot/ssh
sed -i /UUID/d /srv/nfs/rpi4-${PI_SERIAL}/etc/fstab
echo "console=serial0,115200 console=tty root=/dev/nfs nfsroot=${KICKSTART_IP}:/srv/nfs/rpi4-${PI_SERIAL},vers=3,proto=tcp rw ip=dhcp rootwait elevator=deadline" > /srv/nfs/rpi4-${PI_SERIAL}/boot/cmdline.txt
echo "dtoverlay=disable-bt" > /srv/nfs/rpi4-${PI_SERIAL}/boot/config.txt
cp -a fixup4.dat /srv/nfs/rpi4-${PI_SERIAL}/boot/
cp -a start4.elf /srv/nfs/rpi4-${PI_SERIAL}/boot/

echo "### Restarting services ###"
systemctl restart dnsmasq
systemctl restart rpcbind
systemctl restart nfs-server

echo "### Done ###"
