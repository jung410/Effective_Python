# 메타클래스로 클래스의 존재를 등록하자
# 프로그램에 있는 타입을 자동으로 등록하는 것
# ex) 파이썬 객체를 직렬화한 표현을 JSON으로 구현한다고 해보자.
import json


class Serializable(object):
    def __init__(self, *args):
        self.args = args

    def serialize(self):
        return json.dumps({'args': self.args})


class Point2D(Serializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Point2D(%d, %d)' % (self.x, self.y)

point = Point2D(5, 3)
print('Object: ', point)
print('Serialized:', point.serialize())

print('-----------------------------------------------')
# 이제 이 Json 문자열을 역직렬화해서 Json이 표현하는 Point2D 객체를 생성한다.
class Deserializable(Serializable):
    @classmethod
    def deserialize(cls, json_data):
        params = json.loads(json_data)
        return cls(*params['args'])

class BetterPoint2D(Deserializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Point2D(%d, %d)' % (self.x, self.y)

point2 = BetterPoint2D(5, 3)
print('Before: ', point2)
data = point2.serialize()
print('Serialized: ', data)
after = BetterPoint2D.deserialize(data)
print('After: ', after)

# 어떤 클래스든 대응하는 파이썬 객체로 역직렬화하는 공통 함수를 하나만 두려고 할 것이다.
class BetterSerializable(object):
    def __init__(self, *args):
        self.args = args

    def serialize(self):
        return json.dumps({
            'class': self.__class__.__name__,
            'args': self.args,
        })

    def __repr__(self):
        return 'EvenBetterPoint2D(%d, %d)' % (self.x, self.y)


registry = {}
def register_class(target_class):
    registry[target_class.__name__] = target_class

def deserialize(data):
    params = json.loads(data)
    name = params['class']
    target_class = registry[name]
    return target_class(*params['args'])

class EvenBetterPoint2D(BetterSerializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

register_class(EvenBetterPoint2D)

print('-----------------------------------------------')
point = EvenBetterPoint2D(5, 3)
print(point)
data = point.serialize()
print(data)
after = deserialize(data)
print(after)

# 위 방법의 문제는 register_class를 호출하는 일을 잊어버릴 수 있다는 것.
class Point3D(BetterSerializable):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.x = x
        self.y = y
        self.z = z



# point = Point3D(5, 9 -4)
# data = point.serialize()
# after = deserialize(data)

class Meta(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        register_class(cls)
        return cls

class RegisteredSerializable(BetterSerializable, metaclass=Meta):
    pass

class Vector3D(RegisteredSerializable):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.x, self.y, self.z = x, y, z

    def __repr__(self):
        return 'Vector3D(%d, %d, %d)' % (self.x, self.y, self.z)


print('-----------------------------------------------')
v3 = Vector3D(10, -7, 3)
print('Before: ', v3)
data = v3.serialize()
print('Serialized: ', data)
print('After: ', deserialize(data))