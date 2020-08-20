import argparse
import json

TOTAL = "$total"
META = "meta"
VALUE = "value"
ROW = "row"
PROPERTY = "property"
SEPARATOR = '|'
PROPS = "props"
METRICS = "metrics"

def read_config(c, header_items):
    config = {}
    config[METRICS] = {}
    config[PROPS] = {}

    for metric in c[METRICS]:
        config[METRICS][metric] = header_items.index(metric)

    for prop in c[PROPS]:
        config[PROPS][header_items.index(prop[0])] = config[METRICS][prop[1]]

    return config


## Hierarchical Sort function
def hierarchical_sort(input_file_path, output_file_path):
    f = open(input_file_path, "r")
    data = f.readlines()

    clean_rows = []
    for row in data:
        clean_rows.append(row.replace('\n', ''))
    data = clean_rows

    header_items = data[0].split(SEPARATOR)

    with open('./config.json') as c:
        config = read_config(json.load(c), header_items)

    nb_prop = sum(item.startswith(PROPERTY) for item in header_items)

    data = list(map(lambda x: x.split(SEPARATOR), data[1:]))

    product_dic = {}
    
    ## Build a tree to store the products
    for row in data:
        cur_depth = 0
        cur_dic = product_dic
        while cur_depth < nb_prop:
            cur_item = row[cur_depth]
            next_item = row[cur_depth + 1] if cur_depth < nb_prop - 1 else None

            if cur_item not in cur_dic:
                cur_dic[cur_item] = {}
                cur_dic[cur_item][META] = {}

            if next_item == TOTAL or next_item == None:
                cur_dic[cur_item][META][VALUE] = float(row[config[PROPS][cur_depth]])
                
            if next_item == None:
                cur_dic[cur_item][META][ROW] = row
            
            cur_dic = cur_dic[cur_item]
            cur_depth += 1

    cur_dic = product_dic
    stack = []
    stack.append(product_dic)
    output_rows = []

    ## Use BFS to traverse the tree
    ## For each level, sort the level
    ## When last level is reached, save row in output_rows
    while len(stack) != 0:
        cur_dic = stack.pop()

        if META in cur_dic and ROW in cur_dic[META]:
            output_rows.append(cur_dic[META][ROW])
            continue

        items = []
        for k in cur_dic.keys():
            if k != TOTAL and k != META:
                items.append((k, cur_dic[k][META][VALUE]))

        items.sort(key=lambda x: x[1])

        if TOTAL in cur_dic:
            items.append((TOTAL, cur_dic[TOTAL][META][VALUE]))

        for item in items:
            stack.append(cur_dic[item[0]])

    o = open(output_file_path, "w+")
    o.write(f"{SEPARATOR.join(header_items)}\n")
    for item in output_rows:
        o.write(f"{SEPARATOR.join(item)}\n")
        

def main(args):
    try:
        hierarchical_sort(args.input, args.output)
        print(f"Data sorted, output file: {args.output}")
    except Exception as error:
        print(str(error))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", help="Input file path", default="./data.txt")
    parser.add_argument("-o", "--output", help="Output file path", default="./data_sorted_config.txt")

    args = parser.parse_args()
    main(args)
