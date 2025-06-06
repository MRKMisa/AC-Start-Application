import configparser

conf = configparser.ConfigParser()
conf.read("config.ini")

ShowReactionTimeGraphic = conf["ReactionTimeGraphic"]["ShowReactionTimeGraphic"]

print(ShowReactionTimeGraphic, type(ShowReactionTimeGraphic))