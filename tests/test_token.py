#!/usr/bin/env pythonfrom context import *import unittestclass TestTokens(unittest.TestCase):    def test_ReactionTokenFailure(self):        self.assertRaisesRegexp(ValueError, "Invalid path parameter.*", Pattern, None)        self.assertRaisesRegexp(ValueError, "Invalid path parameter.*", Pattern, "")    ###########################################################################    ## ALL POSSIBLE PATTERN COMBINATIONS    ###########################################################################    #############################################    # CASE 1    #   a/b/c is matched by /a/*    #############################################    def test_Matching1(self):        self.assertTrue(Pattern('/a/*').match('/a/b/c'))    #############################################    # CASE 2    #   /a/b is NOT matched by /a/*/c    #############################################    def test_Matching2(self):        self.assertFalse(Pattern('/a/*/c').match('/a/b'))    #############################################    # CASE 3    #   /a/b/b/b/c is matched by /a/*/c    #############################################    def test_Matching3(self):        # Expected pattern /a/*/c (some token ending with c)        # Input path: /a/b fails since no c at the end        self.assertTrue(Pattern('/a/*/c').match('/a/b/b/b/c'))    #############################################    # CASE 4    #   /a/b/b/b/c/d is NOT matched by /a/*/c    #############################################    def test_Matching4(self):        # Expected pattern /a/*/c (some token ending with c)        # Input path: /a/b fails since no c at the end        self.assertFalse(Pattern('/a/*/c').match('/a/b/b/b/c/d'))    #############################################    # CASE 5    #   /a/b/b/b/c/d is NOT matched by /a/*/c    #############################################    def test_Matching5(self):        # Expected pattern /a/*/c (some token ending with c)        # Input path: /a/b fails since no c at the end        self.assertTrue(Pattern('/a/*/c').match('/a/b/b/b/c/c/c'))    #############################################    # CASE 6    #   /a/b/b/b/a/c/c/d is matched by /a/*/d    #############################################    def test_Matching6(self):        # Expected pattern /a/*/c (some token ending with c)        # Input path: /a/b fails since no c at the end        self.assertTrue(Pattern('/a/*/d').match('/a/b/b/b/a/c/c/d'))    #############################################    # CASE 7    #   /a/b/b///b/a/c/c/d is matched by /a/*/d    #############################################    def test_Matching7(self):        # Expected pattern /a/*/c (some token ending with c)        # Input path: /a/b fails since no c at the end        self.assertTrue(Pattern('/a/*/d').match('/a/b/b///b/a/c/c/d'))    def test_Matching8(self):        # Expected pattern /a/*/c (some token ending with c)        # Input path: /a/b fails since no c at the end        self.assertFalse(Pattern('/arithm/calc/*').match('/arithm/result'))    def test_Matching9(self):        # Expected pattern /a/*/c (some token ending with c)        # Input path: /a/b fails since no c at the end        self.assertTrue(Pattern('/arithm/result').match('/arithm/result'))    def test_Matching10(self):        # Expected pattern /a/*/c (some token ending with c)        # Input path: /a/b fails since no c at the end        self.assertFalse(Pattern('/arithm/result').match('/arithm/result/test'))