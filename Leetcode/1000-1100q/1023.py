'''
A query word matches a given pattern if we can insert lowercase letters to the pattern word so that it equals the query. (We may insert each character at any position, and may insert 0 characters.)

Given a list of queries, and a pattern, return an answer list of booleans, where answer[i] is true if and only if queries[i] matches the pattern.

 

Example 1:

Input: queries = ["FooBar","FooBarTest","FootBall","FrameBuffer","ForceFeedBack"], pattern = "FB"
Output: [true,false,true,true,false]
Explanation: 
"FooBar" can be generated like this "F" + "oo" + "B" + "ar".
"FootBall" can be generated like this "F" + "oot" + "B" + "all".
"FrameBuffer" can be generated like this "F" + "rame" + "B" + "uffer".
Example 2:

Input: queries = ["FooBar","FooBarTest","FootBall","FrameBuffer","ForceFeedBack"], pattern = "FoBa"
Output: [true,false,true,false,false]
Explanation: 
"FooBar" can be generated like this "Fo" + "o" + "Ba" + "r".
"FootBall" can be generated like this "Fo" + "ot" + "Ba" + "ll".
Example 3:

Input: queries = ["FooBar","FooBarTest","FootBall","FrameBuffer","ForceFeedBack"], pattern = "FoBaT"
Output: [false,true,false,false,false]
Explanation: 
"FooBarTest" can be generated like this "Fo" + "o" + "Ba" + "r" + "T" + "est".
 

Note:

1. 1 <= queries.length <= 100
2. 1 <= queries[i].length <= 100
3. 1 <= pattern.length <= 100
4. All strings consists only of lower and upper case English letters.
'''

class Solution(object):
    def camelMatch(self, queries, pattern):
        """
        :type queries: List[str]
        :type pattern: str
        :rtype: List[bool]
        """
        import re
        result = []
        patterns = re.findall('[A-Z][a-z]*', pattern)
        
        for query in queries:
            splitter = re.findall('[A-Z][a-z]*', query)
            flag = True
            if len(patterns) == len(splitter):
                for index in range(len(patterns)):
                    # print patterns[index], splitter[index]
                    p_i, s_i = 1, 1
                    if patterns[index][0] == splitter[index][0]:
                        while p_i < len(patterns[index]) and s_i < len(splitter[index]):
                            if patterns[index][p_i] == splitter[index][s_i]:
                                p_i += 1
                                s_i += 1
                            else:
                                s_i += 1
                        if p_i != len(patterns[index]):
                            flag = False
                            break
                    else:
                        flag = False
                        break
                if flag:
                    result.append(True)
                else:
                    result.append(False)
            else:
                result.append(False)
        return result
