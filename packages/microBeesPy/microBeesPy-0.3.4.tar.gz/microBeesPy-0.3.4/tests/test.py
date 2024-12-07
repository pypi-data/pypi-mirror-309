import aiohttp
import asyncio

async def  callTEST():
  session  = aiohttp.ClientSession()
  resp = await  session.post("https://dev.microbees.com/public/testPOST")
  if resp.status == 200:
    response = await resp.text()
    print(response)

loop = asyncio.get_event_loop()

# Blocking call which returns when the display_date() coroutine is done
loop.run_until_complete(callTEST())
loop.close()