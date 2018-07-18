# clean_text
# Purpose: clean the Earthbound text dump file.

# load the original file.
textstream = open("eb_script.txt", "r")
textdump = textstream.read()

# remove '@' and '-' symbols from the text dump
textdump = textdump.replace("@", "")
textdump = textdump.replace("-", "")

# write to the new file.
output = open("eb_script_clean.txt", "w")
output.write(textdump)
output.close()
