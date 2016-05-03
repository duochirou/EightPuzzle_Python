import copy
import random
import time
import queue


class Node(object):
    def __init__(self, data, depth):
        Node.is_legal_data(data)
        self.data = data
        self.depth = depth

    def __eq__(self, other):
        return self.data == other.data and isinstance(other, Node)

    def __str__(self):
        s = '\n'.join("  ".join([str(self.data[row][column]) for column in range(len(self.data[row]))]) for row in range(len(self.data)))
        return "".join(["当前步数：{}\n".format(self.depth + 1), s])

    def __repr__(self):
        return '\n'.join("  ".join([str(self.data[row][column]) for column in range(len(self.data[row]))]) for row in range(len(self.data)))

    def __getitem__(self, item):
        return self.data[item]

    @classmethod
    def copy(cls, node):
        '''return a deep copy of self.data, self.depth'''
        return Node(copy.deepcopy(node.data), copy.deepcopy(node.depth))

    @classmethod
    def get_blank_position(cls, p_node):
        '''get the position of 0. range from (0, 0) to (2 , 2)'''
        for row in range(len(p_node.data)):
            for column in range(len(p_node.data[row])):
                if p_node.data[row][column] == 0:
                    return row, column

    @classmethod
    def is_legal_data(cls, data):
        '''check if the data is 2-dimension data'''
        temp_list = list()
        assert len(data) == 3
        for x in data:
            assert len(x) == 3
            for y in x:
                temp_list.append(y)
        temp_list.sort()
        assert temp_list == list(range(9))

    @classmethod
    def can_move(cls, p_node, direction_str):
        '''return if p_node can move to the specified direction
            U for up, D for down, L for left, R for right'''
        if direction_str == "U":
            return not Node.get_blank_position(p_node)[0] == 0
        elif direction_str == "D":
            return not Node.get_blank_position(p_node)[0] == 2
        elif direction_str == "L":
            return not Node.get_blank_position(p_node)[1] == 0
        elif direction_str == "R":
            return not Node.get_blank_position(p_node)[1] == 2
        else:
            SystemError("no such direction: {}".format(direction_str))

    @classmethod
    def move(cls, p_node, direction_str):
        '''move the blank of p_node to the specified direction
            U for up, D for down, L for left, R for right'''
        x, y = Node.get_blank_position(p_node)
        if direction_str == "U":
            p_node[x][y], p_node[x - 1][y] = p_node[x - 1][y], p_node[x][y]
        elif direction_str == "D":
            p_node[x][y], p_node[x + 1][y] = p_node[x + 1][y], p_node[x][y]
        elif direction_str == "L":
            p_node[x][y], p_node[x][y - 1] = p_node[x][y - 1], p_node[x][y]
        elif direction_str == "R":
            p_node[x][y], p_node[x][y + 1] = p_node[x][y + 1], p_node[x][y]
        else:
            SystemError("no such direction: {}".format(direction_str))

    @classmethod
    def random_node(cls, depth=0):
        '''generate random node, default depth = 0'''
        gen_list = list(range(9))
        target_data = []
        for i in range(3):
            temp = []
            for j in range(3):
                choice = random.choice(gen_list)
                temp.append(choice)
                gen_list.remove(choice)
            target_data.append(temp)
        return Node(target_data, depth)

    @classmethod
    def get_parity(cls, p_node):
        '''return the parity, false to odd, true to oven'''
        temp = []
        for row in range(len(p_node.data)):
            for column in range(len(p_node.data[row])):
                temp.append(p_node.data[row][column])
        temp.remove(0)
        parity_count = 0
        for i in range(len(temp)):
            for j in range(i):
                if temp[j] > temp[i]:
                    parity_count += 1
        return parity_count % 2 == 0

    @classmethod
    def heuristic_funtion(cls, p_node, target_node, factor_a=1, factor_b=1) -> int:
        '''return the value of F(x) = a*G(x) + b*H(x)
            where G(x) is the depth, a is factor,
            and H(x) is the expectation, b is factor'''
        counter = 0
        for row in range(len(p_node.data)):
            for column in range(len(p_node.data[row])):
                if not p_node.data[row][column] == target_node.data[row][column]:
                    counter += 1
        return factor_a * p_node.depth + factor_b * counter

    @classmethod
    def get_node_heuristic(cls, opened_list, target_node, factor_a, factor_b):
        '''get the best node from opened_list accroding to heuristic funtion'''
        best_node_index = 0
        best_node_value = Node.heuristic_funtion(opened_list[0][1], target_node, factor_a, factor_b)
        for i in range(1, len(opened_list)):
            if opened_list[i][0] is None:
                temp_value = Node.heuristic_funtion(opened_list[i][1], target_node, factor_a, factor_b)
                opened_list[i][0] = temp_value
            else:
                temp_value = opened_list[i][0]
            if best_node_value >= temp_value:
                best_node_index = i
                best_node_value = temp_value
        return opened_list.pop(best_node_index)[1]


class NodeUtils(object):
    '''some utils about the node'''

    @classmethod
    def show_resolve_path(cls, final_node):
        '''show the path from start to final'''
        cursor = final_node
        temp = []
        while hasattr(cursor, "prev"):
            temp.append(cursor)
            cursor = cursor.prev
        temp.append(cursor)
        while not len(temp) == 0:
            yield temp.pop()

    @classmethod
    def show_bidirection_resolve_path(cls, result):
        '''show_result path for bi-direction search'''
        cursor = result[0]
        temp = []
        while hasattr(cursor, "prev"):
            temp.append(cursor)
            cursor = cursor.prev
        temp.append(cursor)
        cursor = result[1]
        if not hasattr(cursor, "next"):
            pass  # 如果已经是最后一个节点了，就没有必要再加上了，因为 startpoint 与 endpoint 一定是相等的
        else:
            cursor = cursor.next  # 消耗重复的startpoint与endpoint
            while hasattr(cursor, "next"):
                temp.insert(0, cursor)
                cursor = cursor.next
            temp.insert(0, cursor)
        # # 修改错误的深度数据
        # for i in range(len(temp) - 1, 0, -1):
        #     if temp[i - 1].depth - temp[i].depth == 1:  # 正常数据
        #         pass
        #     else:  # 非正常数据
        #         temp[i - 1].depth = temp[i].depth + 1

        while len(temp) != 0:
            yield temp.pop()


def depth_first_search(p_startpoint, p_endpoint):
    '''depth first search'''
    # 深拷贝
    startpoint = copy.deepcopy(p_startpoint)
    endpoint = copy.deepcopy(p_endpoint)
    # 检查奇偶性
    if not Node.get_parity(startpoint) == Node.get_parity(endpoint):
        return list()
    # 数据结构初始化
    searched_nodes = []  # search history
    to_search_stack = [startpoint, ]  # init the search stack
    # 开始搜索
    while len(to_search_stack) != 0:
        # 取出待分析节点
        current_node = to_search_stack.pop()
        # 分析节点, 如果是目标节点则结束搜索
        if current_node == endpoint:
            return list(NodeUtils.show_resolve_path(current_node))
        # 如果不是目标节点，存入搜索历史
        searched_nodes.append(current_node)
        # 如果未达到target节点，尝试深度优先搜索
        for direction_str in ["U", "D", "L", "R"]:
            if Node.can_move(current_node, direction_str):
                new_node = Node.copy(current_node)
                Node.move(new_node, direction_str)
                if new_node not in searched_nodes:
                    to_search_stack.append(new_node)
                new_node.depth += 1
                new_node.prev = current_node
    # 搜索不到时返回空列表
    return list()


def width_first_search(p_startpoint, p_endpoint):
    '''width first search'''
    # 深拷贝
    startpoint = copy.deepcopy(p_startpoint)
    endpoint = copy.deepcopy(p_endpoint)
    # 检查奇偶性
    if not Node.get_parity(startpoint) == Node.get_parity(endpoint):
        return list()
    # 数据结构初始化
    searched_nodes = []
    to_search_queue = queue.Queue()
    to_search_queue.put(startpoint)
    # 开始搜索
    while not to_search_queue.empty():
        # 取出待分析节点，并输出信息
        current_node = to_search_queue.get()
        # 分析节点, 如果是目标节点则结束搜索
        if current_node == endpoint:
            return list(NodeUtils.show_resolve_path(current_node))
        # 如果不是目标节点，存入搜索历史
        searched_nodes.append(current_node)
        # 如果未达到target节点，尝试宽度优先搜索
        for direction_str in ["U", "D", "L", "R"]:
            if Node.can_move(current_node, direction_str):
                new_node = Node.copy(current_node)
                Node.move(new_node, direction_str)
                if new_node not in searched_nodes:
                    to_search_queue.put(new_node)
                new_node.depth += 1
                new_node.prev = current_node
    # 搜索不到时返回空列表
    return list()


def heuristic_search(p_startpoint, p_endpoint, max_depth, factor_a=1, factor_b=1):
    # 深拷贝
    startpoint = copy.deepcopy(p_startpoint)
    endpoint = copy.deepcopy(p_endpoint)
    # 检查奇偶性
    if not Node.get_parity(startpoint) == Node.get_parity(endpoint):
        return list()
    # 数据结构初始化
    opened_nodes = [[None, startpoint], ]
    closed_nodes = []
    while True:
        current_node = Node.get_node_heuristic(opened_nodes, endpoint, factor_a, factor_b)
        # 分析节点, 如果是目标节点则结束搜索
        if current_node == endpoint:
            return list(NodeUtils.show_resolve_path(current_node))
        # 如果不是目标节点，存入搜索历史
        closed_nodes.append(current_node)
        # 拓展节点
        for direction_str in ["U", "D", "L", "R"]:
            if Node.can_move(current_node, direction_str):
                new_node = Node.copy(current_node)
                Node.move(new_node, direction_str)
                if new_node not in closed_nodes:
                    opened_nodes.append([None, new_node])
                new_node.depth += 1
                new_node.prev = current_node
    # 搜索不到时返回空列表
    return list()


def bi_direction_width_search(p_startpoint, p_endpoint):
    '''bi-direction width first search'''
    # 深拷贝
    startpoint = copy.deepcopy(p_startpoint)
    endpoint = copy.deepcopy(p_endpoint)
    # 检查奇偶性
    if not Node.get_parity(startpoint) == Node.get_parity(endpoint):
        return list()
    # 数据结构初始化
    searched_nodes_1, searched_nodes_2 = [], []
    to_search_queue_1 = queue.Queue()
    to_search_queue_1.put(startpoint)
    to_search_queue_2 = queue.Queue()
    to_search_queue_2.put(endpoint)
    # 开始搜索
    while not (to_search_queue_1.empty() or to_search_queue_2.empty()):
        # 从正向取出待分析节点
        current_node_1 = to_search_queue_1.get()
        # 如果待分析节点在正向搜索的队列中,返回中间两个结尾值
        if current_node_1 in searched_nodes_2:
            result = [current_node_1, searched_nodes_2[searched_nodes_2.index(current_node_1)]]
            return list(NodeUtils.show_bidirection_resolve_path(result))
        # 由于接下来的确认，所以如果不是目标值，待分析节点一定不在自己已搜索的节点中，尝试宽度优先搜索，并加入历史记录
        searched_nodes_1.append(current_node_1)
        for direction_str in ["U", "D", "L", "R"]:
            if Node.can_move(current_node_1, direction_str):
                new_node = Node.copy(current_node_1)
                Node.move(new_node, direction_str)
                if new_node not in searched_nodes_1:
                    to_search_queue_1.put(new_node)
                new_node.depth += 1
                new_node.prev = current_node_1

        # 从反向取出待分析节点
        current_node_2 = to_search_queue_2.get()
        # print("current_node_1 quchu" + str(current_node_1))  # debug
        # 如果待分析节点在正向搜索的队列中,返回中间两个结尾值
        if current_node_2 in searched_nodes_1:
            result = [searched_nodes_1[searched_nodes_1.index(current_node_2)], current_node_2]
            return list(NodeUtils.show_bidirection_resolve_path(result))
        # 由于接下来的确认，所以如果不是目标值，待分析节点一定不在自己已搜索的节点中，尝试宽度优先搜索，并加入历史记录
        searched_nodes_2.append(current_node_2)
        for direction_str in ["U", "D", "L", "R"]:
            if Node.can_move(current_node_2, direction_str):
                new_node = Node.copy(current_node_2)
                Node.move(new_node, direction_str)
                if new_node not in searched_nodes_2:
                    to_search_queue_2.put(new_node)
                new_node.depth -= 1
                new_node.next = current_node_2
    # 搜索不到时返回空列表
    return list()


def main():
    # 指定生成节点
    # startpoint = Node([
    #     [1, 2, 3],
    #     [4, 0, 5],
    #     [6, 7, 8],
    # ], 0)
    # endpoint = Node([
    #     [2, 3, 5],
    #     [0, 7, 8],
    #     [1, 4, 6],
    # ], 0)

    # 随机生成有效节点
    while True:
        startpoint = Node.random_node()
        endpoint = Node.random_node()
        if Node.get_parity(startpoint) == Node.get_parity(endpoint):
            break

    # 输出初始节点信息
    print('起始状态: \n{}'.format(startpoint.__repr__()))
    print('结束状态: \n{}'.format(endpoint.__repr__()))

    # # 深度优先
    # t1 = time.time()
    # result_list = depth_first_search(startpoint, endpoint)
    # if result_list:
    #     print('[depth first search] result found in {:.3}s.'.format(time.time() - t1))
    #     print('\tpath:')
    #     for x in result_list:
    #         print('\t' + str(x))
    # else:
    #     print('no solution!')


    # 宽度优先
    # t1 = time.time()
    # result_list = width_first_search(startpoint, endpoint)
    # if result_list:
    #     print('[width first search] result found in {:.3}s.'.format(time.time() - t1))
    #     print('\tpath:')
    #     for x in result_list:
    #         print('\t' + str(x))
    # else:
    #     print('no solution!')

    # 双向宽度优先
    # t1 = time.time()
    # result_list = bi_direction_width_search(startpoint, endpoint)
    # if result_list:
    #     print('[bi-direction width first search] result found in {:.3}s.'.format(time.time() - t1))
    #     print('path ({} steps):'.format(len(result_list)))
    #     for x in result_list:
    #         print(str(x))
    # else:
    #     print('no solution!')

    # 启发式搜索
    t1 = time.time()
    result_list = heuristic_search(startpoint, endpoint, max_depth=40, factor_a=1, factor_b=11)
    if result_list:
        print('[启发式搜索] 共耗时{:.3}s.'.format(time.time() - t1), end="")
        print('(共{}步):'.format(len(result_list)))
        for x in result_list:
            print(str(x))
    else:
        print('max depth reached. search failed.')


if __name__ == '__main__':
    main()
