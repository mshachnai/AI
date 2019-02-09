def x(ayy, lmao):
    print(ayy, lmao)

def loopz(func, args):
    for i in range(10):
        func(args[0], args[1])

if __name__ == "__main__":
    loopz(x, ["the", "fuq"]) 
