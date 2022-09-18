class Meta(type):
    children_number = 0

    def __new__(mcs, *args, **kwargs):
        return type.__new__(mcs, *args, **kwargs)

    def __init__(cls, *args, **kwargs):
        cls.class_number = Meta.children_number
        Meta.children_number += 1

    def __call__(cls, data, *args, **kwargs):
        instance = object.__new__(cls, *args, **kwargs)
        instance.__init__(cls, *args, **kwargs)
        return instance


class Cls1(metaclass=Meta):
    def __init__(self, data):
        self.data = data


class Cls2(metaclass=Meta):
    def __init__(self, data):
        self.data = data


assert (Cls1.class_number, Cls2.class_number) == (0, 1)
a, b = Cls1(''), Cls2('')
assert (a.class_number, b.class_number) == (0, 1)

