import ipaddress
import requests
import json
import time

ip_services = {'IPIFY.ORG': 'https://api.ipify.org?format=json',
               'MYIP.COM': 'https://api.myip.com'}

DEFAULT_TIME_POLL = 1

LOGIN = 'mylogin'
PASSWORD = 'mypassword'

MYDOMAIN = "mydomain.com"


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


def change_ip_address_for_domain(domain_name, ip_address):
    # TODO: Add wide list domain registrators
    # url = f'https://api.beget.com/api/user/getAccountInfo?login={LOGIN}&passwd={PASSWORD}'
    input_data = {'fqdn': domain_name,
                  'records': {'A': [
                      {
                          "priority": 10,
                          "value": ip_address
                      }
                  ]}
                  }

    data = {'login': LOGIN,
            'passwd': PASSWORD,
            'input_format': 'json',
            'output_format': 'json',
            'input_data': json.dumps(input_data)}
    url = f'https://api.beget.com/api/dns/changeRecords'
    request = requests.get(url, params=data)
    response = json.loads(request.text)
    return bool(response.answer.result)


def main():
    # TODO: Add start program arguments
    # -t: time period for update information about external IP
    # -m: memory mode: previous IP address storing in the stack
    # -f: file mode: previous IP address storing in the file
    # -o: One work cycle without loop
    # -d DomainName

    ip_address = None
    while True:
        prev_ip_address = ip_address
        ip_address = myip()
        if prev_ip_address != ip_address:
            change_ip_address_for_domain(MYDOMAIN, str(ip_address))
        print(ip_address)
        time.sleep(DEFAULT_TIME_POLL)


if __name__ == '__main__':
    change_ip_address_for_domain('tum0xa.ru', str(myip()))
    # main()
