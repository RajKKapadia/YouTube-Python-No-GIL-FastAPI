import threading
import time

balance = 1000

def withdraw(amount):
    global balance

    if balance >= amount:
        time.sleep(0.1)  # simulate delay
        balance -= amount
        print(f"Withdrawn {amount}, balance = {balance}")
    else:
        print("Insufficient balance")

t1 = threading.Thread(target=withdraw, args=(700,))
t2 = threading.Thread(target=withdraw, args=(700,))

t1.start()
t2.start()

t1.join()
t2.join()

print("Final balance:", balance)
