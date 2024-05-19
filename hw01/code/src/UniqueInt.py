import os
import glob

class IntegerFileProcessor:
    @staticmethod
    def find_unique_integers(input_file, output_file):
        unique_integers = set()

        try:
            with open(input_file, 'r') as file:
                for line in file:
                    items = line.strip().split()
                    if len(items) == 1:
                        try:
                            num = int(items[0])
                            if -1023 <= num <= 1023:
                                unique_integers.add(num)
                        except ValueError:
                            continue
        except FileNotFoundError:
            print(f"File not found: {input_file}")
            return

        with open(output_file, 'w') as file:
            for integer in sorted(unique_integers):
                file.write(f"{integer}\n")

        print(f"Completed processing {input_file}. Results saved to {output_file}.")

def main():
    base_path = os.path.dirname(__file__)
    input_dir = os.path.join(base_path, '../../sample_inputs/')
    output_dir = os.path.join(base_path, '../../sample_results/')

    input_files = glob.glob(os.path.join(input_dir, '*.txt'))

    for file_path in input_files:
        file_name = os.path.basename(file_path)
        result_file = os.path.join(output_dir, f"{file_name}_results.txt")
        IntegerFileProcessor.find_unique_integers(file_path, result_file)

if __name__ == "__main__":
    main()
