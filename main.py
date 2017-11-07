from pymongo import MongoClient

import json

# import our cassiopeia to make riot calls.
import cassiopeia as cass

from pprint import pprint

from cassiopeia import Summoner, Match
from cassiopeia.data import Season, Queue

def explor(account_id: int, summoner_id: int, summoner_name: str, region: str, level: int, db):
    if level == 0:
        return
    # Get the matchlist for the specified account id.
    summoner = Summoner(name=summoner_name, account=account_id, id=summoner_id, region=region)

    match_history = cass.get_match_history(summoner=summoner, seasons={Season.season_7}, queues={Queue.ranked_solo_fives})

    for match in match_history:
        gameId = match.id
        # fetch the specific game details.
        matchObject = {}
        matchObject['participants'] = []
        matchObject['teams'] = []
        matchObject['timelines'] = []

        for p in match.participants:
            newParticipantObject = {}
            for property, value in vars(p._data).items():
                newParticipantObject[property] = value
            matchObject['participants'].append(newParticipantObject)

        db.matches.insert_one({
                'match': matchObject
            })
        # for team in match.teams:

        # for timeline in match.timeline:


    return



def main():
    # set the configuration to our json.
    cass.apply_settings("configuration.json")

    # connect to MongoDB
    client = MongoClient("localhost:27017")

    # sets the database to timewinder.
    db = client.timewinder

    explor(account_id=40831277, summoner_id=26441012, summoner_name="NullCodex", region="NA", level=1, db=db)

if __name__ == "__main__":
    main()


