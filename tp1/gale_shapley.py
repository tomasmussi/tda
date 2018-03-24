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

	matches = {}
	vacancies = [N_PLAYERS / N_TEAMS for i in range(N_TEAMS)]
	team_prefs_index = [0 for i in range(N_TEAMS)]
	teams_not_full = [i for i in range(N_TEAMS)]
	player_team = [-1 for i in range(N_PLAYERS)]
	matrix_preference = [{} for i in range(N_PLAYERS)]

	for i in range(N_PLAYERS):
		pref = 0
		for j in player_prefs[i]:
			matrix_preference[i][j] = pref
			pref += 1

	while (teams_not_full):
		team_i = teams_not_full[0]
		next_offer = team_prefs_index[team_i]
		player_j = team_prefs[team_i][next_offer]
		if (player_team[player_j] == -1):
			# Jugador no tiene equipo
			matches[(team_i, player_j)] = True
			vacancies[team_i] -= 1
			if (vacancies[team_i] == 0):
				teams_not_full.pop(0)
			player_team[player_j] = team_i
		else:
			current_team = player_team[player_j]

			if (matrix_preference[player_j][team_i] < matrix_preference[player_j][current_team]):
				matches.pop((current_team, player_j), None)
				vacancies[current_team] += 1
				if (not current_team in teams_not_full): # GUARDA CON ESTO, ES O(N)!!!
					teams_not_full.insert(len(teams_not_full), current_team)
				vacancies[team_i] -= 1
				if (vacancies[team_i] == 0):
					teams_not_full.pop(0)
		team_prefs_index[team_i] += 1

	return matches

def is_stable_matching(sm, team_prefs, player_prefs):
	return False


def main():
	generate_instance()
	team_prefs, player_prefs = get_preferences()
	sm = gale_shapley(team_prefs, player_prefs)
	assert(is_stable_matching(sm, team_prefs, player_prefs))



if __name__ == '__main__':
	main()