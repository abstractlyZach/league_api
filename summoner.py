import json

import exceptions
import utils


class Summoner:
    def __init__(self, summoner_info_dict):
        self._id = summoner_info_dict['id']
        self._account_id = summoner_info_dict['accountId']
        self._name = summoner_info_dict['name']
        self._profile_icon_id = summoner_info_dict['profileIconId']
        self._revision_date = summoner_info_dict['revisionDate']
        self._summoner_level = summoner_info_dict['summonerLevel']

    @property
    def id(self):
        return self._id

    @property
    def account_id(self):
        return self._account_id

    @property
    def name(self):
        return self._name

    @property
    def profile_icon_id(self):
        return self._profile_icon_id

    @property
    def revision_date(self):
        return self._revision_date

    @property
    def summoner_level(self):
        return self._summoner_level

    def __str__(self):
        format_string = 'Name       : {name}\n' \
                        'Summoner ID: {summoner_id}\n' \
                        'Account ID : {account_id}\n'
        return format_string.format(name=self._name,
                                    summoner_id=self._id,
                                    account_id=self._account_id)


class RankedInfo:
    def __init__(self, ranked_dict):
        self._queue_type = ranked_dict['queueType']
        self._tier = ranked_dict['tier']
        self._rank = ranked_dict['rank']
        self._league_points = ranked_dict['leaguePoints']
        self._wins = ranked_dict['wins']
        self._losses = ranked_dict['losses']

    @property
    def queue_type(self):
        return self._queue_type

    @property
    def ranked_level(self):
        return '{} {}'.format(self._tier, self._rank)

    @property
    def tier(self):
        return self._tier

    @property
    def rank(self):
        return self._rank

    @property
    def league_points(self):
        return self._league_points

    @property
    def wins(self):
        return self._wins

    @property
    def losses(self):
        return self._losses

    def __str__(self):
        format_string = '{queue_type}\n' \
                        '{ranked_level}\n' \
                        '{wins:>3} wins\n' \
                        '{losses:>3} losses\n'
        return format_string.format(queue_type=self.queue_type,
                                    ranked_level=self.ranked_level,
                                    wins=self.wins,
                                    losses=self.losses)


def get_summoner_info(name):
    """Retrieves the summoner info for a summoner name in NA"""
    if not utils.validate_summoner_name(name):
        raise exceptions.InvalidSummonerNameException('Name is invalid: {}'.format(name))
    request_url = 'https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/{}'.format(name)
    response = utils.make_request(request_url)
    if response.ok:
        response_dict = json.loads(response.text)
        return Summoner(response_dict)
    else:
        utils.handle_response_error(response)


def get_summoner_mastery_by_id(summoner_id):
    """Returns the total champion mastery score for the given summoner_id"""
    request_url = 'https://na1.api.riotgames.com/lol/champion-mastery/v3/scores/by-summoner/{}'.format(summoner_id)
    response = utils.make_request(request_url)
    if response.ok:
        return int(response.text)
    else:
        utils.handle_response_error(response)


def get_ranked_info(summoner_id):
    """Returns a list of RankedInfo objects for the given summoner_id"""
    request_url = 'https://na1.api.riotgames.com/lol/league/v3/positions/by-summoner/{}'.format(summoner_id)
    response = utils.make_request(request_url)
    if response.ok:
        ranked_info_list = response.json()
        return [RankedInfo(ranked_info_item) for ranked_info_item in ranked_info_list]
    else:
        utils.handle_response_error(response)

me = get_summoner_info('exzacktlee')
ranked_infos = get_ranked_info(me.id)
