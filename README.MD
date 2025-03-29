''' this is multiline comment '''

a=input("enter the input") -> in this case the input is string
a=int(input("enter the input"))

# printing techniques
print("..",a,"+",b,"=",c)
print(".. {}+{}={}".formate(a,b,c))
print(".. {0}+{1}={2}".formate(a,b,c))
print(".. {2}+{0}={1}".formate(b,c,a))
print(f".. {a}+{b}={c}") -> smart printing
print("hello","all",sep=",") -> hello, all

print("s"*5) -> s s s s s
# operator
+,-,*,%,/(float division),//(integer division),**(a^b)
logical operator: and , or, not
Relational operator: >,>=,<,<=,!=,==,    -gt,-ge,-Lt,-ne,-eq
Ternary operator: x= "True " if (condn) else "false"

char(65) -> convert in letter
ord('A') -> print ASSCI value
char((ord('A')) | 32) -> convert in small letter
char((ord('a')) & 223) -> convert in capital letter

# misc concepts
value ranging from -5 to 256(inclusive) will generate the same id for same value, 
ex: a=256 b=256 both a and b have same id

ex: a=257 b=257 both a and b have diffrent id

# data type
data type identify by value get to the variable 
a=100->integer a="hello"->string a=12.4->float a=True ->bool

# loop
range(initalize,end,step) end is mendentaroy end is excluded
for i in range(0,10,1):            
    print(i,end=",")
else:
    print("\nrun when loop break");  #ensuring the loop run completely or not

    while i<1:
          print(f"i:.2f")
          i+=0.1

# function
def fun():
      print("welcome")
fun()

def fun(msg,times=2):
      print(msg*times)
fun("chandu")
fun("chandu",5)

function takes input arguments and return multiple values in collection class object as output arguments
def fun4(n1,n2):
    total=n1+n2
    diff=n1-n2
    prod=n1*n2
    quotient=n1/n2
    remainder=n1%n2
    return total,diff,prod,quotient,remainder
tt,dd,pp,qq,rr=fun4(100,40)
print(f"Total={tt},Difference={dd},Product={pp},Quotient={qq},Remainder={rr}")
res=fun4(100,40)
print(f"Total={res[0]},Difference={res[1]},Product={res[2]},Quotient={res[3]},Remainder={res[4]}")
print(res)

Total=140,Difference=60,Product=4000,Quotient=2.5,Remainder=20
Total=140,Difference=60,Product=4000,Quotient=2.5,Remainder=20
(140, 60, 4000, 2.5, 20)


function with variable number of input arguments
*arg defines forefully that arg is a tuple object
**arg defines forefully that arg is a dictionary object

def fun(*arg,**karg):  
    print(arg)
    print(karg,len(karg))
fun(collegeName="TIU",place="Kolkata")
fun(empname="chandu",empjob="CEO",emploc="Bihar")
fun("Joydeep","Tester","Pune",55000,"Male",True)

()
{'collegeName': 'TIU', 'place': 'Kolkata'}
()
{'empname': 'chandu', 'empjob': 'CEO', 'emploc': 'Bihar'}
('Joydeep', 'Tester', 'Pune', 55000, 'Male', True)
{}

# Lambda or Anonymous function
myaddition=lambda num1,num2:num1+num2
print(myaddition(10,30)) -> 40

# math
import math
math -> .sin(0),.cos(0),.tan(0),.sinh(0),.cosh(0),.tanh(0),asinh(0),acosh(0),.atanh(0), .pi,.e,.tau,.factorial(4),.gcd(100,750),.pow(10,3),.ceil(10.1),floor(10.1)

# String
 0  1  2  3  4  5  6  7  8  9  -> indexing from left to right
 u  n  i  v  e  r  s  i  t  y -> mystr
-10 -9 -8 -7 -6 -5 -4 -3 -2 -1 -> indexing from right to left

