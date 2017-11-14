from math import *
from operator import *


# Try 1: Using nodes - Not complete

OPERATIONS = {'+': add, '-': sub, '*': mul, '/': truediv}


class Node:
	def __init__(self, left_child=None, right_child=None, operation=None, value=None):
		self.left_child = left_child
		self.right_child = right_child
		self.operation = OPERATIONS.get(operation, None)
		self.is_evaluated = False
		self.value = value

	def __str__(self):
		if self.is_leaf():
			return str(self.value)
		return '(%s %s %s)' % (str(self.left_child), self.operation, str(self.right_child))

	def __repr__(self):
		if self.is_leaf():
			return str(self.value)
		return '(%s %s %s)' % (str(self.left_child), self.operation, str(self.right_child))

	def is_leaf(self):
		return self.left_child is None and self.right_child is None

	def _evaluate(self):
		if self.is_leaf():
			return self.value

		assert self.left_child is not None
		assert self.right_child is not None

		if self.operation is None:
			raise BaseException('Operation must be one of ' + str(OPERATIONS))

		self.value = self.operation(self.left_child.value, self.right_child.value)
		self.is_evaluated = True

	def clone(self):
		if self.is_leaf():
			return Node(operation=self.operation, value=self.value, left_child=None, right_child=None)

		return Node(operation=self.operation, value=self.value, left_child=self.left_child.clone(),
					right_child=self.right_child.clone())

	def leaves(self):
		if self.is_leaf():
			return [self]
		assert self.right_child is not None
		assert self.left_child is not None
		return [self] + self.left_child.leaves() + self.right_child.leaves()
	
	def dump_node(self):
		if self.is_leaf():
			return self.value
		d = {self.operation.__name__: {'left': None if self.left_child is None else self.left_child.dump_node(),
									   'right': None if self.right_child is None else self.right_child.dump_node()}}


def find_ex(nums, result):
	leaves_num = len(nums)
	trees = []
	build_operations_tree(leaves_num, None, trees)
	return trees


def build_operations_tree(leaves_num, root, trees):
	if leaves_num == 1:
		return Node()

	for i in range(1, ceil((1+leaves_num)/2)):
		left_leaves_num = leaves_num - i
		right_leaves_num = i
		
		for op in OPERATIONS:
			if root is None:
				my_root = Node(operation=op)
				trees.append(my_root)
				node = my_root
			else:
				my_root = root.clone()
				node = Node(operation=op)
			node.left_child = build_operations_tree(left_leaves_num, my_root, trees)
			node.right_child = build_operations_tree(right_leaves_num, my_root, trees)


def fill_nums(nums, tree):
	perms = permutations(nums)
	leaves = tree.leaves()
	for p in perms:
		for i in range(len(nums)):
			leaves[i].value = p[i]
		yield root.value(True)


def permutations(nums_list):
	def internal_permutations(nums, filled, index, permutations):
		if len(nums) == 0:
			permutations.append(list(filled))
			return
		cloned_nums = list(nums)
		for num in nums:
			filled[index] = num
			cloned_nums.remove(num)
			internal_permutations(cloned_nums, filled, index+1, permutations)
			cloned_nums = [num] + cloned_nums

	perms = []
	empty = [None]*len(nums_list)
	internal_permutations(nums_list, empty, 0, perms)
	return perms



############################################################################################################################
# Try 2 - Using Stack
############################################################################################################################

def find_math_exercise(nums, result):
	stack = list()
	for n in nums:
		stack.append(n)
		new_list = list(nums)
		new_list.remove(n)
		_find_math_exercise(new_list, stack, 0, result)
		stack.pop()


def _find_math_exercise(available_nums, stack, ops_num, result):
	if (ops_num > 0):
		for op in OPERATIONS:
			stack.append(op)
			_find_math_exercise(available_nums, stack, ops_num - 1, result)
			stack.pop()

	if len(available_nums) == 0:
		if ops_num == 0:
			ex = stack_to_math_exercise(list(stack))
			value = evaluate_stack(list(stack))
			if value is not None and abs(value, result) < 0.0001:
				print(ex)
			return
	else:
		for n in available_nums:
			stack.append(n)
			new_list = list(available_nums)
			new_list.remove(n)
			_find_math_exercise(new_list, stack, ops_num+1, result)
			stack.pop()


def stack_to_math_exercise(stack):
	if len(stack) == 0:
		raise BaseException("Error size 0")
	top = stack.pop()
	if isinstance(top, int) or isinstance(top, float):
		return str(top)
	elif isinstance(top, str):
		left = stack_to_math_exercise(stack)
		right = stack_to_math_exercise(stack)
		return "( {l} {o} {r} )".format(l=left, o=top, r=right)
	else:
		raise BaseException("Unknown element %s %s")


def evaluate_stack(stack):
	if len(stack) == 0:
		raise BaseException("Error size 0")
	top = stack.pop()
	if isinstance(top, int) or isinstance(top, float):
		return top
	elif isinstance(top, str):
		left = evaluate_stack(stack)
		right = evaluate_stack(stack)
		operation = OPERATIONS[top]
		if left is None or right is None or (top=='/' and right==0):
			return None
		return operation(left, right)
	else:
		raise BaseException("Unknown element %s" % str(top))


def clone(stack):
	return list(list(stack))


def abs(a, b):
	return a-b if a >= b else b-a