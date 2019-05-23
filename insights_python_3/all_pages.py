import requests, json, sys

with open("config.json", "r") as read_file:
    api_base_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

    # start writing data in csv file
    file = open('results.csv', 'w')
    column_title = "URL, First Meaningful Paint, First Contentful Paint, Speed Index, Interactive\n"
    file.write(column_title)

    # read config.json file
    data = json.load(read_file)
    strategy = str(sys.argv[1])

    # process api request
    for x in data[strategy]:
        url = data[strategy][x]['url']
        page = x
        print('strategy : ' + strategy + '\npage : ' + page + '\nurl : ' + url + '\n')
        
        # send api request
        googleinsight_api = f'{api_base_url}?url={url}&strategy={sys.argv[1]}'
        print(f'Sending API request: {googleinsight_api}')

        r = requests.get(googleinsight_api)
        final_dump = r.json()

        # manipulate data
        arr = ["first-contentful-paint", "first-meaningful-paint", "speed-index", "interactive"]

        value = []
        for action in arr:
            key = str(action)
            value.append(str(final_dump["lighthouseResult"]["audits"][str(action)]["displayValue"]))
            print(f'{key}: ' + list(value)[len(value)-1])

        print(f'************************************* \n')
    
        try:
            row = f'{url},{value[0]},{value[1]},{value[2]},{value[3]}\n'
            file.write(row)
        except NameError:
            print(f'<NameError> Failed to write output')

    file.close()