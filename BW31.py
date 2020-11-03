# 재사용 가능한 @property 메서드에는 디스크립터를 사용하자.
# 파이썬에 내장된 @property의 큰 문제점은 재사용성이다.
# 다시 말해, @property로 데코레이트를 하는 메서드를 같은 클래스에 속한 여러 속성에 사용하지 못한다.
from weakref import WeakKeyDictionary


class Homework(object):
    def __init__(self):
        self._grade = 0

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._grade = value


galileo = Homework()
galileo.grade = 95


class Exam(object):
    def __init__(self):
        self._writing_grade = 0
        self._math_grade = 0

    @staticmethod
    def _check_grade(value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')

    @property
    def writing_grade(self):
        return self._writing_grade

    @writing_grade.setter
    def writing_grade(self, value):
        self._check_grade(value)
        self._writing_grade = value

    @property
    def math_grade(self):
        return self._math_grade

    @math_grade.setter
    def math_grade(self, value):
        self._check_grade(value)
        self._math_grade = value

# 위 class는 범용으로 사용하기에 좋지 않다.
# 추가로 다른 점수들을 사용하기 위해서 같은 코드를 계속 추가해야 한다.
# 더 좋은 방법은 디스크립터를 사용하는 것.

class Grade(object):
    def __init__(self):
        self._value = 0

    def __get__(self, instance, instance_type):
        return self._value

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._value = value

class Exam(object):
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()

# exam = Exam()
# exam.writing_grade = 40
first_exam = Exam()
first_exam.writing_grade = 82
first_exam.science_grade = 99
print('Writing', first_exam.writing_grade)
print('Science', first_exam.science_grade)

second_exam = Exam()
second_exam.writing_grade = 75
print('Second', second_exam.writing_grade, 'is right')
print('First', first_exam.writing_grade, 'is wrong')


# 위의 문제는 한 Grade 인스턴스가 모든 Exam 인스턴스의 writing_grade 클래스 속성으로 공유된다는 점.
# 해결 : 각 Exam 인스턴스별로 값을 추적하는 Grade class가 필요하다.

class Grade2(object):
    def __init__(self):
        self._value = {}

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return self._value.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._value[instance] = value
# Grade2는 메모리 누수 현상이 일어난다.
# _value dictionary가 instance를 계속 가지고 있기 때문

class Grade3(object):
    def __init__(self):
        self._value = WeakKeyDictionary()

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return self._value.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._value[instance] = value


class Exam3(object):
    math_grade = Grade3()
    writing_grade = Grade3()
    science_grade = Grade3()


first_exam3 = Exam3()
first_exam3.writing_grade = 82
first_exam3.science_grade = 99
print('Writing', first_exam3.writing_grade)
print('Science', first_exam3.science_grade)

second_exam3 = Exam3()
second_exam3.writing_grade = 75
print('Second', second_exam3.writing_grade, 'is right')
print('First', first_exam3.writing_grade, 'is right')













