import aiohttp
import asyncio


async def subscribe_to_update_control():

    async with aiohttp.ClientSession() as session:

        fetch_url = 'http://localhost/test/subscribe_device?id=111'
        async with session.get(pokemon_url) as resp:
            pokemon = await resp.json()
            print(pokemon['name'])



#asyncio.run(main())