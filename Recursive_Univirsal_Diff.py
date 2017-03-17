"""
@copyright:
        This code related to Eng.Mohammad Kabajah 
		email: Kabajah.mohammad@gmail.com

@author:
         Mohammad Kabajah
@Contact:
         Kabajah.mohammad@gmail.com
@date:
         Nov 24, 2014
@Purpose:
        Getting the Deep Difference of dictionaries, iterables,
         strings and other objects. It will recursively look for all the changes.
"""

from __future__ import print_function
import difflib
import datetime
import json
from collections import Iterable

class Extensive_Diff(object):
    """
    Deep Difference of dictionaries, iterables, strings and other objects. It will recursively look for all the changes.
    the Function work with(String ,Tuples ,List ,Set ,dictionary , combination of these types with multiple stages)

    Parameters
    ----------
    t1 : Any Pyhton Object(List, dictionary, string that has __dict__
        This is the first item to be compared to the second item

    t2 : Any Pyhton Object(List, dictionary, string that has __dict__
        The second item to be compared to the first one

    Returns
    -------
        A Extensive_Diff object that has already calculated the difference of the 2 items. You can access the result in the 'changes' attribute


    Examples
    --------

    Importing
        >>> from Recursive_Univirsal_Diff import Extensive_Diff
        >>> from pprint import pprint
        >>> from __future__ import print_function


    Same object returns empty dict
        >>> t1 = {'instantID':1, 'username':'kabajah', 'password':12345}
        >>> t2 = t1
        >>> ddiff = Extensive_Diff(t1, t2)
        >>> print (ddiff.changes)
        {}


    Type of an item has changed
        >>> t1 = {'instantID':1, 'username':'kabajah', 'password':12345}
        >>> t2 = {'instantID':'1', 'username':'kabajah', 'password':12345}
        >>> ddiff = Extensive_Diff(t1, t2)
        >>> print (ddiff.changes)
        {'type_changes': ["root['instantID']: 1=<type 'int'> vs. 1=<type 'str'>"]}


    Value of an item has changed
        >>> t1 = {'instantID':1, 'username':'kabajah', 'password':12345}
        >>> t2 = {'instantID':1, 'username':'kabajah', 'password':55555}
        >>> ddiff = Extensive_Diff(t1, t2)
        >>> print (ddiff.changes)
        {'values_changed': ['root['password']: 12345 ====>> 55555']}


    Item added and/or removed
        >>> t1 = {1:1, 2:2, 3:3, 4:4}
        >>> t2 = {1:1, 2:4, 3:3, 5:5, 6:6}
        >>> ddiff = Extensive_Diff(t1, t2)
        >>> pprint (ddiff.changes)
        {'dic_item_added': ['root[5, 6]'],
         'dic_item_removed': ['root[4]'],
         'values_changed': ['root[2]: 2 ====>> 4']}


    String difference
        >>> t1 = {1:1, 2:2, 3:3, 4:{"a":"Mohammad", "b":"Kabajah"}}
        >>> t2 = {1:1, 2:4, 3:3, 4:{"a":"Mohammad", "b":"Kabajah!!!!"}}
        >>> ddiff = Extensive_Diff(t1, t2)
        >>> pprint (ddiff.changes, indent = 2)
        { 'values_changed': [ 'root[2]: 2 ====>> 4',
                              "root[4]['b']:\n--- \n+++ \n@@ -1 +1 @@\n-Kabajah\n+Kabajah!!!!"]}
        >>>
        #for accessing the differences from the ddiff object.
        >>> print (ddiff.changes['values_changed'][1])
        root[4]['b']:
        ---
        +++
        @@ -1 +1 @@
        -Kabajah
        +Kabajah!!!!


    String difference 2
        >>> t1 = {1:1, 2:2, 3:3, 4:{"a":"hello", "b":"world!\nGoodbye!\n1\n2\nEnd"}}
        >>> t2 = {1:1, 2:2, 3:3, 4:{"a":"hello", "b":"world\n1\n2\nEnd"}}
        >>> ddiff = Extensive_Diff(t1, t2)
        >>> pprint (ddiff.changes, indent = 2)
        { 'values_changed': [ "root[4]['b']:\n--- \n+++ \n@@ -1,5 +1,4 @@\n-world!\n-Goodbye!\n+world\n 1\n 2\n End"]}
        >>>
        >>> print (ddiff.changes['values_changed'][0])
        root[4]['b']:
        ---
        +++
        @@ -1,5 +1,4 @@
        -world!
        -Goodbye!
        +world
         1
         2
         End


    Type change
        >>> t1 = {1:1, 2:2, 3:3, 4:{"a":"hello", "b":[1, 2, 3]}}
        >>> t2 = {1:1, 2:2, 3:3, 4:{"a":"hello", "b":"Mohammad_Kabajah"}}
        >>> ddiff = Extensive_Diff(t1, t2)
        >>> pprint (ddiff.changes, indent = 2)
        { 'type_changes': [ "root[4]['b']: [1, 2, 3]=<type 'list'> vs. Mohammad_Kabajah=<type 'str'>"]}

    List difference
        >>> t1 = {1:1, 2:2, 3:3, 4:{"a":"hello", "b":[1, 2, 3]}}
        >>> t2 = {1:1, 2:2, 3:3, 4:{"a":"hello", "b":[1, 2]}}
        >>> ddiff = Extensive_Diff(t1, t2)
        >>> pprint (ddiff.changes, indent = 2)
        { 'list_removed': ["root[4]['b']: [3]"]}

    List difference 2: ** Note that it DOES NOT take order into account(Order not Matter in Our Test)
        >>> # Note that it DOES NOT take order into account
        ... t1 = {1:1, 2:2, 3:3, 4:{"a":"hello", "b":[1, 2, 3]}}
        >>> t2 = {1:1, 2:2, 3:3, 4:{"a":"hello", "b":[1, 3, 2]}}
        >>> ddiff = Extensive_Diff(t1, t2)
        >>> pprint (ddiff.changes, indent = 2)
        { }


    List that contains dictionary:
        >>> t1 = {1:1, 2:2, 3:3, 4:{"a":"hello", "b":[1, 2, {1:1, 2:2}]}}
        >>> t2 = {1:1, 2:2, 3:3, 4:{"a":"hello", "b":[1, 2, {1:3}]}}
        >>> ddiff = Extensive_Diff(t1, t2)
        >>> pprint (ddiff.changes, indent = 2)
        { 'dic_item_removed': ["root[4]['b'][2][2]"],
          'values_changed': ["root[4]['b'][2][1]: 1 ====>> 3"]}
          
    """

    def __init__(self, t1, t2):
        """
        Once the object is initialized, the changes will be filled since
        it will call the diff_iterable.

        If no changes found
        """
        self.changes = {"type_changes":[],
                        "dic_item_added":[],
                        "dic_item_removed":[],
                        "values_changed":[],
                        "unprocessed":[],# for further issue 
                        "list_added":[],
                        "list_removed":[]}

        self.diff_iterable(t1, t2)

        self.changes = dict((k, v) for k, v in self.changes.iteritems() if v)


    def diff_dictionary(self, t1, t2, parent):
        """
        takes 2 dictionaries and their parent (in a semi-tree structure handling)
        This will process the dictionaries keys and fill the 2 lists:

        1- dic_item_added
        2- dic_item_removed

        It will also call diff_iterable method if an iterable object was found.
        """
        t2_keys, t1_keys = [
            set(d.keys()) for d in (t2, t1)
        ]

        t_keys_intersect = t2_keys.intersection(t1_keys)

        t_keys_added = t2_keys - t_keys_intersect
        t_keys_removed = t1_keys - t_keys_intersect

        if t_keys_added:
            self.changes["dic_item_added"].append("%s%s" % (parent, list(t_keys_added)))

        if t_keys_removed:
            self.changes["dic_item_removed"].append("%s%s" % (parent, list(t_keys_removed)))

        for item in t_keys_intersect:
            if isinstance(item, basestring):
                item_str = "'%s'" % item
            else:
                item_str = item
            self.diff_iterable(t1[item], t2[item], parent="%s[%s]" % (parent, item_str))


    def diff_iterable(self, t1, t2, parent="root"):
        """
        This method will take 2 iterable objects and determine the type of change between those 2 iterables
        in a recursive manner, the types of change could be:

        1- type_changes: for example if value was integer and now it's a string
        2- values_changed: for example if value was 5 and changed to anything else
        3- unprocessed: if the type could not be processed (unicode or unrecognized data)
        4- list_added: new list found in iterable
        5- list removed: previous list could not be found in iterable

        Any change will be stored in local variables in object.

        If the iterable was dictionary, it will call diff_dictionary method.
        """
        if type(t1) != type(t2):
            self.changes["type_changes"].append("%s: %s=%s vs. %s=%s" % (parent, t1, type(t1), t2, type(t2)))

        elif isinstance(t1, basestring):
            diff = difflib.unified_diff(t1.splitlines(), t2.splitlines(), lineterm='')
            diff = list(diff)
            if diff:
                diff = ' \n '.join(diff)
                self.changes["values_changed"].append("%s:\n %s" % (parent, diff))

        elif isinstance(t1, (int, long, float, complex, datetime.datetime)):
            if t1 != t2:
                self.changes["values_changed"].append("%s: %s ====>> %s" % (parent, t1, t2))


        elif isinstance(t1, dict):
            self.diff_dictionary(t1, t2, parent)

        elif isinstance(t1, Iterable):

            try:
                t1_set = set(t1)
                t2_set = set(t2)
            # When we can't make a set since the iterable has unhashable items
            except TypeError:
                for i, (x, y) in  enumerate(zip(t1, t2)):
                    self.diff_iterable(x, y, "%s[%s]" % (parent, i))

                if len(t1) != len(t2):
                    items_added = [item for item in t2 if item not in t1]
                    items_removed = [item for item in t1 if item not in t2]
                else:
                    items_added = None
                    items_removed = None
            else:
                items_added = list(t2_set - t1_set)
                items_removed = list(t1_set - t2_set)

            if items_added:
                self.changes["list_added"].append("%s: %s" % (parent, items_added))

            if items_removed:
                self.changes["list_removed"].append("%s: %s" % (parent, items_removed))

        else:
            try:
                t1_dict = t1.__dict__
                t2_dict = t2.__dict__
            except AttributeError:
                pass
            else:
                self.diff_dictionary(t1_dict, t2_dict, parent)
        return
