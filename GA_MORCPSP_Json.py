"""
---写在前面---
项目的鲁棒性，根据某论文中的理论，是等于各个活动的鲁棒性之和
而每个活动的鲁棒性又等于本活动的总时差（最早开始时间-最晚开始时间）乘以本活动的累积不稳定权重
而每个活动的累积不稳定权重又等于本活动的不稳定权重加上该活动的所有紧后活动的不稳定权重
为了计算方便，本文对所有活动的不稳定权重都取0.1
因此，拥有紧后活动数量多的活动的累积不稳定权重自然就大

[[1,0,0],[2,0,2],[4,3,6],[3,8,10],[5,10,10]]
活动1的紧后活动为活动2，活动1的总时差为0
活动2的紧后活动为活动3和活动4，活动2的总时差为0
活动3的紧后活动为活动5，活动3的总时差为1
活动4的紧后活动为活动5，活动4的总时差为0
活动5没有紧后活动，活动5的总时差为0
鲁棒性=0*(0.1+0.1)+0*(0.1*3)+1*(0.1+0.1)+0*(0.1+0.1)+0*(0.1+0.1)=0.2

writen by 二开金城武
"""
import copy
import random
import numpy as np
import matplotlib.pyplot as plt
project={
    1:{"successors":[2, 3, 4, 5],"predecessors":[],"duration":0,"resource_request":[0, 0, 0, 0]},
    2:{"successors":[6],"predecessors":[1],"duration":2,"resource_request":[0, 1, 0, 0]},
    3:{"successors":[10],"predecessors":[1],"duration":4,"resource_request":[0, 0, 0, 3]},
    4:{"successors":[9],"predecessors":[1],"duration":6,"resource_request":[0, 0, 2, 0]},
    5:{"successors":[11],"predecessors":[1],"duration":9,"resource_request":[0, 0, 7, 0]},
    6:{"successors":[7],"predecessors":[2],"duration":8,"resource_request":[0, 0, 5, 0]},
    7:{"successors":[8, 11],"predecessors":[6],"duration":10,"resource_request":[3, 0, 0, 0]},
    8:{"successors":[12],"predecessors":[7],"duration":4,"resource_request":[0, 0, 0, 7]},
    9:{"successors":[12],"predecessors":[4],"duration":3,"resource_request":[3, 0, 0, 0]},
    10:{"successors":[12],"predecessors":[3],"duration":5,"resource_request":[0, 0, 6, 0]},
    11:{"successors":[12],"predecessors":[5, 7],"duration":1,"resource_request":[0, 9, 0, 0]},
    12:{"successors":[],"predecessors":[8, 9, 10, 11],"duration":0,"resource_request":[0, 0, 0, 0]},
    "total_resource": [3, 9, 9, 9]

}
# 种群初始化操作，我想用离散编码的方式，即列表中的元素表示的是每个活动的开始时间，列表的索引+1是活动的序号
project = {
    "total_resource": [3, 9, 9, 9],
    1: {"successors": [2, 3, 4, 5], "predecessors": [], "duration": 0, "resource_request": [0, 0, 0, 0]},
    2: {"successors": [6], "predecessors": [1], "duration": 2, "resource_request": [0, 1, 0, 0]},
    3: {"successors": [10], "predecessors": [1], "duration": 4, "resource_request": [0, 0, 0, 3]},
    4: {"successors": [9], "predecessors": [1], "duration": 6, "resource_request": [0, 0, 2, 0]},
    5: {"successors": [11], "predecessors": [1], "duration": 9, "resource_request": [0, 0, 7, 0]},
    6: {"successors": [7], "predecessors": [2], "duration": 8, "resource_request": [0, 0, 5, 0]},
    7: {"successors": [8, 11], "predecessors": [6], "duration": 10, "resource_request": [3, 0, 0, 0]},
    8: {"successors": [12], "predecessors": [7], "duration": 4, "resource_request": [0, 0, 0, 7]},
    9: {"successors": [12], "predecessors": [4], "duration": 3, "resource_request": [3, 0, 0, 0]},
    10: {"successors": [12], "predecessors": [3], "duration": 5, "resource_request": [0, 0, 6, 0]},
    11: {"successors": [12], "predecessors": [5, 7], "duration": 1, "resource_request": [0, 9, 0, 0]},
    12: {"successors": [], "predecessors": [8, 9, 10, 11], "duration": 0, "resource_request": [0, 0, 0, 0]}
}

