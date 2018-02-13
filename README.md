# Coding Summary

I used Python 2.7.12 for this coding challenge. In the challenge I used sys, time, os, numpy and datetime libraries.
There is one python script in the src directory, donation-analytics.py. To run the script, execute run.sh.

The script is to: 

1. Lable repeat donors and store the min year for a repeat donor. A donor ( use comnination of name and zip code) is defined as repeat donor if he have made donations in any prior years.
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

* recipient of the contribution (or `CMTE_ID` from the input file)
* 5-digit zip code of the contributor (or the first five characters of the `ZIP_CODE` field from the input file)
* 4-digit year of the contribution
* running percentile of contributions received from repeat donors to a recipient streamed in so far for this zip code and calendar year. Percentile calculations should be rounded to the whole dollar (drop anything below $.50 and round anything from $.50 and up to the next dollar) 
* total amount of contributions received by recipient from the contributor's zip code streamed in so far in this calendar year from repeat donors
* total number of transactions received by recipient from the contributor's zip code streamed in so far this calendar year from repeat donors