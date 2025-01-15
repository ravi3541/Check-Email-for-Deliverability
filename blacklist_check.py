import socket

def check_blacklist(ip):
    print(f'checking ip for blacklist = {ip}')
    # reversed_ip = '.'.join(ip.split('.')[::-1])
    print(f'reversed ip  = {ip}')
    query = f"{ip}.zen.spamhaus.org"
    print(f'query = {query}')
    try:
        socket.gethostbyname(query)
        print(f"IP {ip} is blacklisted.")
        return True
    except socket.gaierror:
        print(f"IP {ip} is not blacklisted.")
        return False
