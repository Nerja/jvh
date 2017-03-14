#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# jvh.py (Jodel Vote Hammer)
# n0 - 2017 - Telegram @n0wastaken

import jodel_api
import pickle
import os
from pathlib import Path

lat, lng, city = 46.533333, 6.666777, "Lausanne"
accounts_file = "./account.json"
js = list()
min_displayed_jodels = 20

def main():
    importAccounts()
    while(True):
        print ("[*] Welcome to Jodel Vote Hammer")
        print ("    n0 - 2017")
        print ("    @n0wastaken")
        print ("")
        print("[-] "+ str(len(js)) + " Account(s) loaded")
        choice = menu()
        if choice == "d":
            mainDownvote()
        elif choice == "u":
            mainUpvote()
        elif choice == "a":
            addAccount()
        elif choice == "r":
            removeAccounts()
        else:
            pass


def importAccounts():
    global js
    if Path(accounts_file).is_file():
        accounts = pickle.load(open(accounts_file, 'rb'))
        for account in accounts:
            js.append(jodel_api.JodelAccount(lat=lat, lng=lng, city=city,
                                   update_location=False, **account))
        return True
    else:
        return False


def exportAccounts():
    accounts = list()
    for j in js:
        accounts.append(j.get_account_data())
    f = open(accounts_file, 'wb')
    pickle.dump(accounts, f)
    f.close()


def addAccount():
    global js
    j = jodel_api.JodelAccount(lat=lat, lng=lng, city=city)
    if j.verify_account():
        js.append(j)
        exportAccounts()
        os.system('clear')


def removeAccounts():
    if Path(accounts_file).is_file():
        os.remove(accounts_file)
        print("[-] All accounts are removed")


def menu():
    print("")
    print("---")
    print("[d] Downvote")
    print("[u] Upvote")
    print("[a] Add an account")
    print("[r] Remove all accounts")
    choice = input("\n    Choice: ")
    os.system('clear')
    if choice in ('d', 'u', 'a', 'r'):
        return choice


def listJodels(displayed_jodels):
    posts = js[0].get_posts_recent(skip=displayed_jodels-min_displayed_jodels+1,
                                   limit=displayed_jodels+1, mine=False,
                                   hashtag=None, channel=None)[1]['posts']
    print (" score [ id ]  message")
    print ("-------------")
    jod_id = 0
    jodels = {}
    for post in posts:
        vote = str(post['vote_count']).center(3, " ")
        dis_id = str(jod_id).rjust(2)
        message_strip = post['message'].replace("\n", "")
        message = message_strip[:50] + (message_strip[50:] and '...')
        print ("  " + vote + "  [ " + dis_id + " ] " + message + "")
        jodels.update({str(jod_id):post['post_id']})
        jod_id += 1
    return jodels


def mainDownvote():
    displayed_jodels = min_displayed_jodels
    while(True):
        print("[!] Downvoting ")
        print("    Strike force: -" + str(len(js)))
        print("")
        jodels = listJodels(displayed_jodels)
        sub_choice = menuDownvote(displayed_jodels)
        if sub_choice == 'n':
            displayed_jodels += 20
        elif sub_choice == 'p' and displayed_jodels >= 2*min_displayed_jodels:
            displayed_jodels -= 20
        elif sub_choice == 'c':
            displayed_jodels += 20
        elif sub_choice == 'b':
            break
        elif jodels[sub_choice]:
            downvote(jodels[sub_choice])
        else:
            pass


def downvote(post_id):
    os.system('clear')
    print("[!] Downvoting ")
    print("")
    count = 0
    for j in js:
        if j.downvote(post_id)[0] == 200:
            print("[-] Downvoted!")
            count -= 1
        else:
            print("[-] Failed to downvote ")
    print("")
    print("    " + str(count) + " issued")
    print("")
    input("[!] Press any key to continue")
    os.system('clear')


def menuDownvote(displayed_jodels):
    print("")
    print("---")
    print("[*] Enter the id of the jodel to downvote")
    print("[n] Next page")
    if displayed_jodels >= 2*min_displayed_jodels:
        print("[p] Previous page")
    print("[b] Home")
    choice = input("\n    Choice: ")
    os.system('clear')
    return choice


def mainUpvote():
    displayed_jodels = min_displayed_jodels
    while(True):
        print("[!] Upvoting ")
        print("    Strike force: +" + str(len(js)))
        print("")
        jodels = listJodels(displayed_jodels)
        sub_choice = menuUpvote(displayed_jodels)
        if sub_choice == 'n':
            displayed_jodels += 20
        elif sub_choice == 'p' and displayed_jodels >= 2*min_displayed_jodels:
            displayed_jodels -= 20
        elif sub_choice == 'c':
            displayed_jodels += 20
        elif sub_choice == 'b':
            break
        elif jodels[sub_choice]:
            upvote(jodels[sub_choice])
        else:
            pass


def upvote(post_id):
    os.system('clear')
    print("[!] Upvoting")
    print("")
    count = 0
    for j in js:
        if j.upvote(post_id)[0] == 200:
            print("[-] Upvoted!")
            count += 1
        else:
            print("[-] Failed to upvote ")
    print("")
    print("    " + str(count) + " issued")
    print("")
    input("[!] Press any key to continue")
    os.system('clear')


def menuUpvote(displayed_jodels):
    print("")
    print("---")
    print("[*] Enter the id of the jodel to upvote")
    print("[n] Next page")
    if displayed_jodels >= 2*min_displayed_jodels:
        print("[p] Previous page")
    print("[b] Home")
    choice = input("\n    Choice: ")
    os.system('clear')
    return choice

if __name__ == "__main__":
    try:
        os.system('clear')
        main()
        print ("[*] Bye!\n")
    except (KeyboardInterrupt, SystemExit):
        print("")
        print("")
        exit("[*] Quitting...\n")
