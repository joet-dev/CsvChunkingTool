import csv
import os

def chunk_large_csv(input_file, chunk_size):
    # Create a directory to store the chunks if it doesn't exist
    output_dir = 'chunks'
    os.makedirs(output_dir, exist_ok=True)

    # List of encodings to try
    encodings = ['utf-8', 'cp1252', 'latin1']  # Add more encodings if needed

    for encoding in encodings:
        try:
            # Open the input CSV file for reading with the current encoding
            with open(input_file, 'r', newline='', encoding=encoding) as csvfile:
                reader = csv.reader(csvfile)
                header = next(reader)  # Read the header row

                # Initialize variables
                count = 1
                rows_written = 0
                chunk = []

                for row in reader:
                    # Append row to the chunk list
                    chunk.append(row)
                    rows_written += 1

                    # If the chunk size is reached, write the chunk to a new file
                    if rows_written >= chunk_size:
                        output_file = os.path.join(output_dir, f'{os.path.splitext(input_file)[0]}_{count}.csv')
                        write_chunk_to_file(output_file, header, chunk)
                        count += 1
                        rows_written = 0
                        chunk = []

                # Write the remaining chunk to a file if any rows left
                if chunk:
                    output_file = os.path.join(output_dir, f'{os.path.splitext(input_file)[0]}_{count}.csv')
                    write_chunk_to_file(output_file, header, chunk)

            # If no exception is raised, break out of the loop
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
    
    input_file = 'output.csv'
    chunk_size = 1000000  # Number of rows per chunk
    chunk_large_csv(input_file, chunk_size)