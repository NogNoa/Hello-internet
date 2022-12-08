report = open('GameFAQs.csv', 'r+')
linoi = report.readlines()
report = open('GameFAQs2.csv', 'w+')
for line in linoi:
    line = line.replace('\n', ',\n')
    line = line.split(',')
    date = line[3]
    date = date.split(' ')
    ln = len(date)
    if ln == 1:
        if not date[0] in {'date', 'TBA', 'Canceled'}:  # we're actually only looking for a year
            date = ['december', date[0]]
    elif date[0][0] == 'Q':  # the first charecter of the first word is Q, a quarter rather than day.
        quart = int(date[0][1])  # the second charecter is the number of the quarter
        month = 3 * quart
        date = [str(month), date[1]]
    date = '/'.join(date)
    line[3] = date
    line = ','.join(line)
    report.write(line)
