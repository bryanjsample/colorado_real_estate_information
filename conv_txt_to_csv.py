
def main():
    with open('./csv_files/epc_parcels.txt', 'rb') as f:
        contents = f.read().decode('ISO-8859-1')

    lines = contents.splitlines()
    with open('./csv_files/epc_parcels1.csv', 'a') as nf:
        for line in lines:
            split_by_tab = line.split('\t')
            new_line = []
            for item in split_by_tab:
                new_item = '"' + item + '"'
                new_line.append(new_item)
            new_line_str = ','.join(new_line) + '\n'
            nf.write(new_line_str)

if __name__ == "__main__":
    main()