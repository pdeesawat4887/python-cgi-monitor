class SweetCandy():
    def __init__(self, swLevel, amount, topping):
        self.swLevel = int(swLevel)
        self.amount = int(amount)
        self.topping = topping

    def calculate(self):
        return self.amount*1000

    def info(self):
        print "My Sweet Level: {}\n" \
              "I have {}\n" \
              "{} on my head".format(self.swLevel, self.amount, self.topping)