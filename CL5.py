num1 = float(input("enter first num: "))
o = input("enter operator: ").strip()
num2 = float(input("enter second num: "))

if o == "+":
    print(num1, o, num2, "=", num1 + num2)
elif o == "-":
    print(num1, o, num2, "=", num1 - num2)
elif o == "*":
    print(num1, o, num2, "=", num1 * num2)
elif o == "/":
    if num2 != 0:
        print(num1, o, num2, "=", num1 / num2)
    else:
        print("Cannot divide by zero")
else:
    print("your wrong")