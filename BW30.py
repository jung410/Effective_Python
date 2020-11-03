'''
내장 @property 데코레이터를 이용하면 더 간결한 방식으로 인스턴스의 속성에 접근하게 할 수 있다.
단순 숫자 속성을 즉석에서 계산하는 방식으로 변경하는 것
호출하는 쪽을 변경하지 않고도 기존에 클래스를 사용한 곳이 새로운 동작을 하게 해주므로 매우 유용함
'''
# 구멍 난 양동이의 할당량을 일반 파이썬 객체로 구현
from datetime import timedelta, datetime


class Bucket(object):
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        # self.quota = 0
        self.max_quota = 0
        self.quota_consumed = 0

    def __repr__(self):
        # return 'Bucket(quota=%d)' % self.quota
        return 'Bucket(max_quota=%d, quota_consumed=%d)' % (self.max_quota, self.quota_consumed)

    @property
    def quota(self):
        return self.max_quota - self.quota_consumed

    @quota.setter
    def quota(self, amount):
        delta = self.max_quota - amount
        if amount == 0:
            self.quota_consumed = 0
            self.max_quota = 0
        elif delta < 0:
            assert self.quota_consumed == 0
            self.max_quota = amount
        else:
            assert self.max_quota >= self.quota_consumed
            self.quota_consumed += delta

def fill(bucket, amount):
    now = datetime.now()
    if now - bucket.reset_time > bucket.period_delta:
        bucket.quota = 0
        bucket.reset_time = now
    bucket.quota += amount

def deduct(bucket, amount):
    now = datetime.now()
    if now - bucket.reset_time > bucket.period_delta:
        return False
    if bucket.quota - amount < 0:
        return False
    bucket.quota -= amount
    return True


bucket = Bucket(60)
fill(bucket, 100)
print('Initial', bucket)

if deduct(bucket, 99):
    print('Had 99 quota')
else:
    print('Not enough for 99 quota')
print('Now', bucket)

if deduct(bucket, 3):
    print('Had 3 quota')
else:
    print('Not enough for 3 quota')
print('Still', bucket)