def  initialize(project:dict,size:int,makespan:int):
    population=[]
    while len(population)<size:
        project = copy.deepcopy(project)
        all_activities=[i+1 for i in range(len(project)-1)]
        assigned_activities=[1]
        unassigned_activities=copy.deepcopy(all_activities)
        unassigned_activities.remove(1)
        candidate_activities=copy.deepcopy(project[1]["successors"])
        scheme=[-1]*(len(project)-1)  # 染色体，这里染色体每个元素所代表的活动的索引值刚好是小于这个活动的活动序号的，因为列表的索引是从0开始的
        scheme[0]=0
        while unassigned_activities:

            if len(candidate_activities)==0:
                break
            random_activity = random.sample(candidate_activities, 1)[0]  # 随机选取活动
            candidate_activity = random_activity
            early_start_time_s = [scheme[predecessor_candidate_activity-1]+project[predecessor_candidate_activity]["duration"]
                                  for predecessor_candidate_activity in project[candidate_activity]["predecessors"]]
            # print(f"num:{s+1} candidate_activities:{candidate_activities}")
            if candidate_activity==len(project)-1:
                early_start_time = makespan
            else:
                early_start_time = max(early_start_time_s)

            while True:
                if _is_resource_enough(candidate_activity,early_start_time,assigned_activities,project,scheme):
                    scheme[candidate_activity-1]=early_start_time
                    assigned_activities.append(candidate_activity)
                    unassigned_activities.remove(candidate_activity)
                    candidate_activities.remove(candidate_activity)
                    successors=copy.deepcopy(project[candidate_activity]["successors"])
                    for successor in successors:
                        if successor in assigned_activities:
                            successors.remove(successor)
                        if set(project[successor]["predecessors"]).intersection(set(unassigned_activities)):
                            successors.remove(successor)
                    candidate_activities+=successors
                    if len(candidate_activities) > 1:
                        for a in candidate_activities:
                            if a == len(project)-1:
                                candidate_activities.remove(a)
                    break
                else:
                    early_start_time+=1

        good_scheme=True
        for gene in scheme[:-1]:
            if gene >= scheme[-1]:
                good_scheme=False
                break
        if good_scheme:
            population.append(scheme)
    return population

def _is_resource_enough(candidate_activity, early_start_time, assigned_activities, project:dict,scheme):
    t = early_start_time + 1
    while t <= early_start_time + project[candidate_activity]["duration"]:
        sum_resource = np.zeros(len(project["total_resource"]))
        for assigned_activity in assigned_activities:
            if scheme[assigned_activity-1]+ 1 <= t <= scheme[assigned_activity-1] + project[assigned_activity]["duration"]:
                sum_resource += project[assigned_activity]["resource_request"]
        sum_resource += project[candidate_activity]["resource_request"]
        if (sum_resource > np.array(project["total_resource"])).any():
            return False
        t += 1

    return True
def _is_resource_enough_project(scheme, project):
    total_resource=np.array(project["total_resource"]*(len(project)-1))\
        .reshape((len(project)-1),len(project["total_resource"]))
    avail_resource=copy.deepcopy(total_resource)
    for i,gene in enumerate(scheme):
        id=i+1
        start=gene
        end=start+project[id]["duration"]
        avail_resource[start:end]-=project[id]["resource_request"]
        if (avail_resource<0).any():
            return False
    return True
def _cross(parent1,parent2):
    # 随机选择交叉区域
    start, end = sorted(random.sample([x for x in range(1, len(parent1) - 1)], 2))
    # 将父代1中交叉区域的基因复制到子代1和2中
    child1 = parent1[:start] + parent2[start:end + 1] + parent1[end + 1:]
    child2 = parent2[:start] + parent1[start:end + 1] + parent2[end + 1:]
    return child1,child2
print("这里只是部分代码，加群免费下载群文件即可，\n群号:808756207")
exit()


