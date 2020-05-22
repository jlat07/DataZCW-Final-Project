# NLP Covid-19 Sentiment Pipeline

For our final project at Zip Code Wilmington, we chose to create a sentiment anlayis on COVID-19 for two different sources, the News API and Twitter API. For the news api we will be using Airflow to gather new articles every hour regarding COVID-19. For the Twitter API we have used Kafka to produce a stream of all tweets regarding COVID-19. 

After aquiring this data we run it through a Vader model to analyze sentiment of the media and store it in a SQL database. Using airflow we will continously clean the data and and show our results using various visualization tools. Check out our pipeline below.  

![Pipeline](Images/Pipeline.png) 
  
To run this program we ask you execute the follow steps.

-Set up a dotenv file with the approriate keys for News API and Twitter API

-Change your directory to StartFile and run the follow commands on your command line:

- Add your dotenv file to this folder 
- "mysql -u username -p < TwitterSetup.sql"
- "mysql -u username -p < NewsSetup.sql"
- "python start.py"

-From the airflow_dag directory add the file "final_project_dag.py" to your airflow home in the dags folder as well as set up your dotenv file in the same folder. Start airflow webserver and scheduler and turn on the final_project_dag.

-Change directory to the twitter_kafka folder and start running your kafka zookeeper and server. After that run both conusmer.py and producer.py simultaneously

-For viusalizations please run the 2 Plotly Dash Apps in the Final_Project/Dashboard/py_files and open local hosts. Also for for a basic visualization report launch the Jupyter Notebook report_df.

___
*(original project requirements below)*  
  
## DataZCW-Final-Project
capstone project for ZCW Data's course.

### Final Group Project Possibles

- How To Build a Neural Network to Recognize Handwritten Digits with TensorFlow
  - ye olde scanning chestnut
  - handwriting recognition
- Image Processing for Feature Identification
  - "Hot dog or not" but for X
- Sentiment Analysis
  - From twitter feeds
  - From facebook feeds
  - Or?
  - provides realtime view of crowdsourced "zeitgeist" on a hot topic
- Recommendation Engine
  - Music, Books, Wine, TV/Movies, Sports
  - if you like X, you'll like Y
- Search Engine of Documents, DataSets, APIs?? (Map/reduce)
  - Google lite
  - Google images
  - popularity or relevance measures

### Group Size

Each group should 2-4 people. Effort should be mostly
Data Engineering, but at the end, do some actaul Data Science.
So a model, or prediction, or something based on the data that
has flowed through the project.

EACH person must have a clear understanding of everything in the project.
Each person should have parts they alone have done, something they've explained to their teammates.

Each team must have single repo, (with NO creds stored anywhere), use the Github tools
for obvious tracking purposes:
- Lots of commits on several branches
- Use of the Issues tab for tracking things being worked on
- Use a project board to handle group comms on task assignments

_We need this project to be clean and cool and clear about what you can do. Your hiring managers
will want to look through it and then be prepped to ask you questions about almost anything within
the project. You should be able to answer those questions._

## Required stages

- Identify Scope of Project
  - Find APIs that could help
  - Find DataSets that might be useful
- ProjectReadme.md file that gives a good high-level description of project.
- Each project should have
  - 2 or more piplines that collect data from sources
    - Extra bonus for "streaming api" usage
  - A cache sql/nosql database that acts as a data lake
  - A series of Spark drivers that wrangle the data into a final form
  - Final data stored back in the cache database
  - A Data Viz and/or Dashbord showing the analysis done (of the data flows)
- A Model which makes some prediction based on the data
  - a ad-hoc prediction request
  - or other insight into the data
- Some documentation in the project's README (along with some PNGs of the results)
- Make it pretty.
- Add a "slide deck" of project work, overall structure, and status of milestones.
  
  ### Tech choices
  
  All tech choices will be approved by instructors. 
  Any tech we've studied is fair game for use.
  All project must have some **Airflow** portion AND some **Spark** portion somewhere within the project.
  All projects must have some python scripts, SQL/NoSQL database, and make use of some data visualization outputs and
  kind of dashboard. (You may use any dashboard tech that is cleared with instrutors).
  
  
  
