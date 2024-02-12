import threading
import time


def task1():
    for _ in range(5):
        print("Task 1 is executing...")
        # time.sleep(1)


def task2():
    for _ in range(5):
        print("Task 2 is executing...")
        # time.sleep(1)


if __name__ == "__main__":
    thread1 = threading.Thread(target=task1)
    thread2 = threading.Thread(target=task2)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print("Both tasks are completed.")
