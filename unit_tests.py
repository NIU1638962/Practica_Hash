# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 15:22:10 2024

@author: Joel Tapia Salvador 
"""
import unittest
from main_hash import uab_md5, second_preimage, collision


class TestLab1(unittest.TestCase):
    def test_uab_md5(self):
        test_vectors_ok = (
            ["hola", 100, 381757249806289069081790873225],
            ["hola", 1, 0],
            ["dfk3874", 68, 229291433845740375560],
            ["dfk3874", 64, 14330714615358773472],
            ["Alexandria", 128, 221630910082124901698625759824682079437],
            ["Alexandria", 129, None],
            ["Alexandria", 0, None],
        )
        for t in test_vectors_ok:
            my_value = uab_md5(t[0], t[1])
            self.assertEqual(my_value, t[2])

    def test_second_preimage(self):
        msg = "find a second preimage"
        for n in range(1, 15):
            new_msg, _ = second_preimage(msg, n)
            self.assertEqual(uab_md5(new_msg, n), uab_md5(msg, n))
            self.assertNotEqual(new_msg, msg)

    def test_collision(self):
        for n in range(1, 15):
            msg1, msg2, _ = collision(n)
            self.assertEqual(uab_md5(msg1, n), uab_md5(msg2, n))
            self.assertNotEqual(msg1, msg2)


unittest.main(argv=[""], verbosity=2, exit=False, buffer=True)
