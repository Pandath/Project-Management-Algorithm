import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
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
def SSGS_via_total_float(project:dict, total_resource):
    all_activities=[value for value in project.values()]  # 所有的活动列表
    assigned_activities=[project[1]]  # 已经分配好的活动的列表
    unassigned_activities=all_activities.copy()  # 还没被分配好的活动的列表
    unassigned_activities.remove(project[1])
    candidate_activities=get_activities_via_ids(project[1].successor,project)  # 将要被分配的活动的列表
    while unassigned_activities:  # 当还没被分配好的活动的列表不为空时，就继续循环，直到把每个活动分配完成
        min_tf_activity=min(candidate_activities,key=lambda activity:activity.tf)  # 总时差最小的活动
        min_tf_activities = [x for x in candidate_activities
                             if x.tf == min_tf_activity.tf]  # 总时差最小的活动的集合
        min_duration_activity=min(min_tf_activities,key=lambda activity:activity.duration)  # 工期最小的活动
        min_duration_activities=[x for x in min_tf_activities if x.duration==min_duration_activity.duration]  # 最小的活动的集合
        min_id_activity=min(min_duration_activities,key=lambda activity:activity.id)  # id最小的那个活动
        candidate_activity=min_id_activity  # 当前正要被安排的活动

        """
        以下，选择candidate_activity的所有紧前活动的
        最早开始时间+活动工期的最大值作为candidate_activity的
        最早开始时间
        """
        early_start_time_s=[predecessor_candidate_activity.es+predecessor_candidate_activity.duration
                            for predecessor_candidate_activity in get_activities_via_ids(candidate_activity.predecessor,project)
                            if  predecessor_candidate_activity in assigned_activities]
        early_start_time=max(early_start_time_s)
        if is_resource_enough(candidate_activity,early_start_time,assigned_activities,total_resource):  # 判断这种选择是否满足资源限量
            candidate_activity.es=early_start_time
            candidate_activity.ef=early_start_time+candidate_activity.duration
            assigned_activities.append(candidate_activity)
            unassigned_activities.remove(candidate_activity)
            candidate_activities.remove(candidate_activity)
            successors_ids=candidate_activity.successor
            successors=get_activities_via_ids(successors_ids,project)
            for successor in successors:
                if successor in assigned_activities:
                    successors.remove(successor)
            candidate_activities=candidate_activities+successors
            if len(candidate_activities)>1:
                for a in candidate_activities:
                    if a.id==len(project):
                        candidate_activities.remove(a)
            continue
        else:  # 如果candidate_activity的所有紧前活动的最早完成时间都不满足要求，
               # 就从所有已经安排好的活动找，找这些活动的最早完成时间来作为candidate_activity的最早开始时间
            candidate_early_start_time=[assigned_activitity.es+assigned_activitity.duration
                                        for assigned_activitity in assigned_activities]
            candidate_early_start_time.sort()
            for time in candidate_early_start_time:
                if time > early_start_time:
                    early_start_time=time
                    if is_resource_enough(candidate_activity, early_start_time, assigned_activities,
                                          total_resource):
                        candidate_activity.es = early_start_time
                        candidate_activity.ef = early_start_time + candidate_activity.duration
                        assigned_activities.append(candidate_activity)
                        unassigned_activities.remove(candidate_activity)
                        candidate_activities.remove(candidate_activity)
                        # 根据candidate_activity的紧后活动生成新的candidate_activities，
                        # 同时避免选择那些已经被安排好的活动和最后一个虚活动（除非只剩下最后一个虚活动了）
                        successors_ids = candidate_activity.successor
                        successors = get_activities_via_ids(successors_ids, project)
                        for successor in successors:
                            if successor in assigned_activities:
                                successors.remove(successor)
                        candidate_activities = candidate_activities + successors
                        if len(candidate_activities) > 1:
                            for a in candidate_activities:
                                if a.id == len(project):
                                    candidate_activities.remove(a)
                        break


                    else:
                        continue
    return assigned_activities
