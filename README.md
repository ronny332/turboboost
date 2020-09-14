# Turbo Boost enabler/disabler

small and simple utility to switch the current state of the Intel Turbo Boost settings. If settings should be written, `sudo` is handled automatically.

```
-> % tb --help
usage: tb [-h] [-e] {on,off}

toggle Intel Turbo Boost or show current state

positional arguments:
  {on,off}

optional arguments:
  -h, --help  show this help message and exit
  -e, --exit  exit on missing permissions

-> % tb
Turbo Boost is on

-> % tb off
Turbo Boost is off

-> % tb on
Turbo Boost is on
```
