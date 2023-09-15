import random as rd
from run import run

great = 0.4         # 우수 개체 선정 비율
childs = 5          # 한 쌍의 부모 개체들의 자식 개체 수
mutation_p = 5      # 변이 확률(%, 정수)
aw = 1/10           # attempts에 부여되는 가중치
initial_generation = 100   # 첫 세대 개체 수
n_generation = 15  # 몇 세대까지 진행할건지


def distance(c):
    dis = 500000-((500-c[0])**2 + (500-c[1])**2)
    return dis      # 변위 (0~500000)


with open("log.txt", "w") as g:
    g.write("")


def create_child(p1, p2):
    child = []
    min_len_parent = max(len(p1), len(p2))
    for i in range(min_len_parent):
        if (int(rd.randint(1, 100)) > 50):
            if i+1 > len(p1):
                child.append(rd.choice([90, 180, 270, 360]))
            else:
                child.append(p1[i])
        else:
            if i+1 > len(p2):
                child.append(rd.choice([90, 180, 270, 360]))
            else:
                child.append(p2[i])
    return child


def create_children(parents, n_child):
    next_population = []
    for i in range(int(len(parents)/2)):
        for j in range(n_child):
            next_population.append(create_child(
                parents[i][3], parents[len(parents)-1-i][3]))
    return next_population


def mutate(m):
    dirs = [0, 90, -90]
    m[rd.randint(0, len(m)-1)] = rd.choice(
        dirs)         # history 중에 하나를 랜덤으로 바꿈
    return m


def mutated_population(normal_population, probability):
    for i in range(len(normal_population)):
        if rd.randint(1, 100) <= probability:
            normal_population[i] = mutate(normal_population[i])
    return normal_population


def go(direction):
    global current_coordinates
    if direction == 90:
        current_coordinates[1] += 50
    elif direction == 270 or direction == -90:
        current_coordinates[1] -= 50
    elif direction == 360 or direction == 0:
        current_coordinates[0] += 50
    elif direction == 180:
        current_coordinates[0] -= 50


def processing(current_coordinates, attempts, history):
    score = ((distance(current_coordinates)/(attempts**aw))) / \
        (500000/20**aw)*100

    history_to_append = ([current_coordinates, distance(
        current_coordinates), attempts, history, score])

    return [score, history_to_append]


histories = []      # [좌표, 변위, 시도횟수, 기록, 점수]
current_coordinates = [0, 0]
final_result = []   # 최종적으로 시뮬레이션되는 개체들

for i in range(initial_generation):         # 초깃값 생성
    history = []
    current_coordinates = [0, 0]
    attempts = 0
    while True:
        direction = rd.randint(1, 4)*90
        if (0 <= current_coordinates[0] <= 500) and (0 <= current_coordinates[1] <= 500) and (current_coordinates != [500, 500]):
            go(direction)
            history.append(direction)
            attempts = attempts + 1
        else:
            break

    score = processing(current_coordinates, attempts, history)[0]
    histories.append(processing(current_coordinates, attempts, history)[1])


histories_sorted = sorted(histories, key=lambda x: x[4], reverse=True)
histories_sorted = histories_sorted[:round((len(histories_sorted)+1)*great)]
rd.shuffle(histories_sorted)


new_generation_basis = create_children(histories_sorted, childs)
new_generation_basis = mutated_population(new_generation_basis, mutation_p)
print(new_generation_basis)

for i in range(n_generation-1):      # 세대 수

    histories = []      # [좌표, 변위, 시도횟수, 기록, 점수]
    current_coordinates = [0, 0]

    for i in new_generation_basis:
        history = []
        current_coordinates = [0, 0]
        attempts = 0

        for j in i:
            if (0 <= current_coordinates[0] <= 500) and (0 <= current_coordinates[1] <= 500) and (current_coordinates != [500, 500]):
                go(j)
                history.append(j)
                attempts = attempts + 1

        score = processing(current_coordinates, attempts, history)[0]
        histories.append(processing(current_coordinates, attempts, history)[1])

    histories_sorted = sorted(histories, key=lambda x: x[4], reverse=True)
    histories_sorted = histories_sorted[:round(
        (len(histories_sorted)+1)*great)]
    rd.shuffle(histories_sorted)

    new_generation_basis = create_children(histories_sorted, childs)
    new_generation_basis = mutated_population(new_generation_basis, mutation_p)
    print(new_generation_basis)         # 교배, 변이까지 마친 새 세대
    print(len(new_generation_basis))

    final_result.append(histories_sorted[0])    # 해당 세대에서 가장 뛰어난 한 개체를 선출


for i in new_generation_basis:
    history = []
    current_coordinates = [0, 0]
    attempts = 0

    for j in i:
        if (0 <= current_coordinates[0] <= 500) and (0 <= current_coordinates[1] <= 500) and (current_coordinates != [500, 500]):
            go(j)
            history.append(j)
            attempts = attempts + 1

    score = processing(current_coordinates, attempts, history)[0]
    histories.append(processing(current_coordinates, attempts, history)[1])

histories_sorted = sorted(histories, key=lambda x: x[4], reverse=True)
histories_sorted = histories_sorted[:3]

print(histories_sorted)
final_result.append(histories_sorted[0])    # 해당 세대에서 가장 뛰어난 한 개체를 선출

final_result_to_run = []
o = 0
while o < len(final_result):
    final_result_to_run.append(final_result[o])
    o += 1
run(final_result_to_run)
input("")       # 엔터 입력하면 꺼짐
