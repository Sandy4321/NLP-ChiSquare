import twitter4j.Paging;
import twitter4j.RateLimitStatus;
import twitter4j.Status;
import twitter4j.Twitter;
import twitter4j.TwitterException;
import twitter4j.TwitterFactory;

import java.util.List;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.io.File;
import java.io.FileReader;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.FileNotFoundException;
import java.util.ArrayList;

public class PoliticsTweets
{

	/**
	 * MAIN CLASS
	 * @param args
	 * @throws TwitterException
	 */
	public static void main(String args[]) throws TwitterException
	{
		ArrayList<String> userHandles = getHandles();

		for(int i = 0; i < userHandles.size(); i++)
		{
			writeTweets(userHandles.get(i));
			try
			{
				Thread.sleep(6000);
			} catch (InterruptedException e)
			{
				e.printStackTrace();
			}
		}
		System.out.print("Success.");

	}

	/**
	 * writeTweets -
	 * @param handle
	 * @throws TwitterException
	 */
	public static void writeTweets(String handle) throws TwitterException
	{
		Twitter twitter = new TwitterFactory().getInstance();
		PrintWriter out = null;
		File f = new File("../udp.txt");

		try
		{
			List<Status> statuses;
			Paging page = new Paging (1, 50);//page number, number per page

            // get statuses for each user
            statuses = twitter.getUserTimeline(handle, page);

			// create PrintWriter object
			out = new PrintWriter(new FileWriter(f, true));

			// write user's tweets to the output file
            for (Status status : statuses)
            {
                out.print("@" + status.getUser().getScreenName() + " - " + status.getText());
                out.printf("\n");
            }
            out.printf("\n----------------------------------------------------------------------\n\n");
		}
		catch(FileNotFoundException fe)
		{
			System.out.println(fe);
		}
		catch(TwitterException te)
		{
			te.printStackTrace();
			System.err.println("Failed to get timeline: " + te.getMessage());
		}
		catch (IOException e)
		{
			System.err.println("IO exception.");
		}
		finally
		{
			if (out != null)
				out.close();
		}

	}


	/**
	 * getHandles - returns ArrayList of handles (called usernames)
	 * @return
	 */
	public static ArrayList<String> getHandles()
	{
		String csvFile = "../user_data_politics.csv";
		BufferedReader br = null;
		String line = "";
		String cvsSplitBy = ",";
		String[] userInfo;
		ArrayList<String> usernames = new ArrayList<String>();

		try
		{
			br = new BufferedReader(new FileReader(csvFile));
			while ((line = br.readLine()) != null)
			{
			     // use comma as separator to create array of user info
				if (!line.startsWith("@")) continue;
				userInfo = line.split(cvsSplitBy);
				usernames.add(userInfo[0]);
			}

		}
		catch (FileNotFoundException e)
		{
			e.printStackTrace();
		}
		catch (IOException e)
		{
			e.printStackTrace();
		}
		finally
		{
			if (br != null)
			{
				try
				{
					br.close();
				}
				catch (IOException e)
				{
					e.printStackTrace();
				}
			}
		}

		return usernames;
	}
}
