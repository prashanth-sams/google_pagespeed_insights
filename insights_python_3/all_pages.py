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
        first_contentful_paint = str(final_dump['lighthouseResult']['audits']['first-contentful-paint']['displayValue'])
        first_meaningful_paint = str(final_dump['lighthouseResult']['audits']['first-meaningful-paint']['displayValue'])
        speed_index = str(final_dump['lighthouseResult']['audits']['speed-index']['displayValue'])
        interactive = str(final_dump['lighthouseResult']['audits']['interactive']['displayValue'])
        
        # print in console
        print(f'first contentful paint: ' + first_contentful_paint)
        print(f'first meaningful paint: ' + first_meaningful_paint)
        print(f'speed index: ' + speed_index)
        print(f'interactive: ' + interactive + ' \n')
        print(f'************************************* \n')
    
        try:
            row = f'{url},{first_contentful_paint},{first_meaningful_paint},{speed_index},{interactive}\n'
            file.write(row)
        except NameError:
            print(f'<NameError> Failed to write output')

    file.close()