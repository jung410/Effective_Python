# 메타클래스로 서브클래스를 검증하자
# 메타클래스를 응용하는 가장 간단한 사례는 클래스를 올바르게 정의했는지 검증하는 것.

class Meta(type):
    def __new__(meta, name, bases, class_dict):
        print((meta, name, bases, class_dict))
        return type.__new__(meta, name, bases, class_dict)


class MyClass(object, metaclass=Meta):
    stuff = 123

    def foo(self):
        pass


# meta = Meta()
my_class = MyClass()


print('sss')
