# Definition for singly-linked list.
from itertools import zip_longest

class ListNode(object):
    def __init__(self, val=0, _next=None):
        self.val = val
        self.next = _next


# Solution 1

class Solution(object):

    def __init__(self):
        self.remainder = 0

    def sum_of_two_vals(self, val_1: int, val_2: int) -> int:
        res = (self.remainder + val_1 + val_2) % 10
        self.remainder = (self.remainder + val_1 + val_2) // 10
        return res

    def addTwoNumbers(self, l1: ListNode, l2: ListNode):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        val_1, val_2 = l1.val, l2.val
        result_list_node = ListNode(val=(self.sum_of_two_vals(val_1, val_2)))
        current_node = result_list_node

        while l1.next and l2.next:
            l1, l2 = l1.next, l2.next
            val_1, val_2 = l1.val, l2.val
            current_node.next = ListNode(val=self.sum_of_two_vals(val_1, val_2))
            current_node = current_node.next

        while l1.next:
            l1 = l1.next
            val_1 = l1.val
            current_node.next = ListNode(val=self.sum_of_two_vals(val_1, 0))
            current_node = current_node.next

        while l2.next:
            l2 = l2.next
            val_2 = l2.val
            current_node.next = ListNode(val=self.sum_of_two_vals(val_2, 0))
            current_node = current_node.next

        if self.remainder != 0:
            current_node.next = ListNode(val=self.remainder)

        return result_list_node


# Solution 2

class Solution2:

    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        dummyHead = ListNode(0)
        tail = dummyHead
        carry = 0

        while l1 is not None or l2 is not None or carry != 0:
            digit1 = l1.val if l1 is not None else 0
            digit2 = l2.val if l2 is not None else 0

            sum = digit1 + digit2 + carry
            digit = sum % 10
            carry = sum // 10

            newNode = ListNode(digit)
            tail.next = newNode
            tail = tail.next

            l1 = l1.next if l1 is not None else None
            l2 = l2.next if l2 is not None else None

        result = dummyHead.next
        dummyHead.next = None
        return result
