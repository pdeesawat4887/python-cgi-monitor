dict_attribute = {
    'isvc': 'service_id',
    'nsvc': 'service_name',
    'fn': 'file_name',
    'cmd': 'command'
}

jsoncondition = {
    "isvc": "a2999bfffe046ced",
    "nsvc": '1'
}

class Candy:

    def __init__(self, table, text):
        self.table = table
        self.user_input = text

    def check_input_hello(self):
        if self.user_input == 'hello':
            return "Very Good"
        else:
            return "NOT"

    def check_input_ip(self):
        if self.user_input == '192.168.254.31':
            return 'Correct IP'
        else:
            return "Incorrect IP"

    def first_step(self):
        dict_table = {
            'iadr': self.check_input_ip(),
            'txt': self.check_input_hello(),
        }

        try:
            return dict_table[self.table]
        except:
            return None


joe = Candy('iadre', '192.168.254.31')
result = joe.first_step()
print result