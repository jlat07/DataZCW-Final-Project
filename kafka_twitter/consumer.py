from kafka import KafkaConsumer, TopicPartition
from json import loads
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker


consumer = KafkaConsumer(
    'tweet_stream',
     bootstrap_servers=['localhost:9092'],
     value_deserializer=lambda m: loads(m.decode('ascii')))


engine = create_engine('mysql+pymysql://root:zipcoder@localhost/twitter')

Base = declarative_base()
class Tweets(Base):
    __tablename__ = 'twitter_stream'
    tweet_id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(250))
    text = Column(String(250))
    location = Column(String(250))
    bounding = Column(String(300))
    time_stamp  = Column(Integer)
    state = Column(String(300))

states = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AS': 'American Samoa',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'GU': 'Guam',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MP': 'Northern Mariana Islands',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NA': 'National',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'PR': 'Puerto Rico',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VI': 'Virgin Islands',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
}


def get_state(loc_name):
    locs = loc_name.split(",")
    if len(locs) > 1:
        if "USA" == locs[1].strip():
            return locs[0]
        elif locs[1].strip() in states.keys(): 
            return states.get(locs[1].strip())



for message in consumer:
    message = message.value
    full_name = get_state(message.get("place").get("full_name"))
    if full_name is not None:
        print("received")
        tweet_id = message.get("id")
        name = message.get("user").get("name")
        text = message.get("text")
        place = message.get("place")
        location = place.get("full_name")
        bounding = str(place.get("bounding_box").get("coordinates"))
        time_stamp = message.get("timestamp_ms")
        state = full_name
        message_sql = Tweets(tweet_id=tweet_id, name=name, text=text, location = location, bounding= bounding, time_stamp = time_stamp, state = state)
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(message_sql)
        session.commit()