def SSGS_via_duration(project:dict, total_resource):
    all_activities=[value for value in project.values()]  # 所有的活动列表
    assigned_activities=[project[1]]  # 已经分配好的活动的列表
    unassigned_activities=all_activities.copy()  # 还没被分配好的活动的列表
    unassigned_activities.remove(project[1])
    candidate_activities=get_activities_via_ids(project[1].successor,project)  # 将要被分配的活动的列表
    while unassigned_activities:  # 当还没被分配好的活动的列表不为空时，就继续循环，直到把每个活动分配完成
        min_duration_activity=min(candidate_activities,key=lambda activity:activity.duration)  # 优先工期最小的活动
        min_duration_activities=[x for x in candidate_activities if x.duration==min_duration_activity.duration]  # 工期最小的活动的集合
        min_id_activity=min(min_duration_activities,key=lambda activity:activity.id)  # 优先安排id最小的那个活动
        candidate_activity=min_id_activity  # 当前正要被安排的活动

        """
        以下，选择candidate_activity的所有紧前活动的
        最早开始时间+活动工期的最大值作为candidateActivity的
        最早开始时间
        """
        early_start_time_s=[predecessor_candidate_activity.es+predecessor_candidate_activity.duration
                            for predecessor_candidate_activity in get_activities_via_ids(candidate_activity.predecessor,project)
                            if  predecessor_candidate_activity in assigned_activities]
        early_start_time=max(early_start_time_s)
        if is_resource_enough(candidate_activity,early_start_time,assigned_activities,total_resource):
            candidate_activity.es=early_start_time
            candidate_activity.ef=early_start_time+candidate_activity.duration
            assigned_activities.append(candidate_activity)
            unassigned_activities.remove(candidate_activity)
            candidate_activities.remove(candidate_activity)
            successors_ids=candidate_activity.successor
            successors=get_activities_via_ids(successors_ids,project)
            for successor in successors:
                if successor in assigned_activities:
                    successors.remove(successor)
            candidate_activities=candidate_activities+successors
            if len(candidate_activities)>1:
                for a in candidate_activities:
                    if a.id==len(project):
                        candidate_activities.remove(a)
            continue
        else:

            candidate_early_start_time=[assigned_activitity.es+assigned_activitity.duration
                                        for assigned_activitity in assigned_activities]
            candidate_early_start_time.sort()
            for time in candidate_early_start_time:
                if time > early_start_time:
                    early_start_time=time
                    if is_resource_enough(candidate_activity, early_start_time, assigned_activities,
                                          total_resource):
                        candidate_activity.es = early_start_time
                        candidate_activity.ef = early_start_time + candidate_activity.duration
                        assigned_activities.append(candidate_activity)
                        unassigned_activities.remove(candidate_activity)
                        candidate_activities.remove(candidate_activity)
                        successors_ids = candidate_activity.successor
                        successors = get_activities_via_ids(successors_ids, project)
                        for successor in successors:
                            if successor in assigned_activities:
                                successors.remove(successor)
                        candidate_activities = candidate_activities + successors
                        if len(candidate_activities) > 1:
                            for a in candidate_activities:
                                if a.id == len(project):
                                    candidate_activities.remove(a)
                        break


                    else:
                        continue
    return assigned_activities
def get_activities_via_ids(ids:list,activities:dict):
    '''
    通过活动的id的集合ids获得活动对象的集合
    :param ids:
    :param project:
    :return:
    '''
    activities_wanted=[]
    for i in ids:
        activities_wanted.append(activities[i])
    return activities_wanted
def is_resource_enough(candidate_activity,early_start_time,assigned_activities,total_resources):
    """
    判断如果把candidate_activity插入到某一个时间段以后了，能否满足该时间段的资源限量要求
    :param candidate_activity:
    :param early_start_time:
    :param assigned_activities:
    :param total_resources:
    :return:
    """
    t=early_start_time+1
    while t<=early_start_time+candidate_activity.duration:
        sum_resource = np.zeros(len(total_resources))
        for assigned_activity in assigned_activities:
            if assigned_activity.es+1<=t<=assigned_activity.es+assigned_activity.duration:
                sum_resource+=assigned_activity.resourceRequest
        sum_resource+=candidate_activity.resourceRequest
        if(sum_resource>total_resources).any():
            return False
        t+=1

    return True
def preprocess_activities(activities):
    """
    处理一下活动集合activities，为了让集合中活动activity的successor和predecessor转换成为活动对象，而不再是活动对象的编号了，
    并对activities的格式做了下处理，方便后面计算各活动的总时差
    :param activities:
    :return:
    """
    for activity in activities.values():
        activity.successor=get_activities_via_ids(activity.successor,activities)
        activity.predecessor=get_activities_via_ids(activity.predecessor,activities)
    activities_processed={}
    for activity in activities.values():
        activity_info={}
        activity_info["duration"]=activity.duration
        activity_info["predecessors"]=activity.predecessor
        activity_info["successors"]=activity.successor
        activities_processed[activity]=activity_info
    return activities_processed
