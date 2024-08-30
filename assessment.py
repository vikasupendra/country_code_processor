import csv
import sys 
import re
import argparse

class CountryCodeProcessor():
    def __init__(self, file_path: str):
        self.csv_file_path = file_path
        self.csv_rows = []
        self.csv_headers = []
        self.country_abbrv_list = []        

    def get_csv_headers(self) -> list[str]:

        try:
            csv_file_obj = open(self.csv_file_path, 'r', newline = '')
           
            file_content = csv.DictReader(csv_file_obj)

            dict_from_csv = dict(list(file_content)[0])
            self.csv_headers = list(dict_from_csv.keys())
            return self.csv_headers

        except IOError as e:
            print ("I/O error({}): {}".format(e.errno, e.strerror))

        except:                                                             #handle other exceptions such as attribute errors
            print ("Unexpected error:", sys.exc_info()[0])        

    def read_csv(self) -> None:

        try:
            csv_file_obj = open(self.csv_file_path, 'r', newline = '')            
            file_content = csv.DictReader(csv_file_obj)
            
            self.get_csv_headers()

            self.csv_rows = [row for row in file_content]
        
            csv_file_obj.close()

        except IOError as e:
            print ("I/O error({}): {}".format(e.errno, e.strerror))

        except:                                                             #handle other exceptions such as attribute errors
            print ("Unexpected error:", sys.exc_info()[0])

    def write_csv(self, output_file_path: str) -> None:

        len_abbreviated_countries = len(self.country_abbrv_list)
        len_csv_rows = len(self.csv_rows)

        if len_abbreviated_countries != len_csv_rows:
            raise Exception("length of abbreviated countries list is NOT the same as original CSV row list !!")

        try:
            out_csv_file = open(output_file_path, 'w', newline = '')

            # append new header
            self.csv_headers.append('country_abbreviation')

            csv_file_op = csv.DictWriter(out_csv_file, fieldnames = self.csv_headers)

            csv_file_op.writeheader()                       # write headers to CSV first

            for i in range(len_abbreviated_countries):
                self.csv_rows[i]['country_abbreviation'] = self.country_abbrv_list[i]
                csv_file_op.writerow(self.csv_rows[i])
        
        except IOError as e:
            print ("I/O error({}): {}".format(e.errno, e.strerror))

        except: #handle other exceptions such as attribute errors
            print ("Unexpected error:", sys.exc_info()[0])

    def get_country_abbreviations(self) -> list[str]:
        
        len_csv_rows = len(self.csv_rows)

        if len_csv_rows == 0:
            raise Exception("CSV file content is EMPTY !!")
        
        for row in self.csv_rows:

            words_in_country_col = re.split('\s|\(|\)|\, |\.|\-', row['country'])
            
            country_abbrv = ''

            if len(words_in_country_col) == 1:                                       # case where country name is just ONE word
                    len_country_value = len(words_in_country_col[0])
                    country_abbrv = words_in_country_col[0][:2].upper() + words_in_country_col[0][-1].upper()

            else:                                                                    # case where country name is multiple words
                for word in words_in_country_col:
                
                    if word and not word.isspace() and word[0].isalpha():            # check if the split word in country column is NOT a space and atleast the 1st character of a country is an alphabet
                        country_abbrv = country_abbrv + word[0].upper()

            self.country_abbrv_list.append(country_abbrv)

        return self.country_abbrv_list

def main():

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--input_csv_path', help = 'Input CSV file path')
    parser.add_argument('--output_csv_path', help = 'Output CSV file path')

    args = parser.parse_args()
    input_file_path = args.input_csv_path
    output_file_path = args.output_csv_path

    obj = CountryCodeProcessor(input_file_path)
    obj.read_csv()
    obj.get_country_abbreviations()
    obj.write_csv(output_file_path)

if __name__ == "__main__":
   main()