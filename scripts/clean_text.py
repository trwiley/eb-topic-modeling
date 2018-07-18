# clean_text
# Purpose: clean the Earthbound text dump file.

textstream = open("eb_script.txt", "r")
textdump = textstream.read()
textdump = textdump.replace("@", "")

output = open("eb_script_clean.txt", "w")
output.write(textdump)
output.close()
