import re

from aqt import gui_hooks


def replace_deck_node_options(deck_id: int, options_name: str, tree: str) -> str:
    pattern = re.compile(re.escape('\"opts:') + str(deck_id) + re.escape('\");\'><img src=\'/_anki/imgs/gears.svg\' class=gears>'))
    replacement = f'\"opts:{deck_id}\");\'><img src=\'/_anki/imgs/gears.svg\' class=gears>{options_name}'
    return re.sub(pattern, replacement, tree)


def replace_home_decks_options_buttons(browser, content) -> None:
    '''
    Grabs all decks from the browser's collection's deck manager,
    and adds their option names to the browser's content tree
    '''
    for deck in browser.mw.col.decks.all_names_and_ids():
        deck_id = deck.id
        if (options_name := (browser.mw.col.decks.config_dict_for_deck_id(deck_id) or {}).get("name")):
            content.tree = replace_deck_node_options(
                deck_id=deck_id,
                options_name=options_name,
                tree=content.tree
            )

# https://github.com/ankitects/anki/blob/main/qt/tools/genhooks_gui.py
gui_hooks.deck_browser_will_render_content.append(replace_home_decks_options_buttons)