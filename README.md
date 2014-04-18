This server will be used in an upcoming king-of-the-hill challenge on [codegolf.stackexchange.com](http://codegolf.stackexchange.com)

Before we even begin, allow me to say this: The bots currently existing under `players/` are strictly for testing. There's not even any code there. All they do is print their name to the console and wait. You get to play the part of the bot yourself by manually reading `from_server` and writing to `to_server`. Lucky you! ...Take those bots out once you have at least 6 actual bots to test with.

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

Voting is also a very important part of the game. To vote for a player, simply output `vote playerName`. To vote for no one, do one of these things:

* Output `vote no one`
* Never vote for anyone for the whole day
* Try to vote for people, but have the output format wrong so the server gets confused and defaults you to voting for no one

Voting shows up for everyone (including you) as `yourBotName votes to kill voteTarget`, with `voteTarget` being the name of the player that was voted for or `no one` if no one was voted for. Note that you cannot vote on day 0: It's treated the same as not outputting anything.

At the end of the day, so long as the majority of people didn't vote to kill someone, there will be a lynch. You will see input that looks like this:
```
The town has killed playerName!
They were $ROLE
```
where `$ROLE` is one of the following:

* `a villager`
* `a mafioso`
* `the cop`
* `the doctor`

If no one was lynched, you will instead see this:
```
The town opted to lynch no one today.
```
When you recieve this input, regardless of whether someone was lynched or not, the server isn't looking for your output. You're only being run so you can see who was lynched.

Overnight, if you have a power role, your bot will be run once more to use your power.

If you are mafia, when you are woken up, you will see this:
```
It is night. Vote for a victim.
```
At that point, you will vote for who you want the mafia to kill overnight. No fancy syntax is necessary, just output the player's name. If you confuse the server, you'll be put down for a "don't kill anyone" vote (which you sometimes want!)

If you're the cop, you get this input at night:
```
It is night. Who would you like to investigate?
```
Again, output the name of the player you want to know more about. Nothing fancy. Screwing this up means you don't investigate anyone.

Finally, the doctor gets this at night:
```
It is night. Who would you like to save?
```
Output the name of the player who you think the mafia is trying to kill tonight. If you're right, no one dies overnight.

When night is over, the next day starts. On days other than 0, the opening message is different:
```
Dawn of day 1. # Obviously the '1' changes depending on which day it is
Last night, someBot was killed. # This line only shows up if the mafia killed someone
Investigations showed that aBot is $$$$-aligned. # This line only shows up if you're the cop and you investigated someone overnight. aBot is their name and $$$$ is replaced by 'mafia' or 'village'.
These players are still alive: every, remaining, player, is, listed, here, in, this, format
```
Days repeat until the mafia matches/exceeds the village in numbers OR the mafia is entirely wiped out.
