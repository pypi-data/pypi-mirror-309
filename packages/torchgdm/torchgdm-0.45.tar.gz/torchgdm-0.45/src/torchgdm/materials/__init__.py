# -*- coding: utf-8 -*-
"""package for materials optical properties
"""
from .base_classes import MaterialBase

from .hardcoded import MatConstant
from .hardcoded import MatTiO2

from .tabulated import list_available_materials
from .tabulated import MatDatabase
