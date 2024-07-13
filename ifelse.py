a=int(input("enter the age"))
print("your age is :",a)
print(a>18)
print(a<=18)
print(a==18)
if(a>18):#there must be space (indentation) while writing any statement
    print("you can drive")
    print("yes")
else:
    print("you can not drive")
    print("no")
print("oooo")#this become out of else statement
#else if 
num=int(input("enter the value"))
if(num<0):
    print("number is negative")
elif(num==0):
    print("number is zero")
elif(num==999):
    print("spacial")
else:
    print("number is positive")
#nested
num1=18
if(num<0):
    print("nuber is negative")
elif(num>10):
    if(num<=10):
        print(" nuber is b/w 1-10")
    elif(num>10 and num<=20):
        print("number is b/w 11-20")
    else:
        print("num greater than 20")
         
         
         
         
         
         
         
         
         
         
         