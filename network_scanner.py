import scapy.all as scapy
import optparse


def get_IP_range():
    parser = optparse.OptionParser()
    parser.add_option("-r", dest="range", help="Specify IP Range to scan")
    (options, arguments) = parser.parse_args()
    if not options.range:
        parser.error("[-] Please specify an IP Range, use --help for more info")
    return options


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list


def print_result(results_list):
    print("IP\t\t\t MAC Address\n---------------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])


IP_range = get_IP_range()
scan_result = scan(IP_range.range)
print_result(scan_result)
