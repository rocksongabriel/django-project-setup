from app import console


while True:
    try:
        install_drf = int(input("Will you use django REST framework in your project? ( 1 - yes, 0 - no): "))
        if install_drf in [0, 1]:
            break
        else:
            raise ValueError
    except ValueError:
        console.log("Enter integer 1 or 0 only")
        continue

if install_drf == 1:
    print("1 pressed")
else:
    print("0 pressed")