import threading, time


def my_threaded_func(arg, arg2):
    print("Running thread! Args:")
    time.sleep(10)
    print("Done!")


thread = threading.Thread(target=my_threaded_func, args=("I'ma", "thread"))
thread.start()
print("Spun off thread")
