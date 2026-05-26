print("Hello world")

# The code is the same as the old version. 

def reverseWords(input): 
      
    inputWords = input.split(" ") 

    inputWords=inputWords[-1::-1] 
  
    output = ' '.join(inputWords) 
      
    return output 
  
  
if __name__ == "__main__": 
    input = 'I like runoob'
    rw = reverseWords(input) 
    print(rw)

    class MyNumbers:
  def __iter__(self):
    self.a = 1
    return self
 
  def __next__(self):
    x = self.a
    self.a += 1
    return x
 
myclass = MyNumbers()
myiter = iter(myclass)
 
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))