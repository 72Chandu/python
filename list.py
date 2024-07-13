list=[1,2,3,4,5,6,7]
for x in list:
    print(x)
list=['a','b','c']
x=len(list)
for i in range(x):
    print(list[i],"is at positive index",i,"and negative index",i-x)

def f1():#--------------------------------------------
    print("this is function")
class student:
    def info(self):
        print("it is method inside class")
f1()
s=student()
s.info()
l=[10,20,10,40,10]#--------------------------------------------
target=int(input("enter the value for search"))
if target in l:
    print(target,"is at first occurance at index",l.index(target))
else:
    print("not found")
print(l.count(10))
l2=[10,20,10,40,10]#--------------------------------------------
target2=int(input("enter the value for search"))
try:
    print(target2,"is at first occurance at index",l.index(target2))
except Error:
    print("not found")
l3=[]#--------------------------------------------
for x in range(120):
    if x%10==0:
        l.append(x)
print(l)
#l.insert(index,element)
l4=[]
l4.append(1)
l4.append(2)
l4.append(3)
l4.append(4)
print(l4)
l4.insert(1,23)
print(l4)
#extende methode
l5=["chan","jejfe","cjjfi"]
l6=["kf","cd","we"]
l5.extend(l6)
print(l5)
print(l6)
#remove methode valueError, no return
l7=[1,2,3,4,5]
x=(int)(input("enter the no to removed"))
if x in l7:
    l7.remove(x)
    print(l7)
else:
    print("element is not found")
#pop methode index erroe, return last ele,removed ele,
l8=[1,29,77,65,44]
print(l8.pop(2))
print(l8)
#reverse
l9=[23,45,67,89]
l9.reverse()
print(l9)
#short no=accending order  string=alphabatically order
l10=["boy","car","dog"]
l10.sort()
print(l10)
l11=[20,4,30,5,50]
l11.sort(reverse=False)
print(l11)
y=l11
print(id(l11))
print(id(y))
y[1]=2345
print(l11)
a=[10,20,30]
b=[40,70,89,90]
#c=a+b
c=a*2
print('a:',a)
print('b:',b)
print('c:',c)
#comparing carcter by caracter 
x=['dog','cat','rat']
y=['dog','cat','rat']
z=['Dog','CAT','RAT']
print(x==y)#t
print(x==z)#f
print(x!=z)#t
c=[1,23,4,5]
print(23 in c)#t
c.clear()#remove all ele
print(c)
#nested
x=[10,20,30,[40,50]]
print(x)
print(x[0])
print(x[3][0])#40
y=[[1,2,3],[4,5,6],[7,8,9]]
print("row wise")
for r in y:
    print(r)# as a list
for i in range(len(y)):#as a determinant 
    for j in range(len(y[i])):
        print(y[i][j],end=' ');
    print()
#comprehensions 
#list=[expression for x in sequence]
p=[]
for x in range(1,11):
    p.append(x*x)
print(p)
p1 = [x * x for x in range(1, 11)]  #same thing will print as above p
print(p1)
#list=[expression for x in sequence if condition]
p3=[x for x in p3 if x%2==0]
print(p3)

p4=[x**2 for x in range(1,21)%2==0]
print(p4)
word= ['edwe','cwdc','defvvcxcsdc']
lu=[w for w in word if len(w)>6]
print(lu)

#dispaly unique vowel present in word
vowel=['a','e','i','o','u']
word=input("enter some word to search")
found[]
for letter in word:
        if letter.lower() in vowel:
            if letter.lower() not in found:
                found.append(letter.lower())
print(found)
print("the number of different vowel presrnt in ",word,"is",len(found))
            

    


