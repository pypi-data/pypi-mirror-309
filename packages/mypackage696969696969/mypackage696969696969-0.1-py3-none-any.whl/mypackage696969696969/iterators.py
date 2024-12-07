#simple_iterator
class CountFromTen:
    def __init__(self, limit):
        self.current = 10  
        self.limit = limit 

    def __iter__(self):
        return self 

    def __next__(self):
        if self.current > self.limit: 
            raise StopIteration  
        current_value = self.current
        self.current += 1 
        return current_value 

limit = 18
iterator = CountFromTen(limit)

if __name__ == "__main__":  
    for number in iterator: 
        print(number)