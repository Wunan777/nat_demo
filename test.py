import asyncio


async def factorial(name, number):
    for i in range(10):
        print("{}:{}".format(number, number))
        await asyncio.sleep(number)


async def main():
    # Schedule three calls *concurrently*:
    L = await asyncio.gather(
        factorial("C", 3),
        factorial("B", 2),
        factorial("A", 1),
    )
    print(L)


asyncio.run(main())
