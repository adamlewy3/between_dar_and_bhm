# Bugs

- There is a bug in utils.py, when we are calculating delay. If a train arrives at 0049, but was meant to arrive at 2328, it will calculate delay incorrectly (-1359). See train with RID 202511046723362. This is true more generally of overlapping dates. (Believe this has been fixed, need to test it properly)
