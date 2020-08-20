import argparse
from functools import total_ordering

TOTAL = "$total"
SEPARATOR = '|'

## Class Item using total_ordering to define ordering logic
@total_ordering
class Item:
    def __init__(self, row, value_index, max_depth, total_dic):
        self.row = row

        try:
            self.value = float(self.row[value_index])
        except:
            raise Exception(f"Product value is not a number, value = {self.row[value_index]}")

        self.total_dic = total_dic
        self.max_depth = max_depth


    def __lt__(self, other):
        i = 0
        dic = self.total_dic
        while i < self.max_depth:
            if self.row[i] == TOTAL:
                return True
            
            if other.row[i] == TOTAL:
                return False

            if i == self.max_depth - 1:
                return other.value < self.value

            if self.row[i] != other.row[i]:
                return dic[other.row[i]]["_"] < dic[self.row[i]]["_"] 

            dic = dic[self.row[i]]

            i += 1


## Build hierarchical dictionary to store totals
def build_total_dictionnary(row, max_depth, value_index, dic, cur_depth = 0):
    if max_depth - 1 == cur_depth:
        return

    cur_item = row[cur_depth]

    if cur_item != TOTAL:
        if cur_item not in dic: 
            dic[cur_item] = {}

        if row[cur_depth + 1] == TOTAL:
            dic[cur_item]["_"] = float(row[value_index])

        build_total_dictionnary(row, max_depth, value_index, dic[cur_item], cur_depth + 1)


## Function to remove end of line in rows
def clean_end_of_line(rows):
    clean_rows = []
    for row in rows:
        clean_rows.append(row.replace('\n', ''))

    return clean_rows


## Hierarchical Sort function
def hierarchical_sort(input_file_path, output_file_path, value_column, depth):
    f = open(input_file_path, "r")
    data = f.readlines()

    max_depth = int(depth)

    data = clean_end_of_line(data)

    header_items = data[0].split(SEPARATOR)

    value_index = header_items.index(value_column)

    data = list(map(lambda x: x.split(SEPARATOR), data[1:]))

    total_dic = {}

    for row in data:
        build_total_dictionnary(row, max_depth, value_index, total_dic)

    items = list(map(lambda x: Item(x, value_index, max_depth, total_dic), data))

    items.sort()

    o = open(output_file_path, "w+")
    o.write(f"{SEPARATOR.join(header_items)}\n")
    for item in items:
        o.write(f"{SEPARATOR.join(item.row)}\n")


def main(args):
    try:
        hierarchical_sort(args.input, args.output, args.value, args.depth)
        print(f"Data sorted, output file: {args.output}")
    except Exception as error:
        print(str(error))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", help="Input file path", default="./data.txt")
    parser.add_argument("-o", "--output", help="Output file path", default="./data_sorted_total_ordering.txt")
    parser.add_argument("-d", "--depth", help="Sorting depth", default="3")
    parser.add_argument("-v", "--value", help="Value property name", default="net_sales")

    args = parser.parse_args()
    main(args)
