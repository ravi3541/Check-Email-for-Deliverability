import dns.resolver

def check_mx_records(domain):
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        if mx_records:
            print(f"MX records found for domain {domain}.")
            return True
    except dns.resolver.NoAnswer:
        print(f"No MX records found for domain {domain}.")
    except dns.resolver.NXDOMAIN:
        print(f"Domain {domain} does not exist.")
    return False
