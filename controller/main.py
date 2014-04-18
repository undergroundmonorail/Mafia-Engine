#!/bin/python2

import os
import sys
import random
import textwrap

from messages import messages

class Player(object):
	"""Player object for each bot."""
	vote = None
	role = 0
	
	# Messages to the player are stored in the player object themself until they
	# are sent, allowing more than one message to be sent with relative ease.
	messages = ''
	
	def __init__(self, name):
		self.name = name
	
	def add_message(self, s):
		self.messages += textwrap.dedent(s + '\n')
	
	def get_role(self):
		if self.role == 1:
			return 'a mafioso'
		if self.role == 2:
			return 'the cop'
		if self.role == 3:
			return 'the doctor'
		return 'a villager'

def m_read(p):
	"""Return contents of player p's 'to_server' file, stripped of special
	characters, and clear the file.
	"""
	with open(p.name + '/to_server', 'r+') as f:
		s = filter(lambda c: c.isalnum() or c == ' ', f.read())
		f.truncate(0)
	return s

def m_write(players):
	"""Write messages to each player to that player's 'from_server' file"""
	# Convert Player object to a 1-element list to allow calling for a single
	# player
	if isinstance(players, Player):
		players = [players]
	for p in players:
		with open(p.name + '/from_server', 'w') as f:
			f.write(p.messages)
		p.messages = ''

def execute(p):
	"""Executes the bot associated with player p"""
	os.chdir(p.name)
	os.system('./run')
	os.chdir('..')

def log(message):
	"""Append message + newline to the log file. This happens a lot, so this
	function exists as shorthand.
	"""
	with open('log', 'a') as f:
		f.write(textwrap.dedent(message + '\n'))

def get_players(players):
	"""Return a list of player objects for each player name in the input. Also
	return the doc, cop and a list of the mafia seperately.
	"""
	def assign_roles(players):
		# Shuffling the whole list ensures you aren't assigning multiple roles to one
		# player, which we would have to account for with random.choice()
		random.shuffle(players)
		
		# Make 1/3rd of the players mafia, one player a doctor and one player a cop
		for _ in xrange(len(players) / 3):
			players[0].role = 1
			players.append(players.pop(0))
		
		players[0].role = 2
		players.append(players.pop(0))
		
		players[0].role = 3
		
		# Return list of players, list of mafia, cop and doctor
		return (players,
		        filter(lambda p: p.role == 1, players),
		        players[-1],
		        players[0])
		
	# At least six players are required. Ensure that we have six. Do this by 
	# testing for at least seven, because...
	if len(players) < 7:
		sys.exit('Not enough players.')
	
	# ...The log file is kept in the same directory as the players. Get rid of it
	players.remove('log')
	
	# Convert to Player object, assign roles, and return
	return assign_roles(map(lambda p: Player(p), players))

def kill(p, players, mafia, cop, doctor):
	"""Return every role the player p might be filling, with them removed."""
	players.remove(p)
	if p in mafia:
		mafia.remove(p)
	if cop is p:
		cop = None
	if doctor is p:
		doctor = None
	
	return players, mafia, cop, doctor	

