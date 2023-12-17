"""
Input: s = "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3.
"""

class Solution:
    """
    Use slight window algorithm.
    create 2 pointers and move left pointer if symb is in the set
    """

    def lengthOfLongestSubstring(self, s: str) -> int:
        l_pointer = 0
        res = 0
        slight_window = set()
        for i in range(len(s)):
            while s[i] in slight_window:
                slight_window.remove(s[l_pointer])
                l_pointer += 1
            slight_window.add(s[i])
            res = max(res, len(slight_window))

        return res



a = Solution().lengthOfLongestSubstring("pwwkew")
print(a)




