This server will be used in an upcoming king-of-the-hill challenge on [codegolf.stackexchange.com](http://codegolf.stackexchange.com)

# HOW TO USE

Under `players/` create a directory with the name of your bot. Inside of it, create these files:

* An empty file called `to_server`
* An empty file called `from_server`
* An empty file called `players`
* An executable file called `run` that, when executed by `./run`, is your bot. If you need command line switches or whatever, name your actual bot file something else and then put this in `run`:

```
#!/bin/bash

~~~the real command to actually run your bot~~~
```

Pro tip: If your language makes it easier to work with STDIN/STDOUT than it does file i/o, do something like this:

```
#!/bin/bash

~~~the real command to actually run your bot~~~ < from_server > to_server
```
That will let you take input from STDIN and spit your output to STDOUT. In theory. I haven't tested it at all lmao

`from_server` and `players` *should* be created by the controller if they doesn't already exist, but why leave it up to chance? Why take risks? Be safe. Practice safe mafia

When your bot is executed, it should read the `from_server` file to see what the server wants to tell it, and output whatever it wants to say to the `to_server` file before shutting down. Yes, your bot will shut down. Each time your bot is called, it will stick around long enough to do exactly one thing and then die. I highly recommend that you keep your own log of what's happened so far in the game, since by default you'll only see the most recent thing.

# WHAT INPUT WILL LOOK LIKE / WHAT OUTPUT WILL BE EXPECTED

This is what input will look like on day 0:

```
Rise and shine! Today is day 0.
No voting will occur today.
Be warned: Tonight the mafia will strike.
```

If you have a power role, there will be additional text explaining that to you.

```
# Mafia
You are a member of the mafia.
Your allies are:
newline
delimited
mafia
members
excluding
you

# Cop
You are the cop

# Doctor
You are the doctor
```

Then, 50 times every day, your bot will be run. This is an opportunity to talk with your fellow bots and place your votes. There are 17 messages you can send, found under `controller/messages.py`. To send one, dump this into `to_server`:
```
say [id of the message you wish to send] [iff the id of the message > than 4: the subject of the message] [optional: the intended recipient of the message]
```
This will show up to others as `yourBotName says "[the message associated with that ID][the subject of your message, if applicable]"`. If you added an intended recipient, `thatBot'sName: ` will be inserted directly after the frst quotation mark.

Note that the subject of the message and the intended recipient must both be the name of a bot playing in the game, though not necessarily one that is still alive. The names of all bots in the game will be inserted into the `player` file for you. Note also that you will recieve messages that you yourself have sent, and that every player recieves them even if you specify who the message is meant for.
