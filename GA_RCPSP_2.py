"""PMX算子，又称部分映射交叉算子（Partially Mapped Crossover，简称PMX）用来进行交叉操作。"""
import copy
import random
import time
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
plt.rcParams["axes.labelsize"]=14
plt.rcParams["xtick.labelsize"]=12
plt.rcParams["ytick.labelsize"]=12


class Activity(object):
    '''
    活动类：包含  1.活动ID  2.活动持续时间    3.活动资源需求量   4.活动紧前活动    5.活动最早开始时间  6.活动最晚开始时间  7.活动是否被访问
    '''

    def __init__(self, id, duration, resourceRequest, successor):
        self.id = id
        self.duration = duration
        self.resourceRequest = np.array(resourceRequest)
        self.predecessor = None
        self.successor = successor
        self.es = 0
        self.ef = 0
        self.ls = 0
        self.lf = 0
        self.tf=0
        self.visited = False
class Painter:
    def __init__(self,project=None,total_resource=None):
        self.project=project
        self.total_resource=total_resource

    def draw_activities(self):
        print("开始画了")
        colors = ['#ff1493', 'g', 'r', 'c', 'm', 'y', 'k', '#FFA500', '#800080', '#00FFFF', '#008080', '#FFC0CB']
        # 第一张图
        plt.figure(figsize=(6, 8))
        plt.subplot(4, 1, 1)
        rects4 = []
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
        plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
        left, right=plt.xlim([0, self.project[-1].es])
        bottom, top=plt.ylim([0,self.total_resource[0]] )  # 改
        y_ticks = [y for y in range(0,int(top),2)]
        y_tick_labels = [y for y in range(0,int(top),2)]
        plt.yticks(y_ticks, y_tick_labels)
        x_ticks = [x for x in range(0,int(right)+1)]
        x_tick_labels = ["" for x in range(0,int(right+1))]
        plt.xticks(x_ticks, x_tick_labels)
        plt.text(self.project[-1].es/2,self.total_resource[0]+1
                 ,'mv1.rcp数据集项目活动进度图（活动工期优先）', fontsize=16,ha="center",va="center")
        for activity in self.project:
            if activity.resourceRequest[0]!=0:  # 改
                pillar=(activity.es,activity.es+activity.duration,activity.resourceRequest[0],0)  # 改
                rect = plt.Rectangle((pillar[0], pillar[3]), width=pillar[1] - pillar[0], height=pillar[2])
                if len(rects4)!=0:
                    for r in rects4:
                        if Painter.is_intersected(rect,r):
                            pillar = (activity.es, activity.es + activity.duration, activity.resourceRequest[0], r.get_height()+r.get_y())  # 改
                            rect = plt.Rectangle((pillar[0], pillar[3]), width=pillar[1] - pillar[0], height=pillar[2])
                rects4.append(rect)
                bar_container=self.draw_pillar(plt,pillar,color=colors[activity.id-1])
                plt.text(bar_container[0].get_x()+bar_container[0].get_width()/2
                         ,bar_container[0].get_height()/2+bar_container[0].get_y()-0.5
                         ,"活动 {}".format(activity.id),ha='center', color='white', fontweight='bold')
                plt.text(-4.5,total_resource[0]/2,"1号资源")

        # 第二张图
        plt.subplot(4, 1, 2)
        rects4 = []
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
        plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
        left, right=plt.xlim([0, self.project[-1].es])
        bottom, top=plt.ylim([0,self.total_resource[1]] )  # 改
        y_ticks = [y for y in range(0,int(top),2)]
        y_tick_labels = [y for y in range(0,int(top),2)]
        plt.yticks(y_ticks, y_tick_labels)
        x_ticks = [x for x in range(0,int(right)+1)]
        x_tick_labels = ["" for x in range(0,int(right+1))]
        plt.xticks(x_ticks, x_tick_labels)
        for activity in self.project:
            if activity.resourceRequest[1]!=0:  # 改
                pillar=(activity.es,activity.es+activity.duration,activity.resourceRequest[1],0)  # 改
                rect = plt.Rectangle((pillar[0], pillar[3]), width=pillar[1] - pillar[0], height=pillar[2])
                if len(rects4)!=0:
                    for r in rects4:
                        if Painter.is_intersected(rect,r):
                            pillar = (activity.es, activity.es + activity.duration, activity.resourceRequest[1], r.get_height()+r.get_y())  # 改
                            rect = plt.Rectangle((pillar[0], pillar[3]), width=pillar[1] - pillar[0], height=pillar[2])
                rects4.append(rect)
                bar_container=self.draw_pillar(plt,pillar,color=colors[activity.id-1])
                plt.text(bar_container[0].get_x()+bar_container[0].get_width()/2
                         ,bar_container[0].get_height()/2+bar_container[0].get_y()-0.5
                         ,"活动 {}".format(activity.id),ha='center', color='k', fontweight='bold')
                plt.text(-4.5,total_resource[1]/2,"2号资源")


        # 第三张图
        plt.subplot(4, 1, 3)
        rects4 = []
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
        plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
        left, right=plt.xlim([0, self.project[-1].es])
        bottom, top=plt.ylim([0,self.total_resource[2]] )  # 改
        y_ticks = [y for y in range(0,int(top),2)]
        y_tick_labels = [y for y in range(0,int(top),2)]
        plt.yticks(y_ticks, y_tick_labels)
        x_ticks = [x for x in range(0,int(right)+1)]
        x_tick_labels = ["" for x in range(0,int(right+1))]
        plt.xticks(x_ticks, x_tick_labels)
        for activity in self.project:
            if activity.resourceRequest[2]!=0:  # 改
                pillar=(activity.es,activity.es+activity.duration,activity.resourceRequest[2],0)  # 改
                rect = plt.Rectangle((pillar[0], pillar[3]), width=pillar[1] - pillar[0], height=pillar[2])
                if len(rects4)!=0:
                    for r in rects4:
                        if Painter.is_intersected(rect,r):
                            pillar = (activity.es, activity.es + activity.duration, activity.resourceRequest[2], r.get_height()+r.get_y())  # 改
                            rect = plt.Rectangle((pillar[0], pillar[3]), width=pillar[1] - pillar[0], height=pillar[2])
                rects4.append(rect)
                bar_container=self.draw_pillar(plt,pillar,color=colors[activity.id-1])
                plt.text(bar_container[0].get_x()+bar_container[0].get_width()/2
                         ,bar_container[0].get_height()/2+bar_container[0].get_y()-0.5
                         ,"活动 {}".format(activity.id),ha='center', color='white', fontweight='bold')
                plt.text(-4.5,total_resource[2]/2,"3号资源")

        # 第四张图
        plt.subplot(4, 1, 4)
        rects4 = []
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
        plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
        left, right=plt.xlim([0, self.project[-1].es])
        bottom, top=plt.ylim([0,self.total_resource[3]] )  # 改
        y_ticks = [y for y in range(0,int(top),2)]
        y_tick_labels = [y for y in range(0,int(top),2)]
        plt.yticks(y_ticks, y_tick_labels)
        x_ticks = [x for x in range(0,int(right)+1)]
        x_tick_labels = [x for x in range(0,int(right)+1)]
        plt.xticks(x_ticks, x_tick_labels)
        plt.xlabel("时间进度",fontsize=12)
        for activity in self.project:
            if activity.resourceRequest[3]!=0:  # 改
                pillar=(activity.es,activity.es+activity.duration,activity.resourceRequest[3],0)  # 改
                rect = plt.Rectangle((pillar[0], pillar[3]), width=pillar[1] - pillar[0], height=pillar[2])
                if len(rects4)!=0:
                    for r in rects4:
                        if Painter.is_intersected(rect,r):
                            pillar = (activity.es, activity.es + activity.duration, activity.resourceRequest[3], r.get_height()+r.get_y())  # 改
                            rect = plt.Rectangle((pillar[0], pillar[3]), width=pillar[1] - pillar[0], height=pillar[2])
                rects4.append(rect)

                bar_container=self.draw_pillar(plt,pillar,color=colors[activity.id-1])

                plt.text(bar_container[0].get_x()+bar_container[0].get_width()/2
                         ,bar_container[0].get_height()/2+bar_container[0].get_y()-0.5
                         ,"活动 {}".format(activity.id),ha='center', color='white', fontweight='bold')
                plt.text(-4.5,total_resource[3]/2,"4号资源")
        plt.subplots_adjust(hspace=0)
        plt.show()
    def draw_pillar(self,plt,pillar:tuple,color):
        x1=pillar[0]
        x2=pillar[1]
        height=pillar[2]
        bottom=pillar[3]
        x_pillar=[x1]
        height=[height]
        bar_container=plt.bar(x_pillar,height=height,width=x2-x1,bottom=bottom,align="edge",edgecolor='black',color=color)

        return bar_container
    @staticmethod
    def is_intersected(bbox1,bbox2):
        """
        判断长方形是否相交
        :param bbox1:
        :param bbox2:
        :return:
        """
        if bbox1.get_x() < bbox2.get_x() + bbox2.get_width() and bbox1.get_x() + bbox1.get_width() > bbox2.get_x() and bbox1.get_y() < bbox2.get_y() + bbox2.get_height() and bbox1.get_y() + bbox1.get_height() > bbox2.get_y():
            return True
        else:
            return False
