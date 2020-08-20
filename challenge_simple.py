import argparse
from functools import total_ordering

TOTAL = "$total"
CATEGORY_INDEX = "category_index"
PRODUCT_INDEX = "product_index"
VALUE_INDEX = "value_index"
SEPARATOR = '|'

## Class Item using total_ordering to define ordering logic
@total_ordering
class Item:
    def __init__(self, row, header_indexes, categories_total):
        self.row = row
        self.is_total = self.row[header_indexes[CATEGORY_INDEX]] == TOTAL
        self.category_total = categories_total[self.row[header_indexes[CATEGORY_INDEX]]] if self.is_total == False else 0
        self.category_label = self.row[header_indexes[CATEGORY_INDEX]]
        self.product_label = self.row[header_indexes[PRODUCT_INDEX]]

        try:
            self.value = float(self.row[header_indexes[VALUE_INDEX]])
        except:
            raise Exception(f"Product value is not a number, value = {self.row[header_indexes[VALUE_INDEX]]}")

        self.header_indexes = header_indexes
        self.categories_total = categories_total


    def __lt__(self, other):
        ## If other category is total
        if other.is_total:
            return False

        ## If self category is total
        if self.is_total:
            return True

        ## If different category, compare category total
        if self.category_label != other.category_label:
            return other.category_total < self.category_total

        ## If same category
        ## If other product is total
        if other.product_label == TOTAL:
            return False

        ## If self product is total
        if self.product_label == TOTAL:
            return True

        ## Else, compare values
        return other.value < self.value


## Function to get totals per categories
def get_categories_total(data, header_indexes):
    categories_total = {}
    category_index = header_indexes[CATEGORY_INDEX]
    product_index = header_indexes[PRODUCT_INDEX]
    value_index = header_indexes[VALUE_INDEX]

    for row in data:
        if row[category_index] != TOTAL and row[product_index] == TOTAL:
            try:
                categories_total[row[category_index]] = float(row[value_index])
            except:
                raise Exception(f"Category total is not a number, value = {row[value_index]}")

    return categories_total
            

## Function to get category, product and value column indexes
def read_header(header_items, category_column, product_column, value_column):
    header_indexes = {}

    for i, item in enumerate(header_items):
        if item == category_column:
            header_indexes[CATEGORY_INDEX] = i
        elif item == product_column:
            header_indexes[PRODUCT_INDEX] = i
        elif item == value_column:
            header_indexes[VALUE_INDEX] = i

    if CATEGORY_INDEX not in header_indexes:
        raise Exception(f"Category column {category_column} was not found in header")

    if PRODUCT_INDEX not in header_indexes:
        raise Exception(f"Product column {product_column} was not found in header")

    if VALUE_INDEX not in header_indexes:
        raise Exception(f"Product column {value_column} was not found in header")

    return header_indexes


## Function to remove end of line in rows
def clean_end_of_line(rows):
    clean_rows = []
    for row in rows:
        clean_rows.append(row.replace('\n', ''))

    return clean_rows


## Hierarchical Sort function
def hierarchical_sort(input_file_path, output_file_path, category_column, product_column, value_column):
    f = open(input_file_path, "r")
    data = f.readlines()

    data = clean_end_of_line(data)

    header_items = data[0].split(SEPARATOR)

    try:
        header_indexes = read_header(header_items, category_column, product_column, value_column)
    except Exception as error:
        raise Exception(f"Header error: {str(error)}")

    data = list(map(lambda x: x.split(SEPARATOR), data[1:]))

    try:
        categories_total = get_categories_total(data, header_indexes)
    except Exception as error:
        raise Exception(f"Categories error: {str(error)}")

    items = list(map(lambda x: Item(x, header_indexes, categories_total), data))

    try:
        items.sort()
    except Exception as error:
        raise Exception(f"Products error: {str(error)}")

    o = open(output_file_path, "w+")
    o.write(f"{SEPARATOR.join(header_items)}\n")
    for item in items:
        o.write(f"{item.row}\n")


def main(args):
    try:
        hierarchical_sort(args.input, args.output, args.category, args.product, args.value)
        print(f"Data sorted, output file: {args.output}")
    except Exception as error:
        print(str(error))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", help="Input file path", default="./data.txt")
    parser.add_argument("-o", "--output", help="Output file path", default="./data_sorted_simple.txt")
    parser.add_argument("-c", "--category", help="Category property name", default="property0")
    parser.add_argument("-p", "--product", help="Product property name", default="property1")
    parser.add_argument("-v", "--value", help="Value property name", default="net_sales")

    args = parser.parse_args()
    main(args)
