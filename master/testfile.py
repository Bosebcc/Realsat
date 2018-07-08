# coding: utf-8

f = open("testfile.txt","w")

y = int(5)
z = int(6)
a = y*z
x = "Hellooooooo"
print a

f.write(x)

f.write(a)

f.close()

file = open("testfile.txt","r")
for line in file:
    print line




# credit : http://www.pythonforbeginners.com/files/reading-and-writing-files-in-python