class Genetic_Algorithms:

    def __init__(self,project=None,total_resource=None):
        self.project=project
        self.total_resource=total_resource
    # 种群初始化算子
    def initialize_population(self,num_population):
        population=[]
        for i in range(num_population):
            project=copy.deepcopy(self.project)  # 深拷贝一份project，防止每次产生的活动序列太过相似
            all_activities = [value for value in project.values()]  # 所有的活动列表
            assigned_activities = [project[1]]  # 已经分配好的活动的列表
            unassigned_activities = all_activities.copy()  # 还没被分配好的活动的列表
            unassigned_activities.remove(project[1])
            candidate_activities = self._get_activities_via_ids(project[1].successor,project)  # 将要被分配的活动的列表
            while unassigned_activities:  # 当还没被分配好的活动的列表不为空时，就继续循环，直到把每个活动分配完成
                random_activity=random.sample(candidate_activities,1)[0]  # 随机选取活动
                candidate_activity=random_activity
                """
                以下，选择candidate_activity的所有紧前活动的
                开始时间+活动工期的最大值作为candidateActivity的
                开始时间
                """
                early_start_time_s = [predecessor_candidate_activity.es + predecessor_candidate_activity.duration
                                      for predecessor_candidate_activity in
                                      self._get_activities_via_ids(candidate_activity.predecessor, project)
                                      ]
                if candidate_activity.id==len(all_activities):
                    early_start_time = max(early_start_time_s)
                else:
                    early_start_time = max(early_start_time_s)   +random.randint(0,10)
                while True:

                    if self._is_resource_enough(candidate_activity, early_start_time, assigned_activities, self.total_resource):
                        candidate_activity.es = early_start_time
                        candidate_activity.ef = early_start_time + candidate_activity.duration
                        assigned_activities.append(candidate_activity)
                        unassigned_activities.remove(candidate_activity)
                        candidate_activities.remove(candidate_activity)
                        successors_ids = candidate_activity.successor
                        successors = self._get_activities_via_ids(successors_ids, project)
                        for successor in successors:
                            if successor in assigned_activities:
                                successors.remove(successor)
                            if set(self._get_activities_via_ids( successor.predecessor,project)).intersection(unassigned_activities):
                                successors.remove(successor)
                        candidate_activities = candidate_activities + successors
                        if len(candidate_activities) > 1:
                            for a in candidate_activities:
                                if a.id == len(project):
                                    candidate_activities.remove(a)
                        break
                    else:
                        early_start_time+=1

            activities_info = []
            for i in assigned_activities:
                activity_info=[i.id,i.es,i.es+i.duration]
                activities_info.append(activity_info)
            population.append(activities_info)
        return population

    def pmx_cross(self,population:list):
        population_crossed=[]
        population=copy.deepcopy(population)
        total_resource=self.total_resource

        while len(population_crossed)<=len(population):
            parent=random.sample(population,2)
            parent1=parent[0]
            parent2=parent[1]
            child1,child2=self._pmx_cross(parent1,parent2)
            count1=0
            count2=0
            child1_project=self.decode(child1,self.project)
            child2_project=self.decode(child2,self.project)
            # 交叉算子似乎还有问题
            flag1=True
            flag2=True
            while (not self._is_resource_enough_for_entire_project(child1,total_resource)) or (self._checkIfDuplicates(child1)) or ( not self._all_activity_is_valid(child1_project)):
                child1, temp = self._pmx_cross(parent1, parent2)  # 多次迭代，保证子代满足资源需求
                count1+=1

                if count1>10:
                    flag1=False
                    break
            while (not self._is_resource_enough_for_entire_project(child2,total_resource)) or (self._checkIfDuplicates(child2))  or ( not self._all_activity_is_valid(child2_project)):
                temp,child2=self._pmx_cross(parent1, parent2)
                count2+=1
                if count2>10:
                    flag2 = False
                    break

            if flag1 and flag2:
                population_crossed.append(child1)
                population_crossed.append(child2)

        return population_crossed
    def mutate(self,population,mutation_rate):
        population_mutated=[]
        for child in population:
            child_mutated = self._mutate(child,mutation_rate)
            population_mutated.append(child_mutated)
        return population_mutated
    def sum_fitness_population(self,population):
        sum=0
        for parent in population:
            sum+=self.fitness_parent(parent)
        return sum
    def fitness_parent(self,parent):
        parent.sort(key=lambda x:x[2])
        return 1/(parent[-1][2])  # 选每个child的最后一项任务的最早结束时间的倒数做为适应度
    def encode(self,project:dict):

        activities_info = []
        for values in project.values():
            activity_info=[values.id,values.es,values.es+values.duration]
            activities_info.append(activity_info)
        activities_info.sort(key=lambda x:x[2])
        return activities_info
    def decode(self,activities_info:list,project:dict):
        for a in activities_info:
            project[a[0]].es=a[1]
            project[a[0]].ef=a[2]
            # project[a[0]].ef=a[1]+project[a[0]].duration
        return project
    def _select(self,parent1,parent2):
        pass
    def _mutate(self,child,mutation_rate):
        child_copy=copy.deepcopy(child)
        if not self._can_mutate(child):
            # print("不能变异了")
            return child_copy
        if mutation_rate > random.random():
            gene_index_s = [x+1 for x in range(len(child_copy)-1 )]
            while True:
                gene_index=random.sample(gene_index_s,1)[0]
                child_copy[gene_index][1]-=1
                child_copy[gene_index][2]-=1
                project_child = self.decode(child_copy, self.project)
                if  not self._is_resource_enough_for_entire_project(child_copy,self.total_resource) \
                    or  not self._is_slower_than_predecessor(self._get_activity_via_id(child_copy[gene_index][0],project_child),project_child)\
                    :
                    child_copy[gene_index][1] += 1
                    child_copy[gene_index][2] += 1
                    gene_index_s.remove(gene_index)
                else:
                    break
                # activity = self._get_activity_via_id(child_copy[gene_index][0], project_child)
                # predecessor_id = activity.predecessor
                # predecessor = self._get_activities_via_ids(predecessor_id, project_child)
                # alist = [x.es + x.duration for x in predecessor]

                # if activity.id==7:
                #     print("es：" + str(activity.es) + "紧前最大" + str(alist))
        return child_copy
    def _can_mutate(self,child):
        child_copy=copy.deepcopy(child)
        for i in [x+1 for x in range(len(child_copy)-1)]:
            gene_index=i
            child_copy[gene_index][1]-=1
            child_copy[gene_index][2]-=1
            project_child = self.decode(child_copy, self.project)
            if   self._is_resource_enough_for_entire_project(child_copy,self.total_resource) \
                and   self._is_slower_than_predecessor(self._get_activity_via_id(child_copy[gene_index][0],project_child),project_child)\
                :
                return True
            else:
                child_copy[gene_index][1] += 1
                child_copy[gene_index][2] += 1
                continue
        return False
    def _pmx_cross(self,parent1, parent2):
        """
        使用PMX算子对两个染色体进行交叉操作
        """
        # 随机选择交叉区域
        start,end=sorted(random.sample([x for x in range(1,len(parent1)-1)],2))
        # 将父代1中交叉区域的基因复制到子代1和2中
        child1 = parent1[:start] + parent2[start:end+1] + parent1[end+1:]
        child2 = parent2[:start] + parent1[start:end+1] + parent2[end+1:]
        # 处理重复的基因
        non_cross_gene_child1=child1[:start]+child1[end+1:]
        cross_gene_child1=child1[start:end+1]
        for i in range(start, end+1):
            if parent1[i] not in child1:
                indexs=[ii for ii, x in enumerate(child1) if x[0] == parent2[i][0]]
                try:
                    index = [ii for ii in indexs if ii not in range(start, end + 1)][0]  # 选择索引是 不在交叉区域的基因的索引
                    child1[index] = parent1[i]

                except:
                    continue

        non_cross_gene_child2=child2[:start]+child2[end+1:]
        cross_gene_child2=child2[start:end+1]
        for i in range(start, end+1):
            if parent2[i] not in child2:
                indexs = [ii for ii, x in enumerate(child2) if x[0] == parent1[i][0]]
                try:

                    index=[ii for ii in indexs if ii not in range(start,end+1)][0]
                    child2[index]=parent2[i]
                except:
                    continue


        return child1, child2
    def _is_resource_enough(self,candidate_activity, early_start_time, assigned_activities, total_resources):
        """
        判断如果把candidate_activity插入到某一个时间段以后了，能否满足该时间段的资源限量要求
        :param candidate_activity:
        :param early_start_time:
        :param assigned_activities:
        :param total_resources:
        :return:
        """
        t = early_start_time + 1
        while t <= early_start_time + candidate_activity.duration:
            sum_resource = np.zeros(len(total_resources))
            for assigned_activity in assigned_activities:
                if assigned_activity.es + 1 <= t <= assigned_activity.es + assigned_activity.duration:
                    sum_resource += assigned_activity.resourceRequest
            sum_resource += candidate_activity.resourceRequest
            if (sum_resource > total_resources).any():
                return False
            t += 1

        return True
    def _get_activities_via_ids(self,ids: list, activities: dict):
        '''
        通过活动的id的集合ids获得活动对象的集合
        :param ids:
        :param project:
        :return:
        '''
        activities_wanted = []
        for i in ids:
            activities_wanted.append(activities[i])
        return activities_wanted
    def _get_activity_via_id(self,id, activities: dict):
        '''
        通过活动的id获得活动对象
        :param ids:
        :param project:
        :return:
        '''
        return activities[id]
    def _is_slower_than_predecessor(self,activity,project:dict):
        if activity.predecessor==None or activity.predecessor==[]:
            return True
        predecessor_id=activity.predecessor
        predecessor=self._get_activities_via_ids(predecessor_id,project)
        alist=[x.es+x.duration for x in predecessor]
        # if len(alist):
        #     return False
        max_time=max(alist)
        # if activity.id==8:
        #     print("es："+str(activity.es)+"紧前最大"+str(alist))
        #


        if activity.es >= max_time:
            return True
        else:
            return False
    def _all_activity_is_valid(self,project:dict):
        project=copy.deepcopy(project)
        for activity in project.values():
            if activity.id==1:
                continue
            if self._is_slower_than_predecessor(activity,project):
                continue
            else:
                return False
        return True
    def _is_resource_enough_for_entire_project(self,project, total_resources):
        """
        判断整个项目是否满足资源限量需求
        :param candidate_activity:
        :param early_start_time:
        :param assigned_activities:
        :param total_resources:
        :return:
        """

        for activity in project:
            t = activity[1] + 1
            while t <= activity[2]:
                sum_resource = np.zeros(len(total_resources))
                if activity[0] != 1:
                    for before_activity in project[:project.index(activity)]:
                        if before_activity[1] + 1 <= t <= before_activity[2]:
                            sum_resource += self.project[before_activity[0]].resourceRequest
                    sum_resource += self.project[activity[0]].resourceRequest
                    if (sum_resource > total_resources).any():
                        return False
                    t += 1

        return True
    def _checkIfDuplicates(self,test_list):
        """
        检查列表里是否有相同的任务
        :param test_list:
        :return:
        """
        for i, x in enumerate(test_list):
            for j, y in enumerate(test_list):
                if i != j and x[0] == y[0]:
                    return True
        return False
    @staticmethod
    def is_resource_enough_for_entire_project_staticmethod(activities:dict,project:list, total_resources):
        """
        判断整个项目是否满足资源限量需求
        :param activities:
        :param project:
        :param total_resources:
        :return:
        """
        for activity in project:
            t = activity[1] + 1
            while t <= activity[2]:
                sum_resource = np.zeros(len(total_resources))
                if project.index(activity) != 0:
                    for before_activity in project[:project.index(activity)]:
                        if before_activity[1] + 1 <= t <= before_activity[2]:
                            sum_resource +=activities[before_activity[0]].resourceRequest
                    sum_resource += activities[activity[0]].resourceRequest
                    if (sum_resource > total_resources).any():
                        return False
                    t += 1

        return True
    @staticmethod
    def checkIfDuplicates_staticmethod(test_list):
        for i, x in enumerate(test_list):
            for j, y in enumerate(test_list):
                if i != j and x[0] == y[0]:
                    return True
        return False

