import certifi
import requests
import sys

def add_custom_ca(host):
    try:
        print('Checking connection to', host, '...')
        url = ''.join(['https://',host])
        test = requests.get(url)
        print('Connection to ', host, ' OK.')
    except requests.exceptions.SSLError as err:
        print('SSL Error. Adding custom certs to Certifi store...')
        cafile = certifi.where()
        with open('/etc/ssl/certs/ca-certificates.crt', 'rb') as infile:
            customca = infile.read()
        with open(cafile, 'ab') as outfile:
            outfile.write(customca)
        print('That might have worked.')


if __name__ == '__main__':
    host = sys.argv[1]
    add_custom_ca(host)
