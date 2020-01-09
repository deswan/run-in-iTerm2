#!/usr/bin/env python3

import iterm2
import sys

title = sys.argv[1]
path = sys.argv[2]

async def main(connection):
    app = await iterm2.async_get_app(connection)

    # Foreground the appc
    await app.async_activate()

    # Create a new tab or window
    myterm = app.current_terminal_window
    if not myterm:
        myterm = await iterm2.Window.async_create(connection)
    else:
        await myterm.async_create_tab()
    await myterm.async_activate()

    partialProfiles = await iterm2.PartialProfile.async_query(connection)
    # Iterate over each partial profile
    for partial in partialProfiles:
        if partial.name == "Default":
            # This is the one we're looking for. Change the current session's
            # profile.
            full = await partial.async_get_full_profile()
            await full.async_set_sync_title(False)
            await app.current_terminal_window.current_tab.current_session.async_set_profile(full)

    # Update the name and disable future updates by
    # control sequences.
    #
    # Changing the name this way is equivalent to
    # editing the Session Name field in
    # Session>Edit Session.

    await myterm.current_tab.async_set_title(title)

    session = myterm.current_tab.current_session
    await session.async_send_text('cd ' + path + '\n')
    await session.async_send_text('npm run webpack' + '\n')


    # session2 = await session.async_split_pane(vertical=True)
    # await session2.async_set_profile_properties(update)
    # await session2.async_send_text('cd ' + path + '\n')
    # await session2.async_send_text('npm run develop' + '\n')
    

    

# Passing True for the second parameter means keep trying to
# connect until the app launches.
iterm2.run_until_complete(main, True)