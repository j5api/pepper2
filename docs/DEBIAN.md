# Pepper2 on Debian Buster 10

Pepper2 has been tested and found to work on Debian 10.

These instructions detail how to get pepper2 running on debian, from PyPI.

In a recommended deployment, it is probably better to package pepper2 as a debian package, and use the system package manager to install it's dependencies.

## System Dependencies

These can be installed using `apt install`.

- dbus
- libcairo2-dev
- libgirepository1.0-dev
- libsystemd-dev
- python3-pip (To install pepper2 from PyPI)
- python3
- udisks2
- udiskie

## Installing Pepper2

- `sudo pip3 install pepper2`
- Install `uk.org.j5.pepper2.conf` into `/etc/dbus-1/system.d/`
- `sudo systemctl reload dbus`

## Running Pepper2

It is recommended that these are both run as systemd services.

- `sudo udiskie --no-notify --no-password-prompt --no-tray --no-file-manager &` - Start udiskie
- `sudo pepperd` - Start the pepper2 daemon

Warning, this does run pepper2 as root, and thus student code could be run as root. This is not recommended.

In order to run pepper2 as a different user, the dbus configuration must be modified to allow that pepper2 to connect to the system dbus as that user. Udiskie should be run as the same user as pepperd in order to ensure that pepperd can read and write to mounted drives.
