import random

n = 3

x = random.randint(1,n)
y = ""
if (x==n): y = "!!!"
elif (x==1): y = "..."
    
print(f"Rolling a d{n}\nResult is: {x}{y}")