### Code to get Hourly Solar Radiation from Day Solar Rad.

### Read SR data
def read_SR_daily_data(day, tss):
    sr_db = []
    with open('SR_data_2019.csv', 'r') as file:
        # (1)date, (2)SR
        reader3 = csv.reader(file)
        next(reader3)
        #OutputList = [map(float, list(i)) for i in zip(*reader)]
        for row in reader3:
            sr1 = row[1:]
            sr2 = map(float, list(sr1))
            sr_db.append(sr2[1])
            #print(sr2)

        print "L57 SR data length:",len(sr_db)
        #print (sr_db)
    return sr_db
### --------- End: Read SR data -----------------


if __name__ == "__main__":
    # Input data
    #list_input = input_data()

    sr_day = 6.802
    sunset = 16.5
    SR_hourly = read_SR_daily_data(sr_day, sunset)
    print "Solar-angle ; Azimut-angle:"
    print SR_hourly

    print "donee..."
