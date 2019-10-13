class test:
    def __init__(self):
        self.count = 1
        self.cost = None
    def test(self,cost=lambda x:1):
        self.cost = cost
        print cost