def _good_mutation(scheme:list,i,project:dict):
    if not _is_resource_enough_project(scheme,project):
        return None
    id = i+1  # id是活动序号，i是scheme列表的索引
    for s in project[id]["successors"]:
        # 如果这个紧后活动不是最后一个虚结束活动的话
        if s != len(project)-1:
            #  如果当前活动的结束时间大于它某个紧后活动的开始时间
            if scheme[i]+project[id]["duration"]>scheme[s-1]:
                scheme[s-1]=scheme[i]+project[id]["duration"]
                scheme=_good_mutation(scheme,s-1,project)
                if scheme == None:
                    return None
        else:
            if scheme[i]+project[id]["duration"]>scheme[s-1]:
                return None
    return scheme

def _mutate(scheme:list,project:dict,mutation_rate):
    scheme_copy=copy.deepcopy(scheme)
    if mutation_rate > random.random():
        gene_index_s = [x + 1 for x in range(len(scheme) - 2)]
        while True:
            if len(gene_index_s) == 0:
                return scheme
            gene_index = random.sample(gene_index_s, 1)[0]
            scheme_copy[gene_index]+=1
            scheme_copy=_good_mutation(scheme,gene_index,project)
            if scheme_copy==None:
                gene_index_s.remove(gene_index)
                scheme_copy = copy.deepcopy(scheme)
                continue
            else:
                return scheme_copy
    return scheme_copy

def _calculate_project_earliest_start_times(project:dict):
    # 计算最早开始时间和最早完成时间
    earliest_start_times = [-1]*(len(project)-1)
    earliest_finish_times = [-1]*(len(project)-1)
    for id in range(1,len(project)):
        if not project[id]["predecessors"]:

            earliest_start_times[id-1]=0
        else:
            earliest_start_times[id-1]=max(
                [earliest_finish_times[p-1] for p in project[id]["predecessors"]]
            )
        earliest_finish_times[id-1]=earliest_start_times[id-1]+project[id]["duration"]
    return earliest_start_times

def _fitness_scheme(scheme:list,project:dict):
    # 各个活动的不稳定权重都为0.1
    earliest_start_times=_calculate_project_earliest_start_times(project)
    total_floats=list(np.array(scheme) -np.array(earliest_start_times))
    robustness=0
    for i in range(len(scheme)):
        id=i+1
        robustness+=(0.1+len(project[id]["successors"])*0.1)*total_floats[i]
    return robustness

def fitness_population(population:list,project:dict):
    total_fitness=0
    for scheme in population:
        total_fitness+=_fitness_scheme(scheme,project)
    return total_fitness

# 最小工期、最大工期、工期的区间
makespan_min=_calculate_project_earliest_start_times(project)[-1]
makespan_max=50
makespan_range=[x for x in range(makespan_min,makespan_max+1)]
size=50
iteration=100
mutation_rate=0.3
pareto_frontier=[]
for makespan in makespan_range:
    population=initialize(project,size,makespan)
    fitness=[]
    for _ in range(iteration):
        print(f"工期为：{makespan} 的第 {_} 次迭代")
        population_for_cross=[]
        while len(population_for_cross)<size:
            parent1,parent2=random.sample(population,2)
            if _fitness_scheme(parent1,project)>_fitness_scheme(parent2,project):
                population_for_cross.append(parent1)
            else:
                population_for_cross.append(parent2)
        population_for_mutate=[]
        while len(population_for_mutate)<size:
            parent1,parent2=random.sample(population_for_cross,2)
            child1,child2=_cross(parent1,parent2)
            population_for_mutate.append(child1)
            population_for_mutate.append(child2)
        population_evolved=[]
        while len(population_evolved)<size:
            child_for_mutate=random.sample(population_for_mutate,1)[0]
            child_evolved=_mutate(child_for_mutate,project,mutation_rate)
            population_evolved.append(child_evolved)
        population=population_evolved
        fitness.append(fitness_population(population,project))
    pareto_frontier.append([makespan,fitness[-1]])

x=[x[0] for x in pareto_frontier]
# x=[1/x[0] for x in pareto_frontier]
y=[x[1] for x in pareto_frontier]
plt.scatter(x,y)
plt.plot(x,y)
plt.xlabel("makespan")
plt.ylabel("robustness")
plt.title("Robustness of the project and Pareto frontier \nof dual objectives of project duration")
plt.xticks(range(min(x),max(x)+1))
plt.show()


























