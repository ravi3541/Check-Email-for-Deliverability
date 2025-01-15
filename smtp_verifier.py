import smtplib
import socks

def smtp_verify(email, proxy):
    domain = email.split('@')[-1]
    mx_server = f"{domain}"  # Basic heuristic; customize as needed
    print("mx_server = ", mx_server)

    try:
        socks.setdefaultproxy(socks.SOCKS5, proxy['host'], proxy['port'])
        print("default proxy setup success")
        socks.wrapmodule(smtplib)
        print("proxy wrap module success")

        server = smtplib.SMTP(mx_server, 25)
        print("connected to smtp ")
        server.set_debuglevel(0)
        server.helo(domain)
        print("HELO done")
        server.mail("ravi@gamil.com")
        code, message = server.rcpt(email)
        print(f'code = {code}   |    message = {message}')
        server.quit()

        if code == 250:
            print(f"Email {email} is deliverable.")
            return True
        else:
            print(f"SMTP rejected {email}: {code} - {message.decode()}")
            return False
    except Exception as e:
        print(f"SMTP verification error for {email}: {e}")
        return False
