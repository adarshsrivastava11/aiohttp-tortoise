from aiohttp import web
from models import Tournament, Team, Event


async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    tournament = Tournament(name='New Tournament')
    await tournament.save()

    # Or by .create()
    await Event.create(name='Without participants', tournament=tournament)
    event = await Event.create(name='Test', tournament=tournament)
    participants = []
    for i in range(2):
        team = await Team.create(name='Team {}'.format(i + 1))
        participants.append(team)

    # M2M Relationship management is quite straightforward
    # (also look for methods .remove(...) and .clear())
    await event.participants.add(*participants)

    # You can query related entity just with async for
    async for team in event.participants:
        print (team)
        pass

    # After making related query you can iterate with regular for,
    # which can be extremely convenient for using with other packages,
    # for example some kind of serializers with nested support
    for team in event.participants:
        print (team)
        pass

    # Or you can make preemptive call to fetch related objects
    selected_events = await Event.filter(
        participants=participants[0].id
    ).prefetch_related('participants', 'tournament')

    # Tortoise supports variable depth of prefetching related entities
    # This will fetch all events for team and in those events tournaments will be prefetched
    await Team.all().prefetch_related('events__tournament')

    # You can filter and order by related models too
    await Tournament.filter(
        events__name__in=['Test', 'Prod']
    ).order_by('-events__participants__name').distinct()
    return web.Response(text=text)
