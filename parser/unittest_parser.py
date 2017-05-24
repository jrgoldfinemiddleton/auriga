#!/usr/bin/env python3

import unittest
from parser import Parser

class TestParser(unittest.TestCase):

    def test_remove_articles(self):
        self.assertTrue('a' not in Parser.remove_articles(['a', 'big', 'day']))
        self.assertTrue('big' in Parser.remove_articles(['a', 'big', 'day']))
        self.assertTrue('day' in Parser.remove_articles(['a', 'big', 'day']))

        self.assertTrue('those' not in Parser.remove_articles(
            ['whose', 'are', 'those']))
        self.assertTrue('whose' in Parser.remove_articles(
            ['whose', 'are', 'those']))
        self.assertTrue('are' in Parser.remove_articles(
            ['whose', 'are', 'those']))

        self.assertTrue('the' not in Parser.remove_articles(['the']))
        self.assertTrue(' the' in Parser.remove_articles([' the']))


    def test_get_verb_invalid(self):
        self.assertIsNone(Parser.get_verb(['', 'sail', 'home']))
        self.assertIsNone(Parser.get_verb(['dear', 'me']))
        self.assertIsNone(Parser.get_verb([]))
        self.assertIsNone(Parser.get_verb(['read1']))
        self.assertIsNone(Parser.get_verb(['you', 'go']))


    def test_get_verb_valid(self):
        CANONICAL_ACTIONS = [
                'drop', 'go', 'listen', 'look', 'pull', 'push', 'recharge',
                'take', 'talk', 'use', 'wait', 'help', 'inventory',
                'loadgame', 'savegame', 'quit'
                ]

        for verb in CANONICAL_ACTIONS:
            self.assertEqual(verb, Parser.get_verb([verb]))

        for verb in Parser.ACTIONS:
            if verb not in CANONICAL_ACTIONS:
                self.assertNotEqual(verb, Parser.get_verb([verb]))

        self.assertNotEqual('look at', Parser.get_verb(['look', 'at']))

        for verb in Parser.ACTIONS:
            self.assertIsNotNone(Parser.get_verb([verb]))


    def test_get_verb_len(self):
        lst = []
        Parser.get_verb(lst)
        self.assertEqual(0, len(lst))

        lst = ['']
        Parser.get_verb(lst)
        self.assertEqual(1, len(lst))

        lst = ['go']
        Parser.get_verb(lst)
        self.assertEqual(0, len(lst))

        lst = ['go', 'north']
        Parser.get_verb(lst)
        self.assertEqual(1, len(lst))

        lst = ['don\'t', 'go']
        Parser.get_verb(lst)
        self.assertEqual(2, len(lst))

        lst = ['go', 'go', 'go']
        Parser.get_verb(lst)
        self.assertEqual(2, len(lst))

        lst = ['clutch', 'the', 'thing']
        Parser.get_verb(lst)
        self.assertEqual(2, len(lst))


    def test_get_prepositions(self):
        self.assertNotIn('an', Parser.get_prepositions(
            ['read', 'em', 'an', 'weep']))
        self.assertIn('up', Parser.get_prepositions(
            ['y\'all', 'all', 'up', 'in', 'my', 'grill']))
        self.assertIn('in', Parser.get_prepositions(
            ['y\'all', 'all', 'up', 'in', 'my', 'grill']))

        self.assertEqual(0, len(Parser.get_prepositions(['go', 'home'])))
        self.assertEqual(1, len(Parser.get_prepositions(['go', 'out'])))
        self.assertEqual(1, len(Parser.get_prepositions(['go', 'up'])))
        self.assertEqual(1, len(Parser.get_prepositions(['go', 'under'])))
  

    def test_get_exit_type(self):
        self.assertEqual('sliding door', Parser.get_exit_type(
            ['sliding', 'door']))

        self.assertEqual('saloon doors', Parser.get_exit_type(
            ['saloon', 'doors']))

        self.assertEqual('air duct', Parser.get_exit_type(
            ['air', 'duct']))

        self.assertEqual('steel door', Parser.get_exit_type(
            ['steel', 'door']))

        self.assertEqual('hallway', Parser.get_exit_type(
            ['hallway']))

        self.assertEqual('elevator', Parser.get_exit_type(
            ['elevator']))

        self.assertEqual('glass door', Parser.get_exit_type(
            ['glass', 'door']))

        self.assertEqual('opening', Parser.get_exit_type(
            ['opening']))

        self.assertEqual('hallway', Parser.get_exit_type(
            ['hall', 'way']))

        self.assertEqual('air duct', Parser.get_exit_type(
            ['use', 'vent', 'path']))

        self.assertIsNone(Parser.get_exit_type(['talk', 'to', 'me']))
        self.assertIsNone(Parser.get_exit_type([]))
        self.assertIsNone(Parser.get_exit_type(['']))
        self.assertIsNone(Parser.get_exit_type(['north']))


    def test_get_item(self):
        self.assertIsNone(Parser.get_item(['read', 'my', 'lips', 'no', 'new']))
        self.assertIsNone(Parser.get_item([]))
        self.assertIsNone(Parser.get_item(['']))
        
        self.assertEqual('ssd', Parser.get_item(['solid', 'state', 'drive']))
        self.assertEqual('ssd', Parser.get_item(['solid', 'state']))
        self.assertEqual('ssd', Parser.get_item(['an', 'ssd', 'item']))
        self.assertEqual('ssd', Parser.get_item(['large', 'ssd']))
        self.assertEqual('ssd', Parser.get_item(['hard', 'disk']))
        self.assertEqual('ssd', Parser.get_item(['hard', 'drive']))

        self.assertNotEqual('ssd', Parser.get_item(['hard', 'to', 'disk']))
        self.assertNotEqual('ssd', Parser.get_item([' ssd']))

        self.assertEqual('small bucket', Parser.get_item(
            ['one', 'small', 'bucket']))
        self.assertEqual('large bucket', Parser.get_item(
            ['one', 'large', 'bucket']))
        self.assertEqual('large bucket', Parser.get_item(
            ['one', 'small', 'large', 'bucket']))
        self.assertNotEqual(Parser.get_item(['small', 'bucket']),
                Parser.get_item(['large', 'bucket']))

        # at one point 'usb cable' erroneously resolved to 'usb'
        self.assertEqual('usb cord', Parser.get_item(
            ['usb', 'cable']))

    def test_get_character(self):
        self.assertIsNone(Parser.get_character(['read', 'my', 'lips', 'no', 'new']))
        self.assertIsNone(Parser.get_character([]))
        self.assertIsNone(Parser.get_character(['']))
        
        self.assertEqual('wasp12', Parser.get_character(['wasp-12']))
        self.assertEqual('wasp12', Parser.get_character(['wasp12']))
        self.assertEqual('wasp12', Parser.get_character(['wasp', '12']))
        self.assertEqual('wasp12', Parser.get_character(['it\'s', 'wasp12']))

        self.assertNotEqual('wasp12', Parser.get_character(['was-p12']))
        self.assertNotEqual('wasp12', Parser.get_character(['wasp1']))
        self.assertNotEqual('wasp12', Parser.get_character(['wasp-12 ']))
        self.assertNotEqual('wasp12', Parser.get_character(['wasp', 'to', '12']))

        self.assertEqual('stuffed robot bear', Parser.get_character(
            ['one', 'stuffed', 'robot', 'bear']))
        self.assertEqual('stuffed robot bear', Parser.get_character(
            ['one', 'robobear']))
        self.assertEqual('stuffed robot bear', Parser.get_character(
            ['the', 'holy', 'robo-bear']))


    def test_get_direction(self):
        self.assertEqual('north', Parser.get_direction(['n']))
        self.assertEqual('down', Parser.get_direction(['below']))
        self.assertEqual('south', Parser.get_direction(['south']))
        self.assertEqual('west', Parser.get_direction(['w', 'n']))
        self.assertEqual('west', Parser.get_direction(['w', 'n', 'e', 's']))
        self.assertEqual('up', Parser.get_direction(['up']))

        # make sure direction is first word
        self.assertIsNone(Parser.get_direction(
            ['which', 'way', 'is', 'up']))
        self.assertIsNone(Parser.get_direction(
            ['which', 'way', 'is', 'north']))
        self.assertIsNone(Parser.get_direction(['the', 'north']))

        self.assertIsNone(Parser.get_direction(['which', 'way']))
        self.assertIsNone(Parser.get_direction(['up?']))
        self.assertIsNone(Parser.get_direction(['up ']))
        self.assertIsNone(Parser.get_direction(['']))
        self.assertIsNone(Parser.get_direction([]))


    def test_get_identity(self):
        pass


    def test_action_requested(self):
        # this will actually be broken into a number of test functions
        pass

if __name__ == '__main__':
    unittest.main(exit = False)