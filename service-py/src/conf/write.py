
text_content = 'hello hello hello'

with open("Output.txt", "wb") as text_file:
    text_file.write("{}".format(text_content))