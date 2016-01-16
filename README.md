# IRC-Word-Cloud #

A simple word cloud builder created from an irc log file to gain experience with python. The program analyses the log file to create a dictionary of words and their relative frequency. This is then normalised and used to assign different font sizes. Pillow was used to draw the cloud.

Requires the log file to be timestamped in the format "[hours:mins] <user_name> stuff". Can create a word cloud of a user's words or of words said in the same sentence as a specific word depending on the input format.

![Alt text](irc_cloud.jpg "Sample word cloud")
