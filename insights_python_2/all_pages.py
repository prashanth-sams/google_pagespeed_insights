import requests, json, sys

with open("./config.json", "r") as read_file:
    api_base_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

    # start writing data in csv file
    file = open("./results.csv", "w")
    column_title = "URL, First Meaningful Paint, First Contentful Paint, Speed Index, Interactive"
    file.write(column_title)

    # read config.json file
    data = json.load(read_file)
    strategy = str(sys.argv[1])

    # process api request
    for x in data[strategy]:
        url = data[strategy][x]["url"]
        page = x
        print("strategy : " + strategy + "| page : " + page + " | url : " + url)
        
        # send api request
        googleinsight_api = "%s?url=%s&strategy=%s" % (api_base_url, url, sys.argv[1])
        print("Sending API request: %s" % googleinsight_api)

        r = requests.get(googleinsight_api)
        initial_data = r.json()
        
        final_dump = json.dumps(initial_data, ensure_ascii=False, indent=4)
        final_dump = final_dump.encode("utf-8")
        final_dump = json.loads(final_dump)
        
        arr = ["first-contentful-paint", "first-meaningful-paint", "speed-index", "interactive"]
        
        val = []
        for action in arr:
          action = final_dump["lighthouseResult"]["audits"][str(action)]["displayValue"]
          
          try:
            val.append(action.encode(encoding="ascii", errors="ignore"))
          except EOFError:
          	print("skipped")

        try:
            row = "%s,%s,%s,%s,%s" % (url,val[0],val[1],val[2],val[3])
            file.write(row)
        except NameError:
            print("<NameError> Failed to write output")

        print("=========")
        print(list(val))
        print("=========")

    file.close()