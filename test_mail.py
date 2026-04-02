import smtplib
from email.mime.text import MIMEText

sender_email = "vinothini14005@gmail.com"
app_password = "kxruplrnhdymuuce"

receiver_email = "vinothini14005@gmail.com"   # same mail use pannunga

msg = MIMEText("Test mail from Python 🚀")
msg['Subject'] = "Test"
msg['From'] = sender_email
msg['To'] = receiver_email

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, app_password)
    server.send_message(msg)
    server.quit()

    print("MAIL SENT SUCCESS ✅")

except Exception as e:
    print("ERROR ❌:", e)