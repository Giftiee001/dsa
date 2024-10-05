import sys


class SparseArray:
    def __init__(self, total_rows=0, total_cols=0):
        self.row_count = total_rows
        self.col_count = total_cols
        self.non_zero_elements = {}

    @staticmethod
    def initialize_from_file(file_name):
        try:
            with open(file_name, 'r') as file:
                content = file.readlines()
                rows = int(content[0].split('=')[1].strip())
                cols = int(content[1].split('=')[1].strip())
                sparse_array = SparseArray(rows, cols)
                for entry in content[2:]:
                    entry = entry.strip()
                    if not entry:
                        continue
                    if entry[0] != '(' or entry[-1] != ')':
                        raise ValueError("Invalid entry format in the input file")
                    r, c, val = map(int, entry[1:-1].split(','))
                    sparse_array.assign_value(r, c, val)
                return sparse_array
        except Exception as err:
            raise ValueError(f"File reading error for {file_name}: {err}")

    def assign_value(self, row_num, col_num, value):
        if value != 0:
            self.non_zero_elements[(row_num, col_num)] = value
        elif (row_num, col_num) in self.non_zero_elements:
            del self.non_zero_elements[(row_num, col_num)]

    def fetch_value(self, row_num, col_num):
        return self.non_zero_elements.get((row_num, col_num), 0)

    def matrix_add(self, another_array):
        if self.row_count != another_array.row_count or self.col_count != another_array.col_count:
            raise ValueError("Addition requires matrices with identical dimensions")
        outcome = SparseArray(self.row_count, self.col_count)
        for (r, c), val in self.non_zero_elements.items():
            outcome.assign_value(r, c, val + another_array.fetch_value(r, c))
        for (r, c), val in another_array.non_zero_elements.items():
            if (r, c) not in self.non_zero_elements:
                outcome.assign_value(r, c, val)
        return outcome

    def matrix_subtract(self, another_array):
        if self.row_count != another_array.row_count or self.col_count != another_array.col_count:
            raise ValueError("Subtraction requires matrices with identical dimensions")
        outcome = SparseArray(self.row_count, self.col_count)
        for (r, c), val in self.non_zero_elements.items():
            outcome.assign_value(r, c, val - another_array.fetch_value(r, c))
        for (r, c), val in another_array.non_zero_elements.items():
            if (r, c) not in self.non_zero_elements:
                outcome.assign_value(r, c, -val)
        return outcome

    def matrix_multiply(self, another_array):
        if self.col_count != another_array.row_count:
            raise ValueError(f"Multiplication requires compatible dimensions: {self.col_count} != {another_array.row_count}")
        outcome = SparseArray(self.row_count, another_array.col_count)
        for (r, c), val in self.non_zero_elements.items():
            for k in range(another_array.col_count):
                if (c, k) in another_array.non_zero_elements:
                    outcome.assign_value(r, k, outcome.fetch_value(r, k) + val * another_array.fetch_value(c, k))
        return outcome

    def save_to_file(self, file_name):
        with open(file_name, 'w') as file:
            file.write(f"rows={self.row_count}\n")
            file.write(f"cols={self.col_count}\n")
            for (r, c), val in sorted(self.non_zero_elements.items()):
                file.write(f"({r}, {c}, {val})\n")


def perform_operations():
    if len(sys.argv) != 4:
        print("Usage: python SparseMatrix.py <operation_type> <matrix_file_a> <matrix_file_b>")
        print("Supported operations: add, subtract, multiply")
        return

    operation_type = sys.argv[1]
    matrix_file_a = sys.argv[2]
    matrix_file_b = sys.argv[3]

    # Generate matrix objects from input files
    try:
        first_matrix = SparseArray.initialize_from_file(matrix_file_a)
        second_matrix = SparseArray.initialize_from_file(matrix_file_b)
    except ValueError as error_msg:
        print(error_msg)
        return

    print(f"Matrix A: {first_matrix.row_count}x{first_matrix.col_count}, Elements: {first_matrix.non_zero_elements}")
    print(f"Matrix B: {second_matrix.row_count}x{second_matrix.col_count}, Elements: {second_matrix.non_zero_elements}")

    try:
        if operation_type == 'add':
            result_matrix = first_matrix.matrix_add(second_matrix)
        elif operation_type == 'subtract':
            result_matrix = first_matrix.matrix_subtract(second_matrix)
        elif operation_type == 'multiply':
            result_matrix = first_matrix.matrix_multiply(second_matrix)
        else:
            print("Operation not supported")
            return

        output_path = rf'C:\dsa\sparse_matrix\sparse_results\result_{operation_type}.txt'
        result_matrix.save_to_file(output_path)
        print(f"Operation successful. Results stored at {output_path}")
    except ValueError as error_msg:
        print(error_msg)


if __name__ == "__main__":
    perform_operations()