def calculate_activities_total_floats(activities):
    """
    计算活动集合activities中各个活动的总时差
    :param activities:
    :return:
    """

    earliest_start_times = {}
    earliest_finish_times = {}
    latest_start_times = {}
    latest_finish_times = {}

    # 计算最早开始时间和最早完成时间
    for activity in activities:
        if not activities[activity]['predecessors']:
            # 如果没有紧前活动，则最早开始时间为0
            earliest_start_times[activity] = 0
        else:
            # 否则，最早开始时间为所有紧前活动的最早完成时间中的最大值
            earliest_start_times[activity] = max([earliest_finish_times[p] for p in activities[activity]['predecessors']])
        earliest_finish_times[activity] = earliest_start_times[activity] + activities[activity]['duration']

    # 计算最晚开始时间和最晚完成时间
    for activity in reversed(list(activities.keys())):
        if not activities[activity]['successors']:
            # 如果没有紧后活动，则最晚完成时间为最早完成时间
            latest_finish_times[activity] = earliest_finish_times[activity]
        else:
            # 否则，最晚完成时间为所有紧后活动的最晚开始时间中的最小值
            latest_finish_times[activity] = min([latest_start_times[s] for s in activities[activity]['successors']])
        latest_start_times[activity] = latest_finish_times[activity] - activities[activity]['duration']

    # 计算总时差
    total_floats = {}
    for activity in activities:
        total_floats[activity] = latest_finish_times[activity] - earliest_finish_times[activity]

    return total_floats
def add_total_float_to_activities(activities):
    """
    把得到的活动的总时差添加到activities的各个活动中去
    :param activities:
    :return:
    """
    for i,j in zip(total_floats.keys(),total_floats.values()):
        activities[i.id].tf=j
    return activities
def deprocess_activities(activities):
    """
    把activities中各个活动的successor和predecessor转换成为活动对象的编号
    :param activities:
    :return:
    """
    for activity in activities.values():
        activity.successor=[activity.id for activity in activity.successor]
        activity.predecessor=[activity.id for activity in activity.predecessor]
    return activities

if __name__ == "__main__":
    # 0、首先在这个网站上下载数据集：https://www.projectmanagement.ugent.be/research/data，下载“RCPLIB.zip”文件
    # 我用的是RCPLIB\DC\DC1\mv1.rcp这个目录下的文件，所以大家测试代码的时候也尽量用这个，其他的文件可能因为字符串格式问题
    # 会让我的代码失效，我粗略看了下，似乎mv1.rcp-mv9.rcp之间的文件大部分能用。
    file_name = r"数据集\RCP格式\RCPLIB\DC\DC1\mv1.rcp"
    # 1、从rcp文件中读取数据，得到活动个数，资源种类数，各个资源的限量np.array，所有活动的集合dict{活动id：活动对象}
    num_activities, num_resource_type, total_resource, activities = read_data_from_RCP_file(file_name)
    # 2、预处理一下活动集合activities，为了让集合中活动activity的successor和predecessor转换成为活动对象，而不再是活动对象的编号了，
    # 并对activities的格式做了下处理，方便后面计算各活动的总时差
    activities_preprocessed = preprocess_activities(activities)
    # 3、计算各个活动的总时差
    total_floats= calculate_activities_total_floats(activities_preprocessed)
    # 4、把各个活动的总时差的值添加到activities的各个活动的ts属性中，也就是说ts属性就是用来储存活动的总时差的
    activities = add_total_float_to_activities(activities)
    # 5、把activities中各个活动的successor和predecessor转换成为活动对象的编号
    # ！！！其实重新写下serialGenerationScheme()方法,第2、5步完全可以避免的。处理过来，处理过去显得很愚蠢。但是我懒。
    activities = deprocess_activities(activities)
    # 6、以活动总时差大小=>活动工期大小=>活动序号大小的优先级对活动进行安排
    project1 = SSGS_via_total_float(activities, total_resource)
    # 7、以活动工期大小=>活动序号大小的优先级对活动进行安排
    project2 = SSGS_via_duration(activities, total_resource)
    # 8、画图
    project2.sort(key=lambda x:x.es)  # 按最早开始时间从小到大排个序

    Painter(project2,total_resource).draw_activities()
    # Painter(project1,total_resource).draw_activities2()












