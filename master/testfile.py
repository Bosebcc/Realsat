# coding: utf-8

f = open("testfile.txt","w")


x = "Hellooooooo"

f.write(x)


def classtest():
    def cls1():
        spam = "def1"

    def cls2():
        nonlocal 'spam'
        spam = "def2"
    def cls3():
        global 'spam'
        spam = "def3"

    spam = "def4"
    cls1()
    print("Hello", spam)
    cls2()
    print("Test", spam)
    cls3()
    print("x", spam)

classtest()
print("Global", spam)



f.close()

file = open("testfile.txt","r")
for line in file:
    print line




# credit : http://www.pythonforbeginners.com/files/reading-and-writing-files-in-python
