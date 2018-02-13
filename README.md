# Coding Summary

I used Python 2.7.12 for this coding challenge. In the challenge I used sys, time, os, numpy and datetime libraries.There is one python script in the src directory, that is donation-analytics.py. To run the script, execute run.sh.

The script is to: 

1. Lable repeat donors and store the min year for a repeat donor. A donor (defined as comnination of name and zip code) is defined as repeat donor if he has made donations in any prior years.
2. For each recipient, zip code and calendar year combination, calculate these three values for contributions coming from repeat donors:

* total dollars received
* total number of contributions received 
* donation amount in a given percentile

## Input files

1. `percentile.txt`, holds a single value -- the percentile value (1-100) that will be used to calculate running percentile.

2. `itcont.txt`, has a line for each campaign contribution that was made on a particular date from a donor.

In the itcont.txt file, the following fields are useful:

* `CMTE_ID`: recipient of this contribution
* `NAME`: name of the donor
* `ZIP_CODE`:  zip code of the contributor (we only want the first five digits/characters)
* `TRANSACTION_DT`: date of the transaction
* `TRANSACTION_AMT`: amount of the transaction
* `OTHER_ID`: a field that denotes whether contribution came from a person or an entity 

## Output file

Data is stored in `repeat_donors.txt`, Each line of this file contain these fields:

* recipient of the contribution 
* 5-digit zip code of the contributor 
* 4-digit year of the contribution
* running percentile of contributions received from repeat donors to a recipient streamed in so far for this zip code and calendar year
* total amount received by recipient from the contributor's zip code streamed in so far in this calendar year from repeat donors
* total number of transactions received by recipient from the contributor's zip code streamed in so far this calendar year from repeat donors

## Brief description of approches

`process_repeat_donations` is the main function where I use donors and recipients dictionaries to track history of donors and recipients. 

Donors dictionary stores a donor ( defined as combination of name and zipcode) and the corresponding min year he made donations in so far from streaming data. 

Recipients dictionary stores a recipient (defined as combination of cmte_id, zipcode and transaction year) and contribution amounts from repeat donors ( defined as donors who made any donations in any prior year) in so far from streaming data. 

First, read data from input file, valid the data with `is_valid_schema` function. If the data is valid, update the donors dictionary with `update_donors` function, otherwise skip the record. Then check if the donation is from repeat donor or not. If it is then use `update_recipients` and `get_recipient_stats` functions to update recipients dictionary and return the recipient's stats described in the Output file part. While processing the data, I store the stats in the buffer before it is full. Use `save_file` function to save data to output file and empty the buffer when it is full. 
