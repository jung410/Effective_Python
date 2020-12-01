'''
자식 프로세스를 관리하려면 subprocess를 사용하자.
가장 간단한 방법은 내장 모듈 subprocess를 사용하는 것.
'''
import subprocess
from time import time

proc = subprocess.Popen(
    ['echo', 'Hello from th child!'],
    stdout=subprocess.PIPE
)
out, err = proc.communicate()
print(out.decode('utf-8'))


def run_sleep(period):
    proc = subprocess.Popen(['sleep', str(period)])
    return proc

start = time()
procs = []
for _ in range(10):
    proc = run_sleep(0.1)
    procs.append(proc)

for proc in procs:
    proc.communicate()
end = time()
print('Finished in %.3f seconds' % (end - start))