def read_data_from_RCP_file(file_name):
    '''
    读取标准化文件中的所有活动信息，包括  1.活动数   2.项目资源数 3.项目资源种类数   4.项目资源限量
    5.所有活动的ID，持续时间，资源需求，紧前活动
    :param fileName:
    :return: 标准化文件数据
    '''
    f = open(file_name)
    taskAndResourceType = f.readline().split('      ')  # 第一行数据包含活动数和资源数
    num_activities = int(taskAndResourceType[0])  # 得到活动数
    num_resource_type = int(taskAndResourceType[1])  # 得到资源数
    total_resource = np.array([int(value) for value in f.readline().split('      ')[:-1]])  # 获取资源限量
    # 将每个活动的所有信息存入到对应的Activity对象中去
    activities = {}
    preActDict = defaultdict(lambda: [])
    for i in range(num_activities):
        nextLine = [int(value) for value in f.readline().split('      ')[:-1]]
        task = Activity(i + 1, nextLine[0], nextLine[1:5], nextLine[6:])
        activities[task.id] = task
        for act in nextLine[6:]:
            preActDict[act].append(i + 1)
    f.close()
    # 给每个活动加上紧前活动信息
    for actKey in activities.keys():
        activities[actKey].predecessor = preActDict[activities[actKey].id].copy()
    return num_activities, num_resource_type, total_resource, activities  # 活动数int， 资源数int， 资源限量np.array， 所有活动集合dic{活动代号：活动对象}


