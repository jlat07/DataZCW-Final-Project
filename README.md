# NLP Covid-19 Sentiment Pipeline

For our final project at Zip Code Wilmington, we chose to utilize our skills to extract data from News Api articles, and process tweets from Twitter's streaming API using Kafka. We store that data into a Database, then clean the data with Spark. Run the data through an NLP model to determine sentiment. Finally view the outcome on a custom Dashboard.  

![Pipeline](Images/NLP_covid_pipeline2.png) 
  
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
  
  
  
