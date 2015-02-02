
// README.txt

---------------------- get_users.py -------------------------------------------------------------------------------------

* got users from wefollow, twellow, tweepz and stored their usernames, categories, and source(s) in file called "udr.csv" 

---------------------- ReligionTweets.java ------------------------------------------------------------------------------

* retrieved all tweets from users in "user_data_religion.csv" and put them in a textfile called "udr.txt"

---------------------- filtertweets.py ----------------------------------------------------------------------------------

* filtered out foreign languages / bad data from "udr.txt" and put the good data in "religiontweets_cleaned.txt"

---------------------- txt_to_csv.py ------------------------------------------------------------------------------------

* converted "religiontweets_cleaned.txt" to "religiontweets_cleaned.csv"

---------------------- religion_chisquare.py ----------------------------------------------------------------------------

* used "religiontweets_cleaned.csv" and "user_data_religion.csv" (which has each user's category info) to get chi square 
values for each category

* wrote the results into "religion_chisquare.csv"
