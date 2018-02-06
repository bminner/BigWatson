import sys

file = open(sys.argv[1], "r")
positive = open("positive_responses","a")
negative = open("negative_responses","a")


for line in file.readlines():
    score = line[len(line) - 2]
    review = line[:-2]
    if score == '0':
        negative.write(review + "\n")
    else:
        positive.write(review + "\n")

negative.close()
positive.close()
