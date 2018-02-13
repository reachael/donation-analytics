import sys
import time
import os
import numpy as np
from datetime import datetime

def update_donors(donors, unique_donor, donation):
    """
    Function to update donors dict.
    If a donor has never donated before, add it to donors dict,
    else update the donars dict to make sure it stores the min year for that donor.
    """
    if unique_donor in donors:
        # update min year
        if donation[2] < donors[unique_donor]:
            donors[unique_donor] = donation[2]   
    else:
        # add to donor dict
        donors[unique_donor] = donation[2]

def update_recipients(recipients, recipient, donation):
    """
    Function to update recipients dict from repeat donor.
    If recipient does not have record, add it. 
    Otherwise add the donation to existing record.
    """
    amount = float(donation[3])
    # check the amount is integer or not, keep the original format
    if int(amount) == amount:
        amount = int(amount)

    if recipient in recipients:
        recipients[recipient].append(amount)
    else:
        recipients[recipient] = [amount]

def get_recipient_stats(recipients, recipient, PERCENTILE):
    """
    Function to get recipient's running stats if the donation
    is from repeat donor.
    """
    amounts = recipients[recipient]
    q = int(round(np.percentile(amounts,PERCENTILE,interpolation='lower')))
    return '|'.join([recipient, str(q), str(sum(amounts)), str(len(amounts))])

def is_valid_schema(CMTE_ID, NAME, ZIP_CODE, TRANSACTION_DT, TRANSACTION_AMT, OTHER_ID):
    """
    Function to check if the interesting fields are valid or not
    """
    if CMTE_ID=="" or NAME=="" or OTHER_ID is not "" or \
    len(ZIP_CODE)<5 or TRANSACTION_DT=="" or TRANSACTION_AMT=="":
        return False
    else:
        try:
            TRANSACTION_DT = datetime.strptime(TRANSACTION_DT,'%m%d%Y')
        except:
                return False
        return True

def save_file(data, output_file):
    """
    Function to write data to putput file.
    """
    f = open(output_file,'a')
    f.write("\n".join(data))
    f.write("\n")
    f.close()

def process_repeat_donations(PERCENTILE, input_file, output_file):
    """
    Main function to process donations in the input files.
    Label repeat donors and update recipients' donations stats.
    """    
    # donors dict stores the earliest year that a donor make a donation
    donors = dict()
    # recipients dict stores amounts from repeat donors
    recipients = dict()
    # store stats results for recipients
    results = []
    # the size of data to keep in buffer before iit writes to output file
    chunk_size = 1000
    count = 0
    context = open(input_file,"r")
    for line in context:
        record = line.split("|")
        CMTE_ID = record[0]
        NAME = record[7]
        ZIP_CODE = record[10]
        TRANSACTION_DT = record[13]
        TRANSACTION_AMT = record[14]
        OTHER_ID = record[15]
        # skip if the data is in bad format
        if is_valid_schema(CMTE_ID, NAME, ZIP_CODE, TRANSACTION_DT, TRANSACTION_AMT, OTHER_ID):
            ZIP_CODE = ZIP_CODE[:5]
            unique_donor= NAME + "|" + ZIP_CODE
            donation = [CMTE_ID, ZIP_CODE, datetime.strptime(TRANSACTION_DT,'%m%d%Y').year, TRANSACTION_AMT]           
            update_donors(donors, unique_donor, donation)
            # if the donation is from a repeat donor, update recipients dict and get stats
            if donation[2] > donors[unique_donor]:
                recipient = '|'.join([donation[0], donation[1], str(donation[2])])
                update_recipients(recipients, recipient, donation)
                results.append(get_recipient_stats(recipients, recipient, PERCENTILE))
                count+=1
                # if the buffer is full, write data to output file and empty buffer
                if count % chunk_size == 0:
                    save_file(results,output_file)
                    results = []
                    count = 0
       # skip if the fields are in bad format 
        else:
            continue
    # save the data to putput file since there is data in the buffer
    save_file(results,output_file)

def main(argv):
    start_time= time.time()
    # check if there is enough arguments
    if len(argv)!=4:
        raise ValueError("Please provide enough arguments!")
    input_file = argv[1]
    pct_file = argv[2]
    output_file = argv[3]
    try:
        PERCENTILE = float(open(pct_file, "r").read())
    except OSError:
        raise ValueError("Please provide correct percentile!")
    # remove output file if exists    
    try:
        os.remove(output_file)
    except OSError:
        pass
    process_repeat_donations(PERCENTILE, input_file, output_file)
    print ("total execution took "+"{0:.5f}".format(time.time()-start_time)+" seconds")

if __name__ == '__main__':
    main(sys.argv)    
