"""
Qilong Zhangli
QZHANGLI

Xuanyi Lin
xuanyil1

Cayson Yim
yimck
"""
# -*- coding: utf-8 -*-
import datetime
import json
import ssl
import urllib.request
from collections import namedtuple

ssl._create_default_https_context = ssl._create_unverified_context  # unlock the mac limit.


def find_TVshow_info():
    key_word = str(input('Please enter the key words:'))  # prompt the users to input the key words.
    title = '+'.join(key_word.split(' '))  # change user key words in to url format.
    URL = "https://www.omdbapi.com?t=" + title + "&apikey=c589aa0b"  # get the url of the season infomation.
    n = True

    while n:  # prompt user for another input.
        try:  # try if the website exist.
            raw = urllib.request.urlopen(URL)  # get raw information from the url.
            finaldata = raw.read()  # read the information.
            finaldic = eval(finaldata.decode(encoding='utf-8'))  # decode the content.

            num_seasons = finaldic['totalSeasons']  # get the dictionary of the season.
            print('Total Season:', finaldic['totalSeasons'])  # print out the total season number.
            n = False  # turn the status into false if the url is opened correctly.

        except KeyError:  # print out the error.
            print('Invalid Name.')  # print out the error messgae.
            key_word = str(input('Please re-enter the key words:'))  # ask user for another input.
            title = '+'.join(key_word.split(' '))  # get the TV show name.

            URL = "https://www.omdbapi.com?t=" + title + "&apikey=c589aa0b"  # get the URL of the season.

    info = []  # create a empty list.
    for i in range(1 + int(finaldic['totalSeasons'])):  # loop through the season list.
        U = URL + '&season=' + str(i)  # get the info for each episode
        raw = urllib.request.urlopen(U)  # get raw information from the url.
        finaldata = raw.read()  # read the information.
        season = eval(finaldata.decode(encoding='utf-8'))  # decode the info and change it into dictionary.
        info.append(season)  # append the seasons for later user.
        if 'Episodes' in season:  # check if the episode exists.
            print('Season', i)  # print out the season number.
            for dic in (season['Episodes']):  # check through each episode.
                if 'Title' in dic:  # check if the episode exist.
                    print('Episodes', dic['Episode'], ':', dic['Title'])  # print out the episode num and seaon num.
        print()

    user_list = []  # create empty list to store five choices.

    for x in range(5):  # ask input for five times.
        season_num = input('Please enter the season number:\n')
        episode_num = input('Please enter the episode number:\n')
        user_list.append([season_num, episode_num])  # append the five input into a list.

    print()

    timelist = []  # create empty list to sort time.
    episode_namedtuple = namedtuple('episode_namedtuple',
                                    'Time Title Season Number Plot')  # create namedtuple to store the episode info.
    test = []  # create the list to store episode info.
    newnew = user_list.copy()

    for y in user_list:  # loop through the user input list.

        for episode in info[int(y[0])]['Episodes']:  # loop through the episode info dic.

            if int(episode['Episode']) == int(y[1]):  # check if the user input match the episode name.
                newnew.remove(y)

                print('Episode Title:', episode['Title'])  # print out the episode if matches
                print('Season:', y[0])
                print('Episode Number:', y[1])
                print('Plot Summary:')

                new_url = URL + '&season=' + str(y[0]) + '&episode=' + str(y[1])  # get the url of episode.
                raw = urllib.request.urlopen(new_url)
                finaldata = raw.read()  # get the episode data.
                season = eval(finaldata.decode(encoding='utf-8'))  # decode the episode info.
                print(season['Plot'])  # print out the plot from episode info.
                print('Time Released:', season['Released'])  # print out when the episode was released.

                print('More Info:', new_url)  # print out the url for user to get more info.
                timelist.append(season['Released'])  # append the time into a list to sort them.
                print()
                Episode = episode_namedtuple(Time=season['Released'], Title=episode['Title'], Season=y[0], Number=y[1],
                                             Plot=season['Plot'])  # create the namedtuple to store episode info.
                test.append(Episode)  # append the episode info into the list.

    if len(newnew) != 0:  # check if all the episodes are printed out.
        for i in newnew:
            print("Didn't Find Season " + i[0] + ' Episode ' + i[1])  # inform the user if no such episode.

    timelist.sort(key=lambda date: datetime.datetime.strptime(date, '%d %b %Y'))

    path_name = str(
        input('Where do you want to save your file (/Users/apple):\n'))  # prompt the user to input the path.
    file_name = str(input("How do you name the file (example):\n"))  # prompt the user to input the file name.
    path_XX = path_name + '/' + file_name + '.csv'  # change user input into a url.

    with open(path_XX, "a") as f:  # try to open the file.
        for day in timelist:  # loop through the user list.
            for namedtup in test:  # get the episode data.
                if day == namedtup.Time:  # check if the user input episode number matchs the real episode.
                    f.write('Episode Title: ')  # write the data into the file.
                    f.write(namedtup.Title)  # write the data into the file.
                    f.write('\n')  # write the data into the file.

                    f.write('Released Time: ')  # write the data into the file.
                    f.write(namedtup.Time)  # write the data into the file.
                    f.write('\n')  # write the data into the file.

                    f.write('Episode Season: ')  # write the data into the file.
                    f.write(namedtup.Season)  # write the data into the file.
                    f.write('\n')  # write the data into the file.

                    f.write('Episode Number: ')  # write the data into the file.
                    f.write(namedtup.Number)  # write the data into the file.
                    f.write('\n')  # write the data into the file.

                    f.write('Plot Summary: ')  # write the data into the file.
                    f.write(namedtup.Plot)  # write the data into the file.
                    f.write('\n')  # write the data into the file.
                    f.write('\n')  # write the data into the file.

    print('Congratulations! Your file has been saved!')  # Done.


if __name__ == "__main__":
    find_TVshow_info()
