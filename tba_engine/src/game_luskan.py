from src.core.components.location import Location
from src.core.game import Game
from src.core.components.item import Item

def make_game():
    se_gatehouse = Location(
        'South East Gatehouse',
        'The large gates at the south-east of Luskan are wide open',
    )

    the_cutlass = Location(
        'The Cutlass',
        "Luskan's infamous pub.  Sits on the border of the Market District and the Docks."
    )

    the_market_square = Location(
        "Market Square",
        "Luskan's vibrant Open Market. Also used for public executions"
    )

    approaching_the_music = """you follow the otherwordly music as it becomes louder and
louder. As you get closer, you feel your mind drift further and
further away from you the closer you get to the source."""

    se_gatehouse.addConnection('the cutlass', the_cutlass,
        {
            'to': """You make your way through the streets of Luskan, the streets
are eerily empty.  No matter where you go, the sounds of an
otherwordly music follow you."""
        })

    se_gatehouse.addConnection('market square', the_market_square,
        {
            'to': approaching_the_music
        })

    the_cutlass.addConnection('southeast gatehouse', se_gatehouse,
        travel_blockade = {
            'to':{
                'failure': """You wander the streets, but your mind keeps drifting back
to the otherworldy music that seems to be permeating the
town. After several minutes of walking, you realize that you
haven't been paying attention to where you were going.  To your
surprise, you find yourself back at The Cutlass.""",
                'success': None,
                'state': None,
                'value': True
            }
        })

    the_cutlass.addConnection('market square', the_market_square, {
            'to': approaching_the_music
        })

    rusty_knife = Item(
        'Rusty Knife', "It's going to give me tetanis...",se_gatehouse.name,
        examine_text="It's even rustier up close.",
        takeable=True,
        take_text="""I very carefully pick up the rusty knife. Last thing I need
right now is lockjaw.""",
        is_container=False,
        drop_text="""Crap... it knicked me.""",
    )

    locations = [se_gatehouse, the_cutlass, the_market_square]
    items = [rusty_knife]
    game = Game(se_gatehouse.name, locations, items)
    return game

