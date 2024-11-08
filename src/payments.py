
class Billing: 
    def __init__(self, accuracy: int = 2):
        self.__default_balance = 0.00
        self.__accuracy = accuracy 
    
    @property
    def zero_balance(self) -> float:
        return round(self.__default_balance, self.__accuracy)