if __name__ == "__main__":
    # 0、首先在这个网站上下载数据集：https://www.projectmanagement.ugent.be/research/data，下载“RCPLIB.zip”文件
    # 我用的是RCPLIB\DC\DC1\mv1.rcp这个目录下的文件，所以大家测试代码的时候也尽量用这个，其他的文件可能因为字符串格式问题
    # 会让我的代码失效，我粗略看了下，似乎mv1.rcp-mv9.rcp之间的文件大部分能用。
    file_name = r"RCPLIB\DC\DC1\mv1.rcp"
    # 1、从rcp文件中读取数据，得到活动个数，资源种类数，各个资源的限量np.array，所有活动的集合dict{活动id：活动对象}
    num_activities, num_resource_type, total_resource, activities = read_data_from_RCP_file(file_name)
    # 2、遗传算法初始化
    ga=Genetic_Algorithms(activities,total_resource)
    # 3、种群初始化
    population=ga.initialize_population(100)  # 尽量偶数个个体
    num_offsprings=len(population)
    def f(population,n,num_offsprings):
        fitness=[]
        for i in range(n):
            sum_fitness_population = ga.sum_fitness_population(population)
            # print("交叉前的适应度："+str(sum_fitness_population))
            population_not_for_cross=[]
            tournament_size = 2  # 比赛的个体数量
            num_offsprings = num_offsprings  # 选择的下一代的数量
            population_for_cross=[]  # 存储选择出的下一代的父母
            fitness_s=[ga.fitness_parent(parent) for parent in population]
            fitness_s.sort(reverse=True)
            while len(population_for_cross) < num_offsprings-1:
                # 在种群中随机选择tournament_size个个体作为比赛的参与者
                parent1,parent2 = random.sample(population, tournament_size)
                # 从参与者中选择适应度最高的个体作为下一代的父母
                if ga.fitness_parent(parent1)/sum_fitness_population > ga.fitness_parent(parent2)/sum_fitness_population:
                    population_for_cross.append(parent1)
                else:
                    population_for_cross.append(parent2)
            population_crossed=ga.pmx_cross(population_for_cross)

            population_for_mutate=population_crossed
            population_mutated=ga.mutate(population_for_mutate,0.3)
            population=population_mutated
            # print("变异后总适应度值："+str(ga.sum_fitness_population(population)))
            fitness.append(ga.sum_fitness_population(population))
            print("迭代了"+str(i+1)+"次")
        return population,fitness
    # 4、迭代计算
    population,fitness=f(population,500,num_offsprings)
    # 5、绘制适应度函数值的图像
    print("最小工期为："+str(population[-1][-1][2]))
    plt.plot([x for x in range(fitness.__len__())],fitness)
    plt.ylabel('fitness')
    plt.xlabel('num_iteration')
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.show()
    child=population[0]
    child_project=ga.decode(child,activities)
    # print("子代种群第一个")
    # print(population[0])
    project=ga.decode(population[0],activities)


    # 6、最终子代的展示
    for child in population:
        # print("child{}的适应度为：".format(population.index(child)+1) + str(ga.fitness_parent(child)))
        print(child)
