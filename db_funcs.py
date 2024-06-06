import sqlite3
import csv

def create_tables():
    commands = [
    '''\
    CREATE TABLE ActiveAssociateBrokers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        LastName TEXT,
        FirstName TEXT,
        MiddleName TEXT,
        Suffix TEXT,
        EntityName TEXT,
        DBA TEXT,
        AddressLine1 TEXT,
        AddressLine2 TEXT,
        City TEXT,
        State TEXT,
        County TEXT,
        ZipCode TEXT,
        Phone TEXT,
        CredentialTypePrefix TEXT,
        CredentialNumber INTEGER,
        SupervisionStart DATE,
        LicenseFirstIssueDate DATE,
        LicenseExpirationDate DATE,
        Status TEXT
    );
    ''',
    '''\
    CREATE TABLE ActiveHOAs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        BusinessName TEXT,
        DesignatedAgent TEXT,
        CredentialTypePrefix TEXT,
        CredentialNumber INTEGER,
        LicenseFirstIssueDate DATE,
        LicenseLastRenewedDate DATE,
        LicenseExpirationDate DATE,
        Attention TEXT,
        AddressLine1 TEXT,
        AddressLine2 TEXT,
        City TEXT,
        State TEXT,
        County TEXT,
        ZipCode TEXT,
        Description TEXT,
        Managed TEXT,
        Units INTEGER,
        ManagementCompany TEXT
    );
    ''',
    '''\
    CREATE TABLE ActiveIndividualProprietors(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        LastName TEXT,
        FirstName TEXT,
        MiddleName TEXT,
        Suffix TEXT,
        DBA TEXT,
        AddressLine1 TEXT,
        AddressLine2 TEXT,
        City TEXT,
        State TEXT,
        County TEXT,
        MailZipCode TEXT,
        MailZipCodePlus4 TEXT,
        Phone TEXT,
        LicenseType TEXT,
        LicenseNumber INTEGER,
        SupervisionStart DATE,
        LicenseFirstIssueDate DATE,
        LicenseLastRenewedDate DATE,
        LicenseExpirationDate DATE,
        Status TEXT
        );
    ''',
    '''\
    CREATE TABLE ActiveRealEstateCompanies(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        EntityName TEXT,
        DBA TEXT,
        SupervisorName TEXT,
        CredentialTypePrefix TEXT,
        CredentialNumber INTEGER,
        SupervisionStart DATE,
        LicenseFirstIssueDate DATE,
        AddressLine1 TEXT,
        AddressLine2 TEXT,
        City TEXT,
        State TEXT,
        County TEXT,
        ZipCode TEXT,
        Phone TEXT,
        Status TEXT
    );
    ''',
    '''\
    CREATE TABLE ActiveResponsibleBrokers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        LastName TEXT,
        FirstName TEXT,
        MiddleName TEXT,
        Suffix TEXT,
        EntityName TEXT,
        DBA TEXT,
        CredentialTypePrefix TEXT,
        CredentialNumber INTEGER,
        SupervisionStart DATE,
        LicenseFirstIssueDate DATE,
        LicenseLastRenewedDate DATE,
        LicenseExpirationDate DATE,
        AddressLine1 TEXT,
        AddressLine2 TEXT,
        City TEXT,
        State TEXT,
        County TEXT,
        ZipCode TEXT,
        Phone TEXT,
        Status TEXT
    );
    ''',
    '''\
    CREATE TABLE ActiveSubdivisionDevelopers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        BusinessName TEXT,
        SupervisorName TEXT,
        CredentialTypePrefix TEXT,
        CredentialNumber INTEGER,
        LicenseFirstIssueDate DATE,
        LicenseLastRenewedDate DATE,
        LicenseExpirationDate DATE,
        Attention TEXT,
        AddressLine1 TEXT,
        AddressLine2 TEXT,
        City TEXT,
        State TEXT,
        County TEXT,
        ZipCode TEXT,
        Description TEXT
    );
    ''',
    '''\
    CREATE TABLE ElPasoCountyParcels(
        LastUpdate DATE,
        PARCEL INTEGER PRIMARY KEY,
        LOCATION TEXT,
        LOCATIONZIP TEXT,
        PLATINUM TEXT,
        PARTIALLEGAL TEXT,
        CmntyArea TEXT,
        SchoolDist TEXT,
        ZONING TEXT,
        MARKETVALUE FLOAT,
        ASSESSEDVALUE FLOAT,
        LANDCODE INTEGER,
        LANDCODESCR TEXT,
        Acreage FLOAT,
        IMPCOUNT INTEGER,
        IMPSTATECODE INTEGER,
        IMPSTATEDESCR TEXT,
        IMPLOCALCODE INTEGER,
        IMPLOCALDESCR TEXT,
        YearBlt TEXT,
        UNITS FLOAT,
        RESSTYLE TEXT,
        Rooms FLOAT,
        Beds FLOAT,
        Baths FLOAT,
        TotalFinishedArea FLOAT,
        TotalBSMT FLOAT,
        FinishedBSMT FLOAT,
        IMPSQFT FLOAT,
        SALEDATE FLOAT,
        SALEPRICE FLOAT,
        AsrSaleCmnt TEXT,
        OWNER1 TEXT,
        OWNER2 TEXT,
        OWNER3 TEXT,
        MAILADR TEXT,
        MAILCITY TEXT,
        MAILSTATE TEXT,
        MAILZIPCODE TEXT
    );
    ''']

    conn = sqlite3.connect('./real_estate_info.db')
    cursor = conn.cursor()
    for command in commands:
        cursor.execute(command)
    conn.commit()
    cursor.close()

