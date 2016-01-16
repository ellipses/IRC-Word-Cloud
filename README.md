# IRC-Word-Cloud #

A simple word cloud builder created from an irc log file to gain experience with python. Uses regular expression to capture sentences by a user and creates a dictionary of words and their count. This is then normalised and used to assign different font sizes. The position of words was found by sampling randomly from valid locations after applying a local averaging filter. Pillow was used to draw the cloud.

Requires the log file to be timestamped in the format "[hours:mins] \<user_name> text". Can create a word cloud of a user's words or of words said in the same sentence as a specific word depending on the input format.

![Alt text](irc_cloud.jpg "Sample word cloud")
