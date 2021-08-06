import os
import plotly.graph_objects as go
import plotly.express as px

import helpers.utils
import vars
import jsonlines
from helpers import utils
import dash_table
import pandas as pd
import hashlib
import logging
import json
from datetime import datetime


def create_histogram():
    logger = logging.getLogger('sc-evtx-parser')
    logger.setLevel(logging.DEBUG)
    data = dict({"date": [], "total": []})
    _all = utils.retrieve_all_events()
    for item in utils.retrieve_all_events():

        time_string = item['data']["Event"]["System"]["TimeCreated"]["#attributes"]["SystemTime"]
        utc_dt = datetime.fromisoformat(time_string.replace('Z', '+00:00'))
        data["date"].append(utc_dt)
        data["total"].append(1)

    df = pd.DataFrame(data, columns=data.keys())
    fig = px.histogram(df, x="date", y="total", histfunc="count", title="all events")

    return fig