def populate_tables():
    def replace_ending_comma(file_path:str):
        with open(file_path, 'r') as f:
            contents = f.read().replace(',\n', '\n')
        with open(file_path, 'w') as f:
            f.write(contents)
    def active_ass():
        conn = sqlite3.connect('./real_estate_info.db')
        cursor = conn.cursor()
        fpath = './csv_files/active_associate_brokers.csv'
        replace_ending_comma(fpath)
        with open(fpath, 'r') as f:
            csv_cont = csv.reader(f)
            insert_statement = 'INSERT INTO ActiveAssociateBrokers (LastName, FirstName, MiddleName, Suffix, EntityName, DBA, AddressLine1, AddressLine2, City, State, County, ZipCode, Phone, CredentialTypePrefix, CredentialNumber, SupervisionStart, LicenseFirstIssueDate, LicenseExpirationDate, Status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            cursor.executemany(insert_statement, csv_cont)
        conn.commit()
        conn.close()
    def active_hoa():
        conn = sqlite3.connect('./real_estate_info.db')
        cursor = conn.cursor()
        with open('./csv_files/active_hoa.csv', 'r') as f:
            contents = csv.reader(f)
            insert_statement = 'INSERT INTO ActiveHOAs (BusinessName, DesignatedAgent, CredentialTypePrefix, CredentialNumber, LicenseFirstIssueDate, LicenseLastRenewedDate, LicenseExpirationDate, Attention, AddressLine1, AddressLine2, City, State, County, ZipCode, Description, Managed, Units, ManagementCompany) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            cursor.executemany(insert_statement, contents)
        conn.commit()
        conn.close()
    def active_prop():
        conn = sqlite3.connect('./real_estate_info.db')
        cursor = conn.cursor()
        replace_ending_comma('./csv_files/active_individual_proprietors.csv')
        with open('./csv_files/active_individual_proprietors.csv', 'r') as f:
            contents = csv.reader(f)
            insert_statement = 'INSERT INTO ActiveIndividualProprietors (LastName, FirstName, MiddleName, Suffix, DBA, AddressLine1, AddressLine2, City, State, County, MailZipCode, MailZipCodePlus4, Phone, LicenseType, LicenseNumber, SupervisionStart, LicenseFirstIssueDate, LicenseLastRenewedDate, LicenseExpirationDate, Status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            cursor.executemany(insert_statement, contents)
        conn.commit()
        conn.close()
    def active_companies():
        conn = sqlite3.connect('./real_estate_info.db')
        cursor = conn.cursor()
        replace_ending_comma('./csv_files/active_real_estate_companies.csv')
        with open('./csv_files/active_real_estate_companies.csv', 'r') as f:
            contents = csv.reader(f)
            insert_statement = 'INSERT INTO ActiveRealEstateCompanies (EntityName, DBA, SupervisorName, CredentialTypePrefix, CredentialNumber, SupervisionStart, LicenseFirstIssueDate, AddressLine1, AddressLine2, City, State, County, ZipCode, Phone, Status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            cursor.executemany(insert_statement, contents)
        conn.commit()
        conn.close()
    def active_responsible():
        conn = sqlite3.connect('./real_estate_info.db')
        cursor = conn.cursor()
        replace_ending_comma('./csv_files/active_responsible_brokers.csv')
        with open('./csv_files/active_responsible_brokers.csv', 'r') as f:
            contents = csv.reader(f)
            insert_statement = 'INSERT INTO ActiveResponsibleBrokers (LastName, FirstName, MiddleName, Suffix, EntityName, DBA, CredentialTypePrefix, CredentialNumber, SupervisionStart, LicenseFirstIssueDate, LicenseLastRenewedDate, LicenseExpirationDate, AddressLine1, AddressLine2, City, State, County, ZipCode, Phone, Status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            cursor.executemany(insert_statement, contents)
        conn.commit()
        conn.close()
    def active_developers():
        conn = sqlite3.connect('./real_estate_info.db')
        cursor = conn.cursor()
        replace_ending_comma('./csv_files/active_subdivision_developers.csv')
        with open('./csv_files/active_subdivision_developers.csv', 'r') as f:
            contents = csv.reader(f)
            insert_statement = 'INSERT INTO ActiveSubdivisionDevelopers (BusinessName, SupervisorName, CredentialTypePrefix, CredentialNumber, LicenseFirstIssueDate, LicenseLastRenewedDate, LicenseExpirationDate, Attention, AddressLine1, AddressLine2, City, State, County, ZipCode, Description) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            cursor.executemany(insert_statement, contents)
        conn.commit()
        conn.close()
    def parcels():
        conn = sqlite3.connect('./real_estate_info.db')
        cursor = conn.cursor()
        replace_ending_comma('./csv_files/filtered_epc_parcels.csv')
        with open('./csv_files/filtered_epc_parcels.csv', 'r') as f:
            contents = list(csv.reader(f))
            print(len(contents))
            filtered_contents = [x for x in contents if len(x) == 39]
            print(len(filtered_contents))
            insert_statement = 'INSERT INTO ElPasoCountyParcels (LastUpdate, PARCEL, LOCATION, LOCATIONZIP, PLATINUM, PARTIALLEGAL, CmntyArea, SchoolDist, ZONING, MARKETVALUE, ASSESSEDVALUE, LANDCODE, LANDCODESCR, Acreage, IMPCOUNT, IMPSTATECODE, IMPSTATEDESCR, IMPLOCALCODE, IMPLOCALDESCR, YearBlt, UNITS, RESSTYLE, Rooms, Beds, Baths, TotalFinishedArea, TotalBSMT, FinishedBSMT, IMPSQFT, SALEDATE, SALEPRICE, AsrSaleCmnt, OWNER1, OWNER2, OWNER3, MAILADR, MAILCITY, MAILSTATE, MAILZIPCODE) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            cursor.executemany(insert_statement, filtered_contents)
        conn.commit()
        conn.close()
    active_ass()
    active_hoa()
    active_prop()
    active_companies()
    active_responsible()
    active_developers()
    parcels()

def query_database(sql_statement:str, condition_values:list|None=None):
    conn = sqlite3.connect('/Users/bryanjsample/Documents/code/github/hoa_prop_managers/real_estate_info.db')
    cursor = conn.cursor()
    cursor.execute(sql_statement, condition_values)
    results = cursor.fetchall()
    cursor.close()
    return results

if __name__ == "__main__":
    populate_tables()