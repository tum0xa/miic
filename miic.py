import ipaddress
import requests
import json
import time

ip_services = {'IPIFY.ORG': 'https://api.ipify.org?format=json',
               'MYIP.COM': 'https://api.myip.com'}


def myip():
    """
    :return: External IP address if its has been gotten successfully, None - if hasn't
    """
    for ip_service in ip_services.values():
        try:
            ip_request = requests.get(ip_service)
        except requests.exceptions.ConnectionError:
            continue
        else:
            request_json = json.loads(ip_request.text)
            ip_address = ipaddress.ip_address(request_json['ip'])
            return ip_address
    return None

def change_dns_record()
    pass

def main():
    # TODO: Add start program arguments
    # -t: time period for update information about external IP
    ip_address = None
    while True:
        prev_ip_address = ip_address
        ip_address = myip()
        if prev_ip_address != ip_address:
            change_dns_record()
        print(ip_address)
        time.sleep(1)


if __name__ == '__main__':
    main()
