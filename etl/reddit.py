import sys

import numpy as np
import pandas as pd
import praw
from praw import Reddit

def connect_reddit(client_id, client_secret, user_agent) -> Reddit:
    try:
        reddit = praw.Reddit(client_id=client_id,
                             client_secret=client_secret,
                             user_agent=user_agent)
        print("Connection Established !")
        return reddit
    except Exception as e:
        print(e)
        sys.exit(1)
