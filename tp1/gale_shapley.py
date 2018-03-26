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

matches : tuplas que van conformando el matching estable. Cada tupla es: (team, player)

vacancies : vacantes que tiene cada team. En la posicion sub i, esta la cantida de vacantes que tiene el equipo sub i
Hecho asi para poder acceder en O(1) a la cantidad de vacantes y decidir si hay que sacar o meter al equipo de la lista de
equipos no llenos

team_prefs_index : team_prefs_index[i] representa el indice a buscar dentro de la lista de preferencias del Team i,
es decir, quien sera el proximo jugador al cual hacerle una propuesta para ingregar al equiopo.

teams_not_full: es el listado de los N_TEAMS teams a los cuales hay que buscar vacantes.
Una vez que tiene 10 jugadores, se lo elimina de esta lista.
Si un jugador decide irse a otro equipo y no esta en esta lista, vuelve a ingresar, dado que tiene que cubrir una vacante

player_team : el player_team[i] representa el Team en el cual esta el Player sub i.
Hecho asi para poder acceder al equipo en O(1)

matrix_preference: es una matriz de N_PLAYERS filas por N_TEAMS columnas, donde se lleva registro de cual es el valor de
preferencia que tiene cada jugador para cada equipo.
matrix_preference[i] es la fila de preferencias del Player i, por lo que matrix_preference[i][j] es el valor que tiene
Player i para Team j. A menor valor, mayor preferencia por dicho equipo.
Se utiliza para realizar comparaciones en tiempo constante de si un jugador prefiere un Team u otro para tomar la decision
de quedarse o irse de un Team

"""
def gale_shapley(team_prefs, player_prefs):

	matches = {}
	vacancies = [N_PLAYERS / N_TEAMS for i in range(N_TEAMS)]
	team_prefs_index = [0 for i in range(N_PLAYERS)]
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

"""
Para verificar que el resultado obtenido es valido se deben verificar:
1) Hay 20 equipos con 10 personas para cada equipo
2) Para cada combinacion de (team, player) no pueden verificarse ambas condiciones
OtroTeam tiene preferencia por un Player de Team
Player tiene preferencia por OtroTeam antes que por Team
"""
def is_stable_matching(sm, team_prefs, player_prefs):
	matrix = {}
	for k in sm.keys():
		if k[0] in matrix:
			matrix[k[0]].append(k[1])
		else:
			matrix[k[0]] = [k[1]]
	for k in matrix:
		if (len(matrix[k]) != (N_PLAYERS / N_TEAMS)):
			return False
	# TODO(tmussi) Falta verificar que es matching estable.
	return True


def main():
	generate_instance()
	team_prefs, player_prefs = get_preferences()
	sm = gale_shapley(team_prefs, player_prefs)
	assert(is_stable_matching(sm, team_prefs, player_prefs))



if __name__ == '__main__':
	main()