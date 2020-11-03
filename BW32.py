# 지연 속성에는 getattr, getattribute, setattr을 사용하자.
# 언어후크를 이용하면 범용 코드를 쉽게 만들 수 있음
# 클래스에 _getattr__ 메서드를 정의하면 객체의 인스턴스 딕셔너리에서 속성을 찾을 수 없을 때마다 이 메서드가 호출된다.

class LazyBD(object):
    def __init__(self):
        self.exists = 5

    def __getattr__(self, name):
        value = 'Value for %s' % name
        setattr(self, name, value)
        return value

# 존재하지 않는 속성인 foo에 접근
data = LazyBD()
print('Before:', data.__dict__)
print('foo:', data.foo)
print('After:', data.__dict__)
