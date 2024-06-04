import csv

def main():
    with open('./csv_files/filtered_epc_parcels.csv', 'r') as f:
        contents = csv.reader(f)
        for count, i in enumerate(contents):
            if len(i) != 39:
                print(len(i), count, sep='  |  ')

if __name__ == "__main__":
    main()