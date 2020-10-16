from pyexcel.cookbook import merge_all_to_a_book
import glob

# Convert from CSV to Excel
filename_csv = 'Nbook Scraping Alappuzha.csv'
filename_excel = 'Nbook Scraping Alappuzha.xlsx'
merge_all_to_a_book(glob.glob(filename_csv), filename_excel)