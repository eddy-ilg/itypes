#!/usr/bin/env python3 

class Key:
    def __init__(self, group_name=None, item_name=None, variable_name=None):
        self._group_name = group_name 
        self._item_name = item_name 
        self._variable_name = variable_name 
    
    def group_name(self):
        return self._group_name

    def item_name(self):
        return self._item_name

    def variable_name(self):
        return self._variable_name

    def __str__(self):
        path = [self._group_name] 
        if self._item_name is not None: 
            path.append(self._item_name)
            if self._variable_name is not None: 
                path.append(self._variable_name)