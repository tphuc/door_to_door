
def f1():
    print('1')
def f2():
    print('2')

choices = {'1': f1, '2':f2}
a = input()
func = choices.get(a, lambda: print("Invalid month"))
func()