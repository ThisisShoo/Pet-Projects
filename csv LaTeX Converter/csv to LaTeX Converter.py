"""Written by Shuhan Zheng"""
import csv

def covert_csv(file_name):
    """This function reads csv tables and converts them to LaTeX source codes that """
    print (r'\begin{tabular}[H]')
    print ('    ')
    with open(f'{file_name}', mode = 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        output = ''
        for row in reader:
            print (' ')
            rowtext = ' & '.join(row)
            rowtext = '    ' + rowtext + ' \\\\ ' + r'\\hline' + ' \\\\'

            output += rowtext
            print (rowtext)
        print (r'\end{tabular}')
    #return output

filename = input('Enter the file name, including ".csv". Type "cancel" to cancel:')
if filename == 'cancel':
    print ('Cancelled')
else:
    covert_csv(filename)

print('You can now copy the latex source code above and add it to your document')
