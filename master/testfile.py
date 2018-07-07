# coding: utf-8

fh = open("testfile.txt","w")

fh.write("Hello World")
fh.write("This is our new text file")
fh.write("and this is another line")
fh.write("Why, Because we can")

x = "Hellooooooo"
print x





fh.close()

file = open("testfile.txt","r")
for line in file:
    print line



# credit : http://www.pythonforbeginners.com/files/reading-and-writing-files-in-python
