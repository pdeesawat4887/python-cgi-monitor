import firebase

class SweetCandy():
    def __init__(self, swLevel, amount, topping):
        self.swLevel = int(swLevel)
        self.amount = int(amount)
        self.topping = topping
        self.connection = firebase.FirebaseApplication('https://pythonwithfirebase-catma.firebaseio.com')
        # self.info()

    def calculate(self):
        return self.amount*1000

    def info(self):
        print "My Sweet Level: {}\n" \
              "I have {}\n" \
              "{} on my head".format(self.swLevel, self.amount, self.topping)

    def information(self):
        self.connection.put('Candy', 'SMTP', self.swLevel)

    def introduction(self):
        self.connection.put('Candy', 'IMAP', self.swLevel)

    def interview(self):
        self.connection.put('Candy', 'POP3', self.swLevel)

    def choice(self, func):
        func_dict = {'smtp': self.information, 'imap': self.introduction, 'pop3': self.interview}
        func_dict[func]()

    # def main(self):
    #     self.info()

candy = SweetCandy(2000, 5, 'ore')
# {'smtp': candy.information(), 'imap': candy.introduction(), 'pop3': candy.interview()}.get(raw_input())

candy.choice('pop3')