This server will be used in an upcoming king-of-the-hill challenge on codegolf.stackexchange.com

# HOW TO USE

Under `players/` create a directory with the name of your bot. Inside of it, create these files:

* The actual bot
* An empty file called `to_server`
* An empty file called `from_server`
* An empty file called `players`
* An executable script called `run` that runs your bot

`from_server` and `players` *should* be created by the controller if they doesn't already exist, but why leave it up to chance? Why take risks? Be safe. Practice safe mafia

When your bot is executed, it should read the `from_server` file to see what the server wants to tell it, and output whatever it wants to say to the `to_server` file before shutting down. Yes, your bot will shut down. Each time your bot is called, it will stick around long enough to do exactly one thing and then die. I highly recommend that you keep your own log of what's happened so far in the game, since by default you'll only see the most recent thing.
