ARP Spoofing Script

This script performs ARP spoofing attacks to intercept network traffic between a target machine and the network gateway. It also includes functionality to enable and disable IP forwarding on the attacker's machine to facilitate packet forwarding.
Features

ARP spoofing to intercept network traffic.
Enable and disable IP forwarding.
Restore ARP tables on exit to prevent network disruption.

Requirements

Python 3
Scapy
Colorama

You can install the required Python packages using pip:

sh

    pip install scapy colorama

Usage

Run the script with the following arguments:

    -t or --target-ip: IP address of the target machine.
    -g or --gateway-ip: IP address of the network gateway.
    -i or --interface: Network interface to use (default is eth0).

Example:

sh

    sudo python3 arp_spoof.py -t 192.168.1.5 -g 192.168.1.1 -i eth0

Arguments

    -t, --target-ip: IP address of the target machine.
    -g, --gateway-ip: IP address of the router.
    -i, --interface: Network interface to use (default: eth0).


Exiting

To exit the script gracefully, press Ctrl+C. This will restore the ARP tables to prevent network disruption and disable IP forwarding.

sh

[-] Quitting using Ctrl+C. Resetting ARP tables, please wait...

[+] ARP tables restored.

[-] Disabling IP forwarding....

[+] IP forwarding disabled.

License

This script is intended for educational purposes only. Use it responsibly and only on networks where you have permission to do so.