mystr[6]->s,mystr[-4]->s
mystr[1:6]->niver,mystr[-9:-4]->niver,mystr[1:-4]->niver,mystr[-9:6]->niver    #slicing
mystr[:6]->univer,mystr[:-4]->univer
mystr[0::2]->uiest,mystr[1::2]->nvriy,mystr[::-1]->ytisrevinu

1. Strings are Immutable : it cannot be changed (modified).
s = "hello"
s[0] = 'H'  # ❌ TypeError: 'str' object does not support item assignment
2. Strings are Ordered (Indexed)
3. Strings are Iterable
4. Strings Support Slicing
5. Strings are Case-Sensitive
6. Strings Support Concatenation(+) & Repetition(*)
7. Strings Have Built-in Methods
a) Case Modification
s = "helLo WoRld"
print(s.upper())     # 'HELLO WORLD'
print(s.lower())     # 'hello world'
print(s.title())     # 'Hello World'
print(s.capitalize())# 'Hello world'
print(s.swapcase())  # 'HELLO WORLD'
print(s.casefold())  # 'hello world'
b) Checking String Content
s="abcd"
print(s.isalpha(),s.isalnum(),s.isdigit(),s.isnumeric()) #True True False False

mystr="1234"
print(s.isalpha(),s.isalnum(),s.isdigit(),s.isnumeric()) #False True True True

s="1234abcd"
print(s.isalpha(),s.isalnum(),s.isdigit(),s.isnumeric()) #False True False False

s="abcd@1234"
print(s.isalpha(),s.isalnum(),s.isdigit(),s.isnumeric()) #False False False False

s = "charity begins at home"
print(s.startswith("charity")) #True
print(s.startswith("begi"),s.startswith("begi",8),s.startswith("begi",8,20)) #False True True
print(s.endswith("home"),s.endswith("at",0,17),s.endswith("begi",15,17))#True True False

c) Finding & Replacing
s = "hello world"
print(s.find("world"))   # 6
print(s.index("world"))  # 6
print(s.replace("world", "Python"))  # 'hello Python'
d) Splitting & Joining
s = "apple,banana,grape"
print(s.split(","))  # ['apple', 'banana', 'grape'] -> return arra

words = ["Hello", "World"]
print(" ".join(words))  # 'Hello World'

8. Strings Support Escape Sequences: Escape sequences allow special characters in strings.
s = "Hello\nWorld"   # New line
s = "Hello\tWorld"   # Tab
s = "She said, \"Hello\""  # Double quotes inside string
s = 'It\'s a beautiful day' # Apostrophe inside single-quoted string

9. Raw Strings (r'')
Raw strings ignore escape sequences.
s = r"C:\Users\name\new_folder"
print(s)  # Output: C:\Users\name\new_folder

10. String Encoding: Strings in Python are Unicode by default.You can encode/decode strings.
s = "hello"
encoded = s.encode('utf-8')  # Converts to bytes
print(encoded)  # b'hello'
decoded = encoded.decode('utf-8')
print(decoded)  # 'hello'

11. Checking Membership (in, not in)
You can check if a substring exists in a string.
s = "Hello World"
print("World" in s)   # True
print("Python" not in s)  # True

12. Strings Have a Length: get the length of a string using len().

13. Counting Occurrences of a Substring (count())
The .count() method is used to count how many times a substring appears in a string.
s = "banana"
print(s.count("a"))   # Output: 3
print(s.count("na"))  # Output: 2
print(s.count("z"))   # Output: 0
print(s.count("a", 2, 5))  # Output: 1 (only counts 'a' in "nan")

14. Removing Whitespace (strip(), lstrip(), rstrip())
The .strip() method removes leading (left) and trailing (right) whitespace (or specified characters).

s = "   hello   "
print(s.strip())   # 'hello' (removes spaces from both sides)

s = "---hello---"
print(s.strip("-"))   # 'hello' (removes '-')
print(s.lstrip("-"))  # 'hello---'
print(s.rstrip("-"))  # '---hello'