def check_file(file_path):
    with open(file_path, 'rb') as f:
        chunk_size = 256
        position = 0
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            print(f"Reading chunk at position {position}: {chunk}")
            position += chunk_size

# Check the file for problematic bytes
check_file("adzuna_category.csv")

'''def find_byte_at_position(file_path, position):
    with open(file_path, 'rb') as f:  # Open the file in binary mode
        f.seek(position)  # Move the cursor to the desired position
        byte = f.read(1)  # Read one byte at the given position
        return byte

# Example usage
file_path = "adzuna_category.csv"
position = 97  # The position mentioned in the error message
byte_at_position = find_byte_at_position(file_path, position)
print(f"Byte at position {position}: {byte_at_position}")
'''