import json
import datetime


def format_timestamp(jsonobject):

        time = jsonobject['time']
        if isinstance(time, dict):
            timestamp = int(time["$date"])/1000.0
            time_obj = datetime.datetime.fromtimestamp(timestamp)
            time_formatted = time_obj.strftime('%Y-%m-%dT%H:%M:%S.%f') 
            jsonobject['time'] = time_formatted
    


if __name__ == '__main__':

    JSONLine = '{ "agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11", "event" : "toto", "event_source" : "server", "event_type" : "/courses/MITx/6.002x/2013_Spring/about", "ip" : "109.182.63.218", "time" : { "$date" : 1356996514740 }, "username" : "" }'
    
    jsonobject = json.loads(JSONLine)
    time = jsonobject['time']
    timestamp = int(time["$date"])/1000.0
    time_obj = datetime.datetime.fromtimestamp(timestamp)
    time_formatted = time_obj.strftime('%Y-%m-%d %H:%M:%S') 
    print time_formatted 

    
    
