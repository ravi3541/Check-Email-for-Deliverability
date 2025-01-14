import smtplib
import requests
import dns.resolver


def get_mx_records(domain):
    """
    Get MX records for a domain.
    """
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_records_list = [record.exchange.to_text() for record in mx_records]
        print("mx_records_list = ", mx_records_list)
        return mx_records_list
    except Exception as e:
        print(f"Error fetching MX records: {e}")
        return None

def is_disposable_email(domain):
    """
    Check if the email domain belongs to a disposable email provider.
    """
    disposable_email_check_url = "https://open.kickbox.com/v1/disposable/" + domain
    try:
        response = requests.get(disposable_email_check_url)
        if response.status_code == 200:
            data = response.json()
            return data.get("disposable", False)
        else:
            print(f"Error checking disposable email: HTTP {response.status_code}")
    except Exception as e:
        print(f"Error checking disposable email: {e}")
    return False

def verify_email(email):
    """
    Verify if an email address exists and is deliverable.
    """
    try:
        # Extract domain from email
        domain = email.split('@')[-1]

        # Check if the domain is disposable
        if is_disposable_email(domain):
            print(f"The email domain {domain} belongs to a disposable email provider.")
            return False

        # Get MX records
        mx_records = get_mx_records(domain)
        if not mx_records:
            print(f"No MX records found for domain: {domain}")
            return False

        # Connect to the first MX server
        mx_server = mx_records[0]
        print(f"Connecting to MX server: {mx_server}")
        smtp = smtplib.SMTP(timeout=10)
        smtp.connect(mx_server)
        smtp.helo(domain)  # Replace with your domain

        # Simulate sending email
        smtp.mail('ravi.mourya@mindbowser.com')  # Replace with your email
        code, message = smtp.rcpt(email)
        print("code = ", code)

        smtp.quit()

        if code == 250:
            print(f"The email {email} is deliverable.")
            return True
        elif code == 550:
            print(f"Error 550: The email address {email} does not exist.")
        elif code == 450:
            print(f"Error 450: The email address {email} is temporarily unavailable.")
        elif code == 421:
            print(f"Error 421: The service is unavailable. Try again later.")
        elif code == 553:
            print(f"Error 553: The email address {email} is invalid or not allowed.")
        else:
            print(f"Unexpected response: {code} {message.decode('utf-8')}")

        return False
    except smtplib.SMTPConnectError as e:
        print(f"SMTP connection error: {e}")
    except smtplib.SMTPServerDisconnected as e:
        print(f"SMTP server disconnected: {e}")
    except smtplib.SMTPResponseException as e:
        print(f"SMTP response error: Code {e.smtp_code}, Message: {e.smtp_error.decode('utf-8')}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return False


# Test the script
# email_to_test = "noveg52859@sfxeur.com"
email_to_test = "support@seeke.us"
verify_email(email_to_test)
