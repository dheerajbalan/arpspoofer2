
ARP Mirage

Description

ARP Mirage is a Python3-based ARP spoofing tool designed for educational and testing purposes. ARP (Address Resolution Protocol) spoofing is a technique where an attacker sends false ARP messages to a local network, allowing them to intercept or manipulate traffic between devices on the network.
Features

Spoofs ARP tables of both target and gateway to intercept network traffic.
Restores ARP tables to their original state upon termination.
Customizable network interface.
Displays status messages with color coding using the Colorama library.

Requirements

    Python 3.x
    Scapy
    Colorama

Installation

To use this tool, you need to install the required Python libraries. You can install them using pip:

sh

    pip install scapy colorama

Usage

Run the script with the necessary arguments:

please run as sudo or else this program wont work and ignore those warnings if you get while spoofing the target


    sudo python3 arpmirage.py -t <target_ip> -g <gateway_ip> [-i <interface>]

Arguments

    -t or --target-ip: The IP address of the target machine.
    -g or --gateway-ip: The IP address of the gateway (router).
    -i or --interface: The network interface to use (default is eth0).

Example

sh

    sudo python3 arpmirage.py -t 192.168.1.5 -g 192.168.1.1 -i wlan0

Disclaimer

This tool is for educational and authorized testing purposes only. Unauthorized use of this tool on networks that you do not own or have explicit permission to test is illegal and unethical. The author is not responsible for any misuse of this tool.
