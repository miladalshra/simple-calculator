num1 = float(input("enter first num: "))
opreter = input("enter operator: ").strip()
num2 = float(input("enter second num: "))

if opreter == "+":
    print(num1 + num2)
elif opreter == "-":
    print(num1 - num2)
elif opreter == "*":
    print(num1 * num2)
elif opreter == "/":
    if num2 != 0:
        print(num1 / num2)
    else:
        print("Cannot divide by zero")
else:
    print("your wrong")






