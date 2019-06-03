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
        self.to_number = '{}{}'.format(self.number, carriers['att'])
        self.auth = ('{}'.format(self.email), '{}'.format(self.password))
        self.server = smtplib.SMTP("smtp.gmail.com", 587)
        self.server.starttls()
        self.server.login(self.auth[0], self.auth[1])

    def send(self, message):
        # Replace the number with your own, or consider using an argument\dict for multiple people.

        # Establish a secure session with gmail's outgoing SMTP server using your gmail account
        self.server.login(self.auth[0], self.auth[1])

        # Send text message through SMS gateway of destination number
        self.server.sendmail(self.auth, self.to_number, message)
