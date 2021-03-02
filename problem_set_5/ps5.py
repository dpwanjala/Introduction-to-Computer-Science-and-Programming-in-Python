# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name: David Paul Wanjala
# Collaborators: None
# Time: 5 hours

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz

# module to search string patterns
import re


# -----------------------------------------------------------------------

# ======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
# ======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
        #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
        #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret


# ======================
# Data structure design
# ======================

# Problem 1
class NewsStory(object):
    """
    takes in properties of a story as strings, assigns them to class attributes and provides getter methods to retrieve
    those properties outside the class definition
    """

    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate


# ======================
# Triggers
# ======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError


# PHRASE TRIGGERS

# Problem 2

class PhraseTrigger(Trigger):
    """
    takes in a string phrase as an argument to the class's constructor.
    it is not case sensitive, i.e Intel and intel are treated equally
    """

    def __init__(self, phrase):
        Trigger.__init__(self)  # provide a default evaluate method
        self.phrase = phrase.lower()  # case insensitive phrase property

    def get_phrase(self):
        return self.phrase

    def is_phrase_in(self, text):
        """
        takes in one string argument text. It returns True if the whole self.phrase is present in text, False otherwise,
        A phrase is one or more words separated by a single space between the words.
        We assume that phrase does not contain any punctuation and should not be case
        sensitive when we search it in text

        fire only when each word is present in its entirely and appears consecutively
        in the text, separated only by spaces or punctuation

        example of valid phrases:
        'purple cow'
        'PURPLE COW'
        'mOoOoOoO'
        'this is a phrase'

        examples of not phrases:
        'purple cow???' contains punctuation)
        purple  cow' (contains multiple spaces between words)
        """
        # assumes that space or any character in string.punctuation is a word separator

        # Strategy
        # 1. split the text at either space or string.punctuation with the help of regular expressions
        text_lst = re.split("[" + " " + string.punctuation + "]+", text)

        # 2. let us now join the text_lst into one long string so we can use regular expression on. we will
        # use a trick here with the "-" to avoid instances where our search might return true when phrase_str
        # appears inside the strings of text_str and not as independent words
        text_str = "-".join(text_lst).lower() + "-"
        phrase_str = "-".join(self.phrase.split(" ")).lower() + "-"

        # we use regular expression to check if phrase_str appears exactly in text_str
        if re.search(phrase_str, text_str):
            return True
        else:
            return False


# Problem 3
class TitleTrigger(PhraseTrigger):
    """
    fires when a news item's title contains a given phrase. evaluate method returns a boolean for this condition.
    """

    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)  # gives us self.phrase property and is_phrase_in method

    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # get title of the story the story
        story_title = story.get_title().lower()
        # check if the object or phrase is in the title of story_title
        return self.is_phrase_in(story_title)


# Problem 4
class DescriptionTrigger(PhraseTrigger):
    """
    fires when a news item's description contains a given phrase. evaluate method returns a boolean for this condition.
    """

    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)  # gives us self.phrase property and is_phrase_in method

    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise. -> description
        """
        # get description of the story
        story_description = story.get_description().lower()
        # check if the object or phrase is in the title of story_title
        return self.is_phrase_in(story_description)


# TIME TRIGGERS

# Problem 5

class TimeTrigger(Trigger):
    """
    takes in time expressed in EST as a string i.e "3 Oct 2016 17:00:10"
    sets an attribute time to a datetime format of the input string.
    """

    def __init__(self, time):
        # convert time to a datetime attribute
        try:
            self.time = datetime.strptime(time, "%d %b %Y %H:%M:%S").replace(tzinfo=pytz.timezone("EST"))
        except ValueError:
            self.time = datetime.strptime(time, "%d %b %Y %H:%M:%S").replace(tzinfo=pytz.timezone("EST"))

    def get_time(self):
        return self.time


class BeforeTrigger(TimeTrigger):
    """
    fires when a story is published strictly before the trigger’s time
    """

    def __init__(self, time):
        TimeTrigger.__init__(self, time)  # gives us self.time attribute

    def evaluate(self, story):
        pub_time = story.get_pubdate().replace(tzinfo=pytz.timezone("EST"))
        return True if pub_time < self.time else False


class AfterTrigger(TimeTrigger):
    """
    fires when a story is published strictly after the trigger’s time
    """

    def __init__(self, time):
        TimeTrigger.__init__(self, time)  # gives us self.time attribute

    def evaluate(self, story):
        pub_time = story.get_pubdate().replace(tzinfo=pytz.timezone("EST"))
        return True if pub_time > self.time else False


# COMPOSITE TRIGGERS

class NotTrigger(Trigger):
    """
    inverts the output of another trigger. It takes
    another triggers as an argument to its constructor.

    EXample: given a trigger and a news item, the output of the NOT trigger's evaluate method should
    be equivalent to not T.evaluate(x)
    """

    def __init__(self, OtherTrigger):
        Trigger.__init__(self)  # gives us evaluate
        self.OtherTrigger = OtherTrigger  # the other trigger

    def evaluate(self, story):
        return False if self.OtherTrigger.evaluate(story) else True


# Problem 8
class AndTrigger(Trigger):
    """
    take two triggers as arguments to its constructor, and should fire on a news story only if both of the inputted
    triggers would fire on that item
    """

    def __init__(self, Trigger1, Trigger2):
        Trigger.__init__(self)  # gives us evaluate
        self.Trigger1 = Trigger1
        self.Trigger2 = Trigger2

    def evaluate(self, story):
        return True if self.Trigger1.evaluate(story) and self.Trigger2.evaluate(story) else False


# Problem 9
class OrTrigger(Trigger):
    """
    take two triggers as arguments to its constructor, and should fire on a news story only if one or both of the inputted
    triggers would fire on that item
    """

    def __init__(self, Trigger1, Trigger2):
        Trigger.__init__(self)  # gives us evaluate
        self.Trigger1 = Trigger1
        self.Trigger2 = Trigger2

    def evaluate(self, story):
        return True if self.Trigger1.evaluate(story) or self.Trigger2.evaluate(story) else False


# ======================
# Filtering
# ======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """

    filtered_stories = []

    for trigger in triggerlist:
        stories_for_trigger = [story for story in stories if trigger.evaluate(story)]
        filtered_stories += stories_for_trigger

    return filtered_stories


# ======================
# User-Specified Triggers
# ======================
# Problem 11

# ***************************** helper function *******************************
def create_trigger_dict(trigger_list):
    """
    takes in a list or triggers and create a corresponding dictionary with keys as names of those triggers and values
    as objects with the correct argument passed into the constructor
    """

    # initialize an empty dictionary
    trigger_dict = {}

    for config in trigger_list:
        # strategy is to check if each item's first element meets this condition and if so, instantiate an object for it
        # and associate it to the key (name of object) as its value.
        config_items = config.split(",")
        if config_items[1] == "TITLE":
            trigger_dict[config_items[0]] = TitleTrigger(config_items[2])
        elif config_items[1] == "DESCRIPTION":
            trigger_dict[config_items[0]] = DescriptionTrigger(config_items[2])
        elif config_items[1] == "AFTER":
            trigger_dict[config_items[0]] = AfterTrigger(config_items[2])
        elif config_items[1] == "BEFORE":
            trigger_dict[config_items[0]] = BeforeTrigger(config_items[2])
        elif config_items[1] == "AND":
            trigger_dict[config_items[0]] = AndTrigger(trigger_dict[config_items[2]], trigger_dict[config_items[3]])
        elif config_items[1] == "OR":
            trigger_dict[config_items[0]] = OrTrigger(trigger_dict[config_items[2]], trigger_dict[config_items[3]])
        elif config_items[1] == "NOT":
            trigger_dict[config_items[0]] = NotTrigger(trigger_dict[config_items[2]])
        else:
            pass

    return trigger_dict


def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # Strategy
    # 1. create a trigger_dictionary that has keys as names of triggers and values as class constructors for those
    # triggers with the correct arguments passed into the constructors
    trigger_dict = create_trigger_dict(lines)

    # 2. since one or more ADD lines in the trigger configuration file will specify which triggers should be in the
    # trigger list. we are going to read which trigger has been references by add, use trigger_dict to read the value
    # for those triggers and add them to a list that we return from this function.

    add_lines = [line for line in lines if line.split(",")[0] == "ADD"]

    # initialize an empty list of triggers
    triggers_list = []

    for add_line in add_lines:
        add_line_items = add_line.split(",")
        # remove add so we only remain with the triggers in that list of items
        add_line_items.remove("ADD")
        triggers_list += [trigger_dict.get(trigger, None) for trigger in add_line_items]

    return triggers_list


SLEEPTIME = 120  # seconds -- how often we poll


def main_thread(master):

    try:
        # Problem 11
        triggerlist = read_trigger_config('triggers.txt')

        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT, fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica", 14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []

        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title() + "\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:
            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            # I think there is a problem with this source, I don't know why objects created from this source don't have
            # 'description' attribute and thus courses my code to have a blank screen if enabled with no stories displayed
            # stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)

            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()
