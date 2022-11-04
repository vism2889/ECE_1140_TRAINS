#!/usr/bin/env python3

##############################################################################
# AUTHOR:   Morgan Visnesky
# DATE:     11/03/2022
# FILENAME: BlockModel_UnitTest.py
# DESCRIPTION:
#       Code for testing the BlockModel.py file and its Dependencies
#
##############################################################################

import sys
# tell interpreter where to look for model files
sys.path.insert(0,"../Track-System-Models")
from BlockModel import BlockModel

class BlockModel_UnitTest(unittest.TestCase):