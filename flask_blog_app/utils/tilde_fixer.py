import os


def fix(filename = None):
    directory = os.getcwd()
    entries_path = os.path.join(directory, 'entries')
    print(f"Looking in directory {entries_path}")
    the_file = None
    all_files = []
    for root, dir, files in os.walk(entries_path):
        if filename and filename in files:
            the_file = os.path.join(root, filename)
            print(f"Found: {the_file}")
        if not filename:
            all_files.extend([os.path.join(root, f) for f in files])
    if filename and the_file:
        process_file(the_file)
    elif not filename:
        # process all files
        for f in all_files:
            basename = os.path.basename(f)
            if '_es.md' in basename:
                print(f"Processing file: {f}")
                process_file(f)


def process_file(the_file):
    # open file
    my_file = open(the_file, 'r', encoding='utf-8')
    string_list = my_file.readlines()
    my_file.close()
    trans_dict = {'á': '&aacute;', 'é': "&eacute;", 'í': '&iacute;', 'ó': '&oacute;', 'ú': '&uacute;', 'ñ': '&ntilde;'}
    new_lines = []
    for line in string_list:
        if 'á' in line or 'é' in line or 'í' in line or 'ó' in line or 'ú' in line or 'ñ' in line:
            print(f"Original Line: {line}")
            trans_table = line.maketrans(trans_dict)
            line = line.translate(trans_table)
            print(f"Line after: {line}")
        new_lines.append(line)
    # write file
    my_file = open(the_file, "w", encoding='utf-8')
    new_file_contents = "".join(new_lines)
    my_file.write(new_file_contents)
    my_file.close()


if __name__ == "__main__":
    filename = input("Enter file name: ")
    fix(filename if filename.strip() is not '' else None)
