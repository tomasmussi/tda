from random import shuffle
import os.path

N_PLAYERS = 200
N_TEAMS = 20
DIR_NAME = "gs-instance/"

"""
Escribe a un archivo las preferencias generadas para un team/player
"""
def write_file(filename, preferences):
	with open(filename, 'wb') as f:
		for number in preferences:
			f.write(str(number) + '\n')

"""
Lee de un archivo las preferencias generadas
"""
def get_numbers_from_file(filename):
	with open(filename, 'r') as f:
		content = f.readlines()
	return [int(x) for x in content]

"""
Genera una instancia de preferencias de players y teams
"""
def generate_instance():
	if (not os.path.isdir(DIR_NAME)):
		os.makedirs(DIR_NAME)
		players = [x for x in xrange(N_PLAYERS)]
		teams = [x for x in xrange(N_TEAMS)]
		player_preference = list(teams)
		team_preference = list(players)

		for player in players:
			shuffle(player_preference)
			write_file(DIR_NAME + "player_" + str(player) + ".txt", player_preference)
		for team in teams:
			shuffle(team_preference)
			write_file(DIR_NAME + "team_" + str(team) + ".txt", team_preference)

"""
Obtiene en forma de matriz las preferencias de todos los players y teams
En el indice i, esta la preferencia del player/team i
"""
def get_preferences():
	team_prefs = []
	for i in xrange(N_TEAMS):
		t_pref = get_numbers_from_file(DIR_NAME + "team_" + str(i) + ".txt")
		team_prefs.append(t_pref)
	player_prefs = []
	for i in xrange(N_PLAYERS):
		p_pref = get_numbers_from_file(DIR_NAME + "player_" + str(i) + ".txt")
		player_prefs.append(p_pref)
	return team_prefs, player_prefs

"""
Algoritmo de Gale Shapley para encontrar un matching estable de equipos
"""
def gale_shapley(team_prefs, player_prefs):
	print team_prefs
	print player_prefs
	raise NotImplementedError()


def main():
	generate_instance()
	team_prefs, player_prefs = get_preferences()
	gale_shapley(team_prefs, player_prefs)



if __name__ == '__main__':
	main()