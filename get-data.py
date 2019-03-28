import json
import asyncio
import aiohttp
from device import Device
from data_reader import read_all_devices, read_messages

with open('config.json', 'r') as configuration:
    config = json.load(configuration)

async def main():
    id = "4D492C"
    await get_messages(id, {"limit": config['limit']})

async def get_messages(id, params):
    url = config['url'] + config['routes']['GET-DEVICES'] + "/" + str(id) + "/" + config['routes']["GET-DEVICE-MESSAGES"]
    auth = aiohttp.BasicAuth(login = config['username'], password = config['password'])
    async with aiohttp.ClientSession(auth=auth) as session:
        async with session.get(url, params=params) as response:
            data = await response.text()

            if response.status != 200:
                print('Error: Archiver returned HTTP %u' % response.status)
                exit()

            try:
                parsed = json.loads(data)
            except Exception as e:
                print('Error: Unable to parse archiver response: %s'+str(e))
                exit()

            previous = None
            with open('data.csv', 'a') as data:
                data.write("difference,messagenumber\n")
                for element in parsed['data']:
                    message = element['data']
                    message = bytes.fromhex(message).decode('utf-8')
                    timestamp = element["time"]

                    if previous:
                        diff = previous - timestamp
                        message_split = message.split(" ")
                        data.write(message_split[-1] + "," + str(diff)+"\n")
                    previous = timestamp
                
            if parsed['paging']:
                nexturl = parsed['paging']['next']
                search_string = "before="
                index = nexturl.index(search_string)
                before = nexturl[index+len(search_string):]
                await get_messages(id, {"limit": config['limit'], "before": before})


def run():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [loop.create_task(main())]
    try:
        print("Running...")
        loop.run_until_complete(asyncio.wait(tasks))
    except KeyboardInterrupt:
        print('')
        print('Exiting ...')
    loop.close()

run()