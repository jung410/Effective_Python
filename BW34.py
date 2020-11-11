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