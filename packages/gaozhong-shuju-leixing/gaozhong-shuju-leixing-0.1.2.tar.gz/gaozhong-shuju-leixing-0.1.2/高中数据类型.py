from collections import deque

class 队列:
    def __init__(self):
        # 使用双端队列来实现队列
        self.队列容器 = deque()

    def 入队(self, 元素):
        # 添加元素到队列的尾部
        self.队列容器.append(元素)

    def 出队(self):
        # 从队列的头部移除元素并返回
        if self.是否为空():
            raise IndexError("尝试从空队列出队")
        return self.队列容器.popleft()

    def 是否为空(self):
        # 检查队列是否为空
        return len(self.队列容器) == 0

    def 大小(self):
        # 返回队列中元素的个数
        return len(self.队列容器)

    def 查看队首(self):
        # 返回队列头部的元素，不移除
        if self.是否为空():
            raise IndexError("尝试从空队列查看队首")
        return self.队列容器[0]
class 栈:
    def __init__(self):
        # 使用列表来实现栈
        self.栈容器 = []

    def 入栈(self, 元素):
        # 将元素添加到栈的顶部
        self.栈容器.append(元素)

    def 出栈(self):
        # 移除并返回栈顶的元素
        if self.是否为空():
            raise IndexError("尝试从空栈出栈")
        return self.栈容器.pop()

    def 是否为空(self):
        # 检查栈是否为空
        return len(self.栈容器) == 0

    def 大小(self):
        # 返回栈中元素的个数
        return len(self.栈容器)

    def 查看栈顶(self):
        # 返回栈顶的元素，不移除
        if self.是否为空():
            raise IndexError("尝试查看空栈的栈顶")
        return self.栈容器[-1]
class 节点:
    def __init__(self, 数据=None):
        self.数据 = 数据
        self.下一个 = None

class 链表:
    def __init__(self):
        self.头 = None

    def 添加到尾部(self, 数据):
        新节点 = 节点(数据)
        if self.头 is None:
            self.头 = 新节点
        else:
            当前 = self.头
            while 当前.下一个:
                当前 = 当前.下一个
            当前.下一个 = 新节点

    def 打印链表(self):
        当前 = self.头
        while 当前:
            print(当前.数据, end=" -> ")
            当前 = 当前.下一个
        print("None")

    def 查找(self, 数据):
        当前 = self.头
        while 当前:
            if 当前.数据 == 数据:
                return 当前
            当前 = 当前.下一个
        return None

    def 删除节点(self, 数据):
        当前 = self.头
        前一个 = None
        while 当前:
            if 当前.数据 == 数据:
                if 前一个:
                    前一个.下一个 = 当前.下一个
                else:
                    self.头 = 当前.下一个
                return True
            前一个 = 当前
            当前 = 当前.下一个
        return False
class 双向节点:
    def __init__(self, 数据=None):
        self.数据 = 数据
        self.上一个 = None
        self.下一个 = None

class 双向链表:
    def __init__(self):
        self.头 = None
        self.尾 = None

    def 添加到尾部(self, 数据):
        新节点 = 双向节点(数据)
        if self.头 is None:
            self.头 = 新节点
            self.尾 = 新节点
        else:
            self.尾.下一个 = 新节点
            新节点.上一个 = self.尾
            self.尾 = 新节点

    def 打印链表(self):
        当前 = self.头
        while 当前:
            print(当前.数据, end=" <-> ")
            当前 = 当前.下一个
        print("None")
class 循环队列:
    def __init__(self, 大小):
        self.队列容器 = [None] * 大小
        self.头 = 0
        self.尾 = 0
        self.容量 = 大小
        self.计数 = 0

    def 入队(self, 元素):
        if self.计数 == self.容量:
            raise OverflowError("队列已满")
        self.队列容器[self.尾] = 元素
        self.尾 = (self.尾 + 1) % self.容量
        self.计数 += 1

    def 出队(self):
        if self.计数 == 0:
            raise IndexError("队列为空")
        元素 = self.队列容器[self.头]
        self.头 = (self.头 + 1) % self.容量
        self.计数 -= 1
        return 元素

    def 是否为空(self):
        return self.计数 == 0

    def 是否为满(self):
        return self.计数 == self.容量
class 二叉树节点:
    def __init__(self, 数据):
        self.数据 = 数据
        self.左 = None
        self.右 = None

class 二叉树:
    def __init__(self):
        self.根 = None

    def 插入(self, 数据):
        if self.根 is None:
            self.根 = 二叉树节点(数据)
        else:
            self._插入递归(self.根, 数据)

    def _插入递归(self, 当前节点, 数据):
        if 数据 < 当前节点.数据:
            if 当前节点.左 is None:
                当前节点.左 = 二叉树节点(数据)
            else:
                self._插入递归(当前节点.左, 数据)
        else:
            if 当前节点.右 is None:
                当前节点.右 = 二叉树节点(数据)
            else:
                self._插入递归(当前节点.右, 数据)

    def 中序遍历(self, 节点):
        if 节点:
            self.中序遍历(节点.左)
            print(节点.数据, end=" ")
            self.中序遍历(节点.右)

# 示例用法
if __name__ == "__main__":
    链表实例 = 链表()
    链表实例.添加到尾部(1)
    链表实例.添加到尾部(2)
    链表实例.添加到尾部(3)
    链表实例.打印链表()  # 输出: 1 -> 2 -> 3 -> None

    print("查找 2:", 链表实例.查找(2) is not None)  # 输出: 查找 2: True
    链表实例.删除节点(2)
    链表实例.打印链表()  # 输出: 1 -> 3 -> None

# 示例用法
if __name__ == "__main__":
    s = 栈()
    s.入栈(1)
    s.入栈(2)
    s.入栈(3)
    print("栈大小:", s.大小())  # 输出: 栈大小: 3
    print("栈顶元素:", s.查看栈顶())  # 输出: 栈顶元素: 3
    print("出栈元素:", s.出栈())  # 输出: 出栈元素: 3
    print("出栈后栈大小:", s.大小())  # 输出: 出栈后栈大小: 2

# 示例用法
if __name__ == "__main__":
    q = 队列()
    q.入队(1)
    q.入队(2)
    q.入队(3)
    print("队列大小:", q.大小())  # 输出: 队列大小: 3
    print("队首元素:", q.查看队首())  # 输出: 队首元素: 1
    print("出队元素:", q.出队())  # 输出: 出队元素: 1
    print("出队后队列大小:", q.大小())  # 输出: 出队后队列大小: 2
if __name__ == "__main__":
    任务列表 = 双向链表()
    任务列表.添加到尾部("任务1")
    任务列表.添加到尾部("任务2")
    任务列表.添加到尾部("任务3")

    print("双向链表内容:")
    任务列表.打印链表()  # 输出: 任务1 <-> 任务2 <-> 任务3 <-> None
if __name__ == "__main__":
    饮水机 = 循环队列(3)

    try:
        饮水机.入队("空瓶子1")
        饮水机.入队("空瓶子2")
        饮水机.入队("空瓶子3")
        print("饮水机是否已满:", 饮水机.是否为满())  # 输出: True

        print("取出空瓶子:", 饮水机.出队())  # 输出: 空瓶子1
        print("饮水机是否已满:", 饮水机.是否为满())  # 输出: False

        饮水机.入队("空瓶子4")
        print("饮水机是否已满:", 饮水机.是否为满())  # 输出: True
    except OverflowError as e:
        print(e)
if __name__ == "__main__":
    数字树 = 二叉树()
    数字树.插入(5)
    数字树.插入(3)
    数字树.插入(7)
    数字树.插入(2)
    数字树.插入(4)
    数字树.插入(6)
    数字树.插入(8)

    print("二叉树的中序遍历结果:")
    数字树.中序遍历(数字树.根)  # 输出: 2 3 4 5 6 7 8
