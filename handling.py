# Setup empty lists
ip = []
date = []
extracted_hash = []
query = []

with open('output_data/output.txt', 'r') as f:
    for line in f:

        # Make sure we have a log line not a carriage return or line feed
        if line not in ['\n', '\r\n']:
            split_line = line.split()

            # Split indices 0: IP, 3: Date, 6: Request, 10: Referer
            # Want to get lines which have catalogue and ?q= in referer and /uuid in request
            # Filtered out results with google in referer as that was making tokenising more difficult
            if 'catalogue' in (split_line[10]) and '/uuid/' in (split_line[6]) and "?q=" in split_line[10] and not 'google' in split_line[10]:

                # Add ip and date to output list
                ip.append(split_line[0])
                date.append(split_line[3])

                # Extract the request
                request = (split_line[6])

                # Get the record uuid from the request
                extracted_hash.append(request.split("/uuid/")[1])

                # Extract the referer
                referer = (split_line[10])

                # Split string to extract the query terms
                splitquery = referer.split("?q=")[1]
                splitquery = splitquery.split('&')[0]
                query.append(splitquery.strip ('"./\\,)([]{}<>').lower())

print (len(ip))
print (len(date))
print (len(extracted_hash))
print (len(query))

# Create a dictionary with the data to output
data = {'ip_address': ip, 'date': date, 'extracted_hash': extracted_hash, 'query': query}

import json

# output the data to file as json
with open('output_data/data.json', 'w') as outfile:
    json.dump(data, outfile)