def main():
	# Get player objects for all players, the doc, the cop, and a list of mafia
	os.chdir('players')
	players, mafia, cop, doctor = get_players(os.listdir('.'))
	
	# Give everyone a list of players
	for p in players:
		with open(p.name + '/players', 'w') as f:
			# Sort it so that it isn't ordered by role
			f.write('\n'.join(sorted([l.name for l in players])))
	
	# Clear the log file, so it's fresh for the new game
	with open('log', 'w') as f:
		f.truncate(0)
	
	# Create a dictionary allowing you to look up player objects by their name
	name_to_player = dict(map(lambda p: (p.name, p), players))
	
	day = 0
	
	# Day 0 doesn't have a suspect or victim, every subsequent day does
	suspect, victim = None, None
	
	# Game loop, exits when mafia is dead or mafia outnumbers village
	while mafia and (len(players) - len(mafia)) > len(mafia):
		log('Day {} begins.'.format(day))
		
		# Randomize turn order every day. Bots /shouldn't/ be able to figure
		# this out, but who knows what you crazy kids will come up with. :P
		random.shuffle(players)
		
		# Print a message at the beginning of each day. On the first day, power
		# roles need to be old their role and mafia members need to know their
		# allies. On every other day, the cop needs to know the result of their
		# investigation and all players need to know who died.
		if day == 0:
			log("""\
          Cop: {}
          Doctor: {}
          Mafia: {}""".format(
          cop.name, doctor.name, ', '.join(m.name for m in mafia)))
			
			for p in players:
				p.add_message("""\
				              Rise and shine! Today is day 0.
				              No voting will occur today.
				              Be warned: Tonight the mafia will strike.""")
			
			for m in mafia:
				m.add_message("""\
                      You are a member of the mafia.
                      Your allies are:""")
				m.add_message('\n'.join(p.name for p in mafia if p is not m))
			
			cop.add_message('You are the cop.')
			doctor.add_message('You are the doctor.')
		else:
			for p in players:
				p.add_message('Dawn of day {}.'.format(day))
				if victim is not None:
					p.add_message('Last night, {} was killed.'.format(victim.name))
			
			if victim is not None:
				players, mafia, cop, doctor = kill(victim, players, mafia, cop, doctor)
				log('{}, {}, was killed.'.format(victim.name, victim.get_role))
			
			if suspect is not None:
				cop.add_message('Investigations showed that {} is {}-aligned.'.format(
				suspect.name, 'mafia' if suspect.role == 1 else 'village'))
			
			log('These players are still alive: {}'.format(
			', '.join(p.name for p in players)))

		m_write(players)

		# During a day, players may perform up to 50 actions (Action= vote or talk)
		for r in xrange(50):
			for p in players:
				try:
					execute(p)
					command = m_read(p).split()
					if command[0] == 'vote':
						# Set the player's vote
						if day != 0:
							if command[1] == 'no':
								if command[2] == 'one':
									p.vote = None
									log('{} has voted to lynch no one.'.format(p.name))
									for l in players:
										l.add_message('{} has voted to lynch no one.'.format(p.name))
							else:
								p.vote = name_to_player[command[1]]
								log('{} has voted to lynch {}.'.format(p.name, command[1]))
								for l in players:
									l.add_message(
									'{} has voted to lynch {}.'.format(p.name, command[1]))
					elif command[0] == 'say':
						# Send a message to all players
						message = '{} says "'.format(p.name)
						# Messages with an id higher than 4 have the name of a bot attached
						# This screws with parsing a bit so we handle them seperately
						if int(command[1]) > 4:
							if len(command) == 4:
								# Convert from a name to a player object and back to ensure
								# that it's a correct name
								message += '{}, '.format(name_to_player[command[3]].name)
							message += messages[int(command[1])]
							message += '{}"'.format(name_to_player[command[2]].name)
						else:
							if len(command) == 3:
								message += '{}, '.format(name_to_player[command[2]].name)
							message += '{}"'.format(messages[int(command[1])])
						log(message)
						for l in players:
							l.add_message(message)
				except:
					# Do nothing on invalid input
					pass
			
			m_write(players)
		
		# Tally up the votes for each player
		votes = [p.vote for p in players]
		
		# Shuffle to eliminate max() bias
		random.shuffle(votes)
		
		# The most voted player is lynched, with ties broken randomly
		lynched = max(votes, key=votes.count)
		if lynched is not None:
			log('The town has killed {}!'.format(lynched.name))
			log('They were {}.'.format(lynched.get_role()))
			for p in players:
				p.add_message("""\
				The town has killed {}!
				They were {}.""".format(lynched.name, lynched.get_role))
			players, mafia, cop, doctor = kill(lynched, players, mafia, cop, doctor)
		else:
			log('The town opted to lynch no one today.')
			for p in players:
				p.add_message('The town opted to lynch no one today.')
		
		m_write(players)
		for p in players:
			execute(p)
			p.vote = None
		
		# Don't go to night if a win condition's been met.
		if not mafia or (len(players) - len(mafia)) <= len(mafia):
			break
		
		# Day ends, night begins
		
		# MAFIA NIGHT ACTION
		# Each mafioso votes for a victim. The most voted player is then killed,
		# unless saved that night by the doctor.
		for m in mafia:
			m.add_message('It is night. Vote for a victim.')
		m_write(mafia)
		
		victim_votes = []		
		for m in mafia:
			try:
				execute(m)
				victim_votes.append(name_to_player[m_read(m)])
				log('{} votes to kill {}.'.format(m.name, victim_votes[-1].name))
			except:
				# Vote to kill no one on invalid input
				victim_votes.append(None)
				log(m.name + ' votes to kill no one.')
		
		# Shuffle to eliminate max() bias
		random.shuffle(victim_votes)
		
		# The victim is the player most voted for by the mafia, with ties broken
		# randomly.
		victim = max(victim_votes, key=victim_votes.count)
		log('The mafia collectively decides to kill {}.'.format(
		    victim.name if victim is not None else 'no one'))
		
		# COP NIGHT ACTION
		# The cop chooses a player to investigate. At the dawn of the next day,
		# they are told whether that player is village- or mafia-aligned.
		if cop is not None:
			cop.add_message('It is night. Who would you like to investigate?')
			m_write(cop)
			try:
				execute(cop)
				suspect = name_to_player[m_read(cop)]
				log('{} spends the night investigating {}.'.format(
				cop.name, suspect.name))
			except:
				# Investigate no one on invalid input
				suspect = None
				log('{} chooses not to investigate anyone.'.format(cop.name))
		
		# DOCTOR NIGHT ACTION
		# The doctor chooses a player they expect the mafia to try to kill. If they
		# are right, the mafia gets no kills that night.
		if doctor is not None:
			doctor.add_message('It is night. Who would you like to save?')
			m_write(doctor)
			try:
				execute(doctor)
				patient = name_to_player[m_read(doctor)]
				if patient == victim:
					victim = None
					log('{} was able to save {} from near-certain death.'.format(
					doctor.name, patient.name))
				else:
					log('{} tried to save {}, but they were not the target.'.format(
					doctor.name, patient.name))
			except:
				# Save no one on invalid input
				log('{} took tonight off.'.format(doctor.name))
		
		log('')
		day += 1
	
	if mafia:
		print 'MAFIA VICTORY'
		log('MAFIA VICTORY')
	else:
		print 'VILLAGE VICTORY'
		log('VILLAGE VICTORY')
		
if __name__ == '__main__':
	main()
