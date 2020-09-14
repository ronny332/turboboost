# Turbo Boost enabler/disabler

small and simple utility to switch the current state of the Intel Turbo Boost settings. If settings should be written, `sudo` is handled automatically.

```
-> % tb --help
usage: tb [-h] [-e] {on,off}

toggle Intel Turbo Boost or show current state

positional arguments:
  {on,off}

optional arguments:
  -h, --help     show this help message and exit
  -e, --exit     exit on missing permissions, don't use sudo instead
  -v, --verbose  be verbose

-> % tb -v
Turbo Boost is on, running on 36 core Intel CPU.

-> % tb -v off
Turbo Boost is off, running on 36 core Intel CPU.

-> % tb -v on
Turbo Boost is on, running on 36 core Intel CPU.
```
