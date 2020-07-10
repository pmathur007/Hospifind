import smtplib, ssl

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "ronnachum13@gmail.com"
password = "Kepler22b711"
message = """\
Subject: Hospifind - High School Students That Can Help Fight Back Against COVID-19

Hi REPRESENTATIVE,

My name is Ron Nachum and I am part of a team of students from Thomas Jefferson High School for Science and Technology who have designed an application called Hospifind to prevent hospital overload in the COVID-19 pandemic. 

The application works by collecting hospital staff-inputted capacity data and uses it to direct patients to hospitals with available space and resources to treat them. Hospifind also includes a hospital data management console that allows government officials to monitor hospital capacity changes over time and respond to sudden spikes in cases in particular locations.

Recently, with the loosening of social distancing guidelines across the country, coronavirus numbers have been sharply increasing. As cases continue to rise, Hospifind will allow the (state name) government to efficiently track coronavirus patient distributions and hospital resources.


Best regards,
Ron Nachum
"""

def send_email(title, name, message, receiver_email):
    message = message.replace("REPRESENTATIVE", title + " " + name.split(" ")[-1])
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

send_email("Representative", "Ron Nachum", message, "ronnachum13@gmail.com")

