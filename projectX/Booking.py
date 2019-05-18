class Booking:
    date = None
    comment = ""
    from_to = ""
    iban = ""
    value = 0.0
    booking_type = ""
    category = ""

    def __init__(self, date, comment, from_to, iban, value, booking_type):
        self.date = date
        self.comment = comment
        self.from_to = from_to
        self.iban = iban
        self.value = value
        self.booking_type = booking_type

    def __str__(self):
        return ','.join([self.date.strftime(format="%d.%m.%y"),
                         self.comment,
                         self.from_to,
                         self.iban,
                         str(self.value),
                         self.booking_type,
                         self.category])
