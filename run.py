#!/usr/bin/env python3

import iterm2
import sys


title = sys.argv[1]
path = sys.argv[2]
commands = sys.argv[3:]

async def runCommand(session, command):
    return await session.async_send_text(command + '\n')

async def cd(session, path):
    return await session.async_send_text('cd ' + path + '\n')

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


    await myterm.current_tab.async_set_title(title)

    firstCommand = commands[0]
    lastCommands = commands[1:]


    session = myterm.current_tab.current_session
    await cd(session, path)
    await runCommand(session, firstCommand)

    for cmd in lastCommands:
        session2 = await session.async_split_pane(vertical=True)
        await cd(session2, path)
        await runCommand(session2, cmd)
        
# Passing True for the second parameter means keep trying to
# connect until the app launches.
iterm2.run_until_complete(main, True)