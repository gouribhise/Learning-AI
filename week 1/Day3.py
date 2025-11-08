#write a function add(a,b) that returns their sum

def add(a,b):
    return a+b

ans=add(10,2)
print("Addition is: ",ans)

#Write a function is_even(num) that checks if a number is even

def is_even(num):
    if num%2==0:
        return "Even"
    else:
        return "Odd"
ans=is_even(19)
print(f"19 is a {ans} number")
ans1=is_even(18)
print(f"18 is a {ans1} number")