# Hierarchical Sorting
The purpose of this challenge is to sort products by properties and metrics. Metrics will define the sorting order or a given property.
Properties can be sorted inside a group of properties. Groups can be sorted based on metrics.
The objective was to be able to do hierarchical sorting.

## Solutions

I have written 4 algorithm to solve the problem:
- challenge_simple: Sort the dataset base on 2 configurable properties and 1 configurable metric
- challenge_total_ordering: Sort the dataset with a configurable depth and 1 configurable metric
- challenge_pure_fn: Sort the dataset with 1 configurable metric
- challenge_config: Sort the dataset with metrics configurable for properties

## Challenge Simple
For this one, I sort a list of object. Using total_ordering decorator, the Item class embed a comparator function (__lt__).
hierarchical_sort function allows to choose the 2 properties that will be used for sorting. First property is the category and second one the product.
The items are sorted by categories and then produts inside their category. The metric column is also a parameter.
To manage the totals, a function is getting categories and products total. They are stored in a dictionnary.
The code is in challenge_simple.py and the output in data_sorted_simple.txt

## Challenge Total Ordering
For this one, I have reused the Item class and total ordering decorator but the depth of the sorting is configurable. Depth means number of properties that will be consider in the hierarchy, starting by the first in the header. I also build a dictionnary with all totals. I have done this with a recursive function to take in account the required depth.
The code is in challenge_total_ordering.py and the output in data_sorted_total_ordering.txt

## Challenge Pure Fn
I wanted to try an other approach than the Item class with total_ordering decorator. I also wanted to remove the recursivity to look for totals since recursive funtion are not the best regarding the memory. In this one, all categories are always used and only the metric can be configured.
I first start by building a tree of the properties. Each property has a value. This value is the total when the property is $total otherwise it is the value of the metric. Each properties also points to their sub-properties. The leaf also store the entire row in an array. The tree is build with dictionnaries.
I then use a BFS algorithm to traverse the tree. First it sorts the properties of the node by their value. Then it moves to the children level. When it reaches a leaf, the row is saved in an output_rows array.
The code is in challenge_pure_fn.py and the output in data_sorted_pure_fn.txt

## Challenge Config
This one is slightly different of the previous one. It allows to set in a config file which metrics to use to sort each properties.
The code is in challenge_config.py, the config in config.json and the output in data_sorted_config.txt.