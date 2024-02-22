import csv
import os
import sys

def chunk_large_csv(input_file, chunk_size):
    output_dir = 'chunks'
    os.makedirs(output_dir, exist_ok=True)

    encodings = ['utf-8', 'cp1252', 'latin1'] 

    for encoding in encodings:
        try:
            with open(input_file, 'r', newline='', encoding=encoding) as csvfile:
                reader = csv.reader(csvfile)
                header = next(reader)

                count = 1
                rows_written = 0
                chunk = []

                for row in reader:
                    chunk.append(row)
                    rows_written += 1

                    if rows_written >= chunk_size:
                        output_file = os.path.join(output_dir, f'{os.path.splitext(input_file)[0]}_{count}.csv')
                        write_chunk_to_file(output_file, header, chunk)
                        count += 1
                        rows_written = 0
                        chunk = []

                if chunk:
                    output_file = os.path.join(output_dir, f'{os.path.splitext(input_file)[0]}_{count}.csv')
                    write_chunk_to_file(output_file, header, chunk)
            break

        except UnicodeDecodeError:
            print(f"Failed to decode using encoding '{encoding}'")

    else:
        print("Unable to decode the file using any of the specified encodings.")

def write_chunk_to_file(output_file, header, chunk):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(chunk)


if __name__ == "__main__": 
    
    input_file = input("Enter CSV path: ")

    if input_file.strip() == "": 
        print("No CSV file provided.")
        sys.exit(1)
    elif not os.path.exists(input_file):
        print("The file provided doesn't exist.")
        sys.exit(1)
    elif os.path.splitext(input_file)[1].lower() != ".csv": 
        print("The file provided is not a CSV file.")
        sys.exit(1)

    chunk_size = input("Enter the maximum number of rows in each chunked CSV: ") 
    
    if not chunk_size.isdigit(): 
        print("The input is not an integer.")
        sys.exit(1)

    chunk_large_csv(input_file, int(chunk_size))