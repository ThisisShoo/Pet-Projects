"""Written by Shuhan Zheng

How to use:
1. Run this in any Python compiler, and follow the prompt
2. Copy the generated LaTeX code into your document
3. Profit!

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
||                   IMPORTANT NOTICE                       ||
||                                                          ||
||  If you encounter any problem, no matter how small,      ||
||  please visit https://github.com/ThisisShoo/Pet-Projects ||
||  and submit an issue there.                              ||
||                                                          ||
||  Your feedback will help MANY others!                    ||
||                                                          ||
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

"""
import csv

def convert_csv(file_name):
    """This function reads csv tables and converts them to LaTeX source codes that """
    begin_table = r'\begin{table}[H]' + '\n' + '    \centering' + '\n'
    begin_table += '    \caption{}' +'\n' + '    \\begin{tabular}[H]'

    with open(f'{file_name}', mode = 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        speci_cha = r'_^\\'
        content = []

        for row in reader:
            counter = 0
            for item in row:
                if any(cha in item for cha in speci_cha):
                    row[counter] = f'\({row[counter]}\)'
                counter += 1
            content.append(' '*8 + ' & '.join(row))

        col_def = "{" + "|l" * len(row) + "|}" + '\n' + ' ' * 8 + '\hline'

    data = (r'\\ \hline' + '\n').join(content) + r'\\ \hline' + "\n"
    begin_table += col_def + '\n'
    end_table = "    \end{tabular}" + "\n" + r'\end{table}'

    print ('\n' + begin_table + data + end_table)

FILE_NAME = input("""Enter the file's path and name, including ".csv". Type "cancel" to cancel: """)


if FILE_NAME == 'cancel':
    print ('\n' + 'Cancelled')
else:
    convert_csv(FILE_NAME)

print('\n' + 'You can now copy the latex source code above and add it to your document' + '\n')
