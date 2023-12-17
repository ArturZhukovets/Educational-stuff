"""
Example 1:

Input: x = 121
Output: true
Explanation: 121 reads as 121 from left to right and from right to left.
"""

class Solution:
    def isPalindrome(self, x: int) -> bool:
        r_l = str(x)[::-1]
        if r_l.endswith("-"):
            r_l = r_l.strip("-")
        if x == int(r_l):
            return True
        return False


class Solution2:
    def isPalindrome(self, x: int) -> bool:
        if x < 0:
            return False

        reversed_num = 0
        temp = x

        while temp != 0:
            digit = temp % 10
            reversed_num = reversed_num * 10 + digit
            temp //= 10

        return reversed_num == x

class Solution3:
    """
    Here we only iterate by a half of a number.
    The code avoids the need for reversing the entire number
    by comparing only the necessary parts.
    """
    def isPalindrome(self, x: int) -> bool:
        # if ends with 0
        if x < 0 or (x != 0 and x % 10 == 0):
            return False

        reversed_num = 0

        while x > reversed_num:
            reversed_num = reversed_num * 10 + x % 10
            x //= 10

        return x == reversed_num or x == reversed_num // 10

a = Solution3().isPalindrome(6262626)
print(a)
