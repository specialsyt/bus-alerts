import smtplib
carriers = {
    'att':    '@mms.att.net',
    'tmobile':' @tmomail.net',
    'verizon':  '@vtext.com',
    'sprint':   '@page.nextel.com'
}


class SMS:

    def __init__(self, number, email, password):
        self.number = number
        self.email = email
        self.password = password

    def send(self, message):
        # Replace the number with your own, or consider using an argument\dict for multiple people.
        to_number = '{}{}'.format(self.number, carriers['att'])
        auth = ('{}'.format(self.email), '{}'.format(self.password))

        # Establish a secure session with gmail's outgoing SMTP server using your gmail account
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(auth[0], auth[1])

        # Send text message through SMS gateway of destination number
        server.sendmail(auth[0], to_number, message)
