import random

print("Computer đưa ra số từ 1 => 100. Mời bạn dự đoán. Bạn có 5 lần dự đoán")
count = 1
computer = random.randint(1, 100)
print(computer)
while count < 6:
    player = int(input(f"Mời bạn nhập số dự đoán lần {count}:"))
    count += 1
    if player < computer:
        print("Số bạn đoán nhỏ hơn số computer chọn!")
    elif player > computer:
        print("Số bạn đoán lớn hơn số computer chọn!")
    else:
        print("bạn đoán đúng")
        break
