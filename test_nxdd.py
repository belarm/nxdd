#!/usr/bin/env python3
import unittest
import nxdd

b0 = [[False],[True]]

b1to1 = [
    [False,False],
    [False,True],
    [True,False],
    [True,True],
]

_b2to1 = [
    [0,0,0,0],
    [0,0,0,1],
    [0,0,1,0],
    [0,0,1,1],
    [0,1,0,0],
    [0,1,0,1],
    [0,1,1,0],
    [0,1,1,1],
    [1,0,0,0],
    [1,0,0,1],
    [1,0,1,0],
    [1,0,1,1],
    [1,1,0,0],
    [1,1,0,1],
    [1,1,1,0],
    [1,1,1,1],
]
b2to1 = []
for i in _b2to1:
    b2to1.append([bool(x) for x in i])

class test_nxdd(unittest.TestCase):
    def test_bool1_to_bool1(self):
        dd = nxdd.nxdd()
        funcs = []
        for func in b1to1:
            funcs.append(dd.func_from_tt(func))
        res = []
        for f in funcs:
            for val in b0:
                res.append(dd.run(f, val))
        self.assertEqual(res, [False, False, False, True, True, False, True, True])
        right_answer = []
        for ra in b1to1:
            right_answer += ra
        self.assertEqual(res, right_answer)

        dd.draw_graph('b1.png')

    def test_bool2_to_bool1(self):
        dd = nxdd.nxdd()
        funcs = []
        for func in b2to1:
            funcs.append(dd.func_from_tt(func))
        res = []
        for f in funcs:
            for val in b1to1:
                res.append(dd.run(f, val))
        right_answer = []
        for ra in b2to1:
            right_answer += ra
        self.assertEqual(res, right_answer)
        dd.draw_graph('b2.png')
        for i, f in enumerate(funcs):
            dd.draw_graph('b2-b1-{}.png'.format(i), f)



if __name__ == '__main__':
    unittest.main()
