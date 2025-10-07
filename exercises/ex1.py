cars = int(input("how many cars?: "))
parking_lots = int(input("how many parking lots?: "))

if parking_lots >= cars:
    print("you can park!")
elif parking_lots < cars:
    print("you can not park here!")
