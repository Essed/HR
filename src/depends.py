class Depends:
    def __init__(self):
        self.__args = None
        self.__kwargs = None

    @property
    def non_name_parametrs(self) -> tuple:
        return self.__args

    @property
    def key_value_parameters(self) -> dict:
        return self.__kwargs
    
    async def inject(self, *arg, **kwargs):
        self.__args = arg
        self.__kwargs = kwargs