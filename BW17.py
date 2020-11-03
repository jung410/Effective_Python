# 인수를 순회할 때는 방어적으로 하자
def normalize(numbers):
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

visits = [15, 35, 80]
percentages = normalize(visits)
print(percentages)

def read_visits(data_path):
    with open(data_path) as f:
        for line in f:
            yield int(line)
