
import os

good = []
banned = []

# Load list of bots and crawlers
with open("banned.txt", "r") as file:
    for line in file:
        banned.append(line.strip())

# Display banned items
print (banned)

# Loop through data files and filter lines based on banned words
for filename in os.listdir("Data/"):
    if (filename[:4] == "ceda"):
        with open("Data/" + filename, "r") as file:
            for line in file:
                if not any(x in line for x in banned):
                    if("uuid" in line):
                        good.append(line)

# Write filtered data to file
with open("output_data/output.txt", "w") as file:
        file.writelines(good)
print("Done")
