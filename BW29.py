# 게터와 세터 메서드 대신에 일반 속성을 사용하자

class OldResistor(object):
    def __init__(self, ohms):
        self._ohms = ohms

    def get_ohms(self):
        return self._ohms

    def set_ohms(self, ohms):
        self._ohms = ohms


r0 = OldResistor(50e3)
print('Before: %5r' % r0.get_ohms())

r0.set_ohms(10e3)
print('After: %5r' % r0.get_ohms())

# 게터와 세터 메스드는 특히 즉석에서 증가시키기 같은 연산에는 사용하기 불편하다.
r0.set_ohms(r0.get_ohms() + 5e3)
print('After: %5r' % r0.get_ohms())


# 파이썬에서는 명시적인 게터와 세터를 구현할 일이 거의 없다.
# 대신 항상 간단한 공개 속성부터 구현하기 시작해야 한다.
class Resistor(object):
    def __init__(self, ohms):
        self.ohms = ohms
        self.voltage = 0
        self.current = 0

r1 = Resistor(50e3)
r1.ohms = 10e3

r1.ohms += 5e3

# 나중에 속성을 설정할 때 특별한 동작이 일어나야 한다면 @property decorator와 이에 대응하는 setter 속성을 사용하는 방법으로 바꿀 수 있다.
class VoltageResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)
        self._voltage = 0

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        self._voltage = voltage
        self.current = self._voltage / self.ohms


r2 = VoltageResistance(1e3)
print('Before: %5r amps' % r2.current)
r2.voltage = 10
print('After: %5r amps' % r2.current)


# 프로퍼티에 setter를 설정하면 클래스에 전달된 값들의 타입을 체크하고 값을 검증할 수도 있다.
# 다음은 모든 저항값이 0옴보타 큼을 보장하는 클래스를 정의한 것이다.
class BoundedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if ohms <= 0:
            raise ValueError('%f ohms must be > 0' % ohms)
        self._ohms = ohms


r3 = BoundedResistance(1e3)
# r3.ohms = 0
# BoundedResistance(-5)

