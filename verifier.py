from proxy_handler import ProxyHandler
from dns_checker import check_mx_records
from smtp_verifier import smtp_verify
from blacklist_check import check_blacklist

def verify_email(email):
    # Step 1: Check DNS Records
    domain = email.split('@')[-1]
    if not check_mx_records(domain):
        print(f"Domain {domain} has no valid MX records.")
        return False

    # Step 2: SMTP Verification with Proxy
    proxy = ProxyHandler.get_proxy()
    print("proxy setup success = ", proxy)
    smtp_status = smtp_verify(email, proxy)

    # Step 3: Blacklist Check
    proxy_ip = proxy['host']
    if check_blacklist(proxy_ip):
        print(f"Proxy IP {proxy_ip} is blacklisted.")
        return False

    # Final Result
    return smtp_status

if __name__ == "__main__":
    email = input("Enter email to verify: ")
    is_valid = verify_email(email)
    print(f"Email {email} is {'valid' if is_valid else 'invalid'}.")
