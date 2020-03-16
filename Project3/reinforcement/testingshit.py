class A(object):
    def __init__(self):
        self.x = 0

class B(A):

    def doer(self):
        self.z =self.x
        return self.z

class Person(object):
    def __init__(self):
        self.name = "{} {}".format("First","Last")

class Employee(Person):
    def introduce(self):
        print("Hi! My name is {}".format(self.name))



if __name__=="__main__":
    ins = B()
    print(ins.doer())
    e = Employee()
    e.introduce()
