# Recursive_Univirsal_Diff
Getting the Deep Difference of dictionaries, iterables,strings and other objects. It will recursively look for all the changes

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
