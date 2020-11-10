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


class LoggingLazyDB(LazyBD):
    def __getattr__(self, name):
        print('Called __getattr__(%s)' % name)
        return super().__getattr__(name)

data = LoggingLazyDB()
print('exists:', data.exists)
print('foo: ', data.foo)
print('foo: ', data.foo)

# 데이터베이스 시스템에서 트랜잭션도 원한다고 하자.
# 사용자가 다음 번에 속성에 접근할 때는 대응하는 데이터베이스의 로우가 여전히 유요한지,
# 트랜잭션이 여전히 열려 있는지 알고 싶다고 해보자.
# __getattr__ hook는 기존 속성에 빠르게 접근하려고 객체의 인스턴스 딕셔너리를 사용할 것이므로 이 작업에는 믿고 쓸 수 없다.
# 이것을 고려한 __getattribute__ 가 존재한다.
# 이 특별한 메서드는 객체의 속성에 접근할 때마다 호출되며, 심지어 해당 속성이 속성 딕셔너리에 있을 때도 호출된다.

class ValidatingDB(object):
    def __init__(self):
        self.exists = 5

    def __getattribute__(self, name):
        print('Called __getattribute__(%s)' % name)
        try:
            return super().__getattribute__(name)
        except AttributeError:
            value = 'Value for %s' % name
            setattr(self, name, value)
            return value

data = ValidatingDB()
print('exists:', data.exists)
print('foo: ', data.foo)
print('foo: ', data.foo)


class SavingDB(object):
    def __setattr__(self, key, value):
        super().__setattr__(key, value)

class LoggingSavingDB(SavingDB):
    def __setattr__(self, key, value):
        print('Called __setattr__(%s, %r)' % (key, value))
        super().__setattr__(key, value)

data = LoggingSavingDB()
print('--------------------------------------------------')
print('Before: ', data.__dict__)
data.foo = 5
print('After: ', data.__dict__)
data.foo = 7
print('Finally: ', data.__dict__)