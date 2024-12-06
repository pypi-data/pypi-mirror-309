from typing import Callable, Any

class on_travel():
    def __init__(self, *target):
        self._list = target
    
    def __call__(self, func: Callable):
        def wrapper(start:int = 0):
            for i, (args) in enumerate(zip(*self._list), start):
                yield from func(i, *args)
        return wrapper
    
class Config:
    def __init__(self):
        self._variants = dict[str, Any]()

    def __getattribute__(self, name):
        if name in super().__getattribute__('_variants'):
            return self._variants[name]
        return super().__getattribute__(name)
    
    def __setattr__(self, name, value):
        if name == '_variants':
            super().__setattr__(name, value)
        else:
            self._variants[name] = value
    
    def __delattr__(self, name):
        if name in self._variants:
            del self._variants[name]
        else:
            super().__delattr__(name)

    def __str__(self):
        c = 0
        ret = ""
        for k, v in super().__getattribute__('_variants').items():
            if c:
                ret += ', '
            ret += f"{k}: {v}"
            c += 1
        return ret if ret else None
    
    def have(self):
        return [(k) for k in super().__getattribute__('_variants').keys()]

if __name__ == '__main__':
    A = Config()
    A.B = 15
    A.C = {"23": 12, "34": 1233}
    A.D = Config()
    A.D.A = 15
    print(A.have())