# -*- coding: utf-8 -*-
import datetime  # import to sort the episode released time.
import json  # import the json to decode the url info.
import ssl  # import ssl to unlock the mac limitation.
import urllib.request  # import to open the url
from collections import namedtuple  # store data.

ssl._create_default_https_context = ssl._create_unverified_context


# unlock the mac certificate limit.


class Model:
    def __init__(self):
        self.URL = ''
        # Set the url to null.
        self.info = []
        # set the info list.
        self.all_episode = []
        # store the episode number.
        self.dict = dict()
        # store episode and season number.
        self.exist_episode = []
        # store chosen episodes.
        self.user_list = []
        # get give input.
        self.finaldic = dict()
        # get url decoded info.
        self.timelist = []
        # get all the released time.
        self.episode_namedtuple = namedtuple('episode_namedtuple',
                                             'Time Title Season Number Plot')
        # store useful episode infos.
        self.Episode = ()
        # set initial episode to empty set.
        self.test = []

    def search_tv(self, key_word):
        title = '+'.join(
            key_word.split(' '))
        # change user key words in to url format.
        self.URL = 'https://www.omdbapi.com?t=' + title + '&apikey=c589aa0b'
        # get the url of the season infomation.
        try:  # try if the website exist.
            raw = urllib.request.urlopen(
                self.URL)
            # get raw information from the url.
            finaldata = raw.read()
            # read the information.
            self.finaldic = eval(
                finaldata.decode(encoding='utf-8'))
            # decode the content.

            num_seasons = self.finaldic[
                'totalSeasons']
            # get the dictionary of the season.
            # print('Total Season:', num_seasons)
            # print out the total season number.
            n = False
            # turn the status into false if the url is opened correctly.

        except KeyError:  # print out the error.
            pass

        for i in range(1 + int(self.finaldic['totalSeasons'])):
            # loop through the season list.
            self.exist_episode = []
            U = self.URL + '&season=' + str(i)
            # get the info for each episode
            raw = urllib.request.urlopen(
                U)  # get raw information from the url.
            finaldata = raw.read()  # read the information.
            season = json.loads(finaldata.decode(
                encoding='utf-8'))
            # decode the info and change it into dictionary.
            self.info.append(season)
            # append the seasons for later user.
            if 'Episodes' in season:
                # check if the episode exists.
                self.dict[
                    ('Season ' + str(i))] = []
                # print out the season number.
                for dic in (season['Episodes']):
                    # check through each episode.
                    if 'Title' in dic:
                        # check if the episode exist.
                        self.dict[('Season ' + str(i))].append(
                            'Episodes ' +
                            str(dic['Episode']) + ': ' + str(dic['Title']))
                        # print out the episode num and seaon num.
                        self.exist_episode.append(dic['Episode'])
            self.all_episode.append(self.exist_episode)

    def get_season(self, season_num, episode_num):
        if 1 <= int(season_num) <= int(self.finaldic['totalSeasons']):
            y = self.get_e(season_num, episode_num)
            # if the user input episode number is valid.
            if y == 0:
                # check if has been chosen.
                return 0
            # return 0 if has been chosen.
        else:
            return 0
        # return 0 if input is not valid.

    def get_e(self, season_num, episode_num):

        if episode_num in self.all_episode[int(season_num)] \
                and [season_num, episode_num] not in self.user_list:
            self.user_list.append([season_num, episode_num])
            # append the five input into a list.

        elif [season_num, episode_num] in self.user_list:
            return 0
            # return 0 if the episode has been chosen.

        else:
            return 0
            # return 0 if the episode is invalid.

    def sort_by_time(self):
        for y in self.user_list:  # loop through the user input list.
            for episode in self.info[int(y[0])]['Episodes']:
                # loop through the episode info dic.
                if int(episode['Episode']) == int(y[1]):
                    # check if the user input match the episode name.
                    new_url = self.URL + '&season=' + str(
                        y[0]) + '&episode=' + str(
                        y[1])
                    # get the url of episode.
                    raw = urllib.request.urlopen(new_url)
                    finaldata = raw.read()
                    # get the episode data.
                    season = eval(finaldata.decode(
                        encoding='utf-8'))
                    # decode the episode info.

                    self.timelist.append(season['Released'])
                    # append the time into a list to sort them.

                    self.Episode = self.episode_namedtuple(
                        Time=season['Released'], Title=episode['Title'],
                        Season=y[0], Number=y[1], Plot=season[
                            'Plot'])
                    # create the namedtuple to store episode.
                    self.test.append(
                        self.Episode)
                    # append the episode info into the list.

        self.timelist.sort(
            key=lambda date: datetime.datetime.strptime(date, '%d %b %Y'))

    def download(self, filename):
        with open(filename + '.csv', 'a') as f:
            # try to open the file.
            for day in self.timelist:
                # loop through the user list.
                for namedtup in self.test:
                    # get the episode data.
                    if day == namedtup.Time:
                        # check if the user input episode
                        # number matches the real episode.
                        if [namedtup.Season, namedtup.Number] \
                                in self.user_list:
                            f.write('Episode Title: ')
                            # write the data into the file.
                            f.write(
                                namedtup.Title)
                            # write the data into the file.
                            f.write('\n')
                            # write the data into the file.

                            f.write(
                                'Released Time: ')
                            # write the data into the file.
                            f.write(
                                namedtup.Time)
                            # write the data into the file.
                            f.write('\n')
                            # write the data into the file.

                            f.write(
                                'Episode Season: ')
                            # write the data into the file.
                            f.write(
                                namedtup.Season)
                            # write the data into the file.
                            f.write('\n')
                            # write the data into the file.

                            f.write(
                                'Episode Number: ')
                            # write the data into the file.
                            f.write(
                                namedtup.Number)
                            # write the data into the file.
                            f.write('\n')
                            # write the data into the file.

                            f.write(
                                'Plot Summary: ')
                            # write the data into the file.
                            f.write(
                                namedtup.Plot)
                            # write the data into the file.
                            f.write('\n')
                            # write the data into the file.
                            f.write('\n')
                            # write the data into the file.
