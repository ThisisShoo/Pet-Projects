"""Written by Shuhan Zheng"""
import csv

def convert_csv(file_name):
    """This function reads csv tables and converts them to LaTeX source codes that """
    begin_table = r'\begin{table}[H]' + '\n' + '    \centering' + '\n' + '    \caption{}' +'\n' + '    \\begin{tabular}[H]'
    
    with open(f'{file_name}', mode = 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        content = []

        for row in reader:
            content.append(' '*8 + ' & '.join(row))

        col_def = "{" + "|l" * len(row) + "|}"

    data = (r'\\ \hline' + '\n').join(content) + "\n"
    begin_table += col_def + '\n'
    end_table = "    \end{tabular}" + "\n" + r'\end{table}'

    print (begin_table + data + end_table)

filename = input('Enter the file name, including ".csv". Type "cancel" to cancel:')

if filename == 'cancel':
    print ('Cancelled')
else:
    convert_csv(filename)

print('You can now copy the latex source code above and add it to your document')
