# import time
#
#
# class Test():
#     a = 1
#     b = 2
#
#     def __init__(self, a, b):
#         self.a = a
#         self.b = b
#
#     # 实例方法
#     def ix_method(self):
#         print(self.a + self.b)
#
#     # 静态方法，是类的一种逻辑，经过staticmethod修饰过的类方法无需实例化即可被调用，参数随意，没有“self”和“cls”参数
#     @staticmethod
#     def static_method():
#         print(time.localtime())
#
#     # 第一个参数必须是当前类对象，该参数名一般约定为“cls”，通过它来传递类的属性和方法（不能传实例的属性和方法）
#     # 原则上，类方法是将类本身作为对象进行操作的方法。假设有个方法，且这个方法在逻辑上采用类本身作为对象来调用更合理，
#     # 那么这个方法就可以定义为类方法。另外，如果需要继承，也可以定义为类方法
#     @classmethod
#     def class_method(cls):
#         pass
#     # 子类会影响父类
#     # 实例对象和类对象都可以调用
#
#
# # 实例方法可以用实例和类调用，但是类调用的时候也需要实例化
# demo_one = Test(3, 5)
# demo_one.ix_method()
# Test.ix_method(demo_one)
#
# # 静态方法，实例和类都可以调用
# demo_one.static_method()
# Test.static_method()

a = ['2', '3', '4', '5', '6', '7', '8', '9']
b = [1, 2, 3, 4, 5, 6, 7, 8, ]
d = {key: value for (key, value) in a, b}
print(d)
