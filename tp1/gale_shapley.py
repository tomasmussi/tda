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
			write_file(DIR_NAME + "player_" + str(player) + ".prf", player_preference)
		for team in teams:
			shuffle(team_preference)
			write_file(DIR_NAME + "team_" + str(team) + ".prf", team_preference)

"""
Obtiene en forma de matriz las preferencias de todos los players y teams
En el indice i, esta la preferencia del player/team i
"""
def get_preferences():
	team_prefs = []
	for i in xrange(N_TEAMS):
		t_pref = get_numbers_from_file(DIR_NAME + "team_" + str(i) + ".prf")
		team_prefs.append(t_pref)
	player_prefs = []
	for i in xrange(N_PLAYERS):
		p_pref = get_numbers_from_file(DIR_NAME + "player_" + str(i) + ".prf")
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

RETURN: devuelve un diccionario de Tupla : True, donde Tupla[0] es Team y Tupla[1] es Player
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
				r = matches.pop((current_team, player_j), None)
				vacancies[current_team] += 1
				if (vacancies[current_team] == 1):
					teams_not_full.insert(len(teams_not_full), current_team)
				vacancies[team_i] -= 1
				if (vacancies[team_i] == 0):
					teams_not_full.pop(0)

				# Cambio de equipo
				player_team[player_j] = team_i
				# Agrego nueva pareja al matching
				matches[(team_i, player_j)] = True
		team_prefs_index[team_i] += 1
	return matches


"""
Verifica si es inestable un par (Team, Player)
"""
def is_stable(team, player, team_prefs, player_prefs):
	# Verifico que Player este dentro de las 10 primeras opciones de Team
	team_prefers_player = team_prefs[team].index(player) < (N_PLAYERS / N_TEAMS)
	if (team_prefers_player):
		# Veo que pasa con las preferencias de Player, me fijo los Teams anteriores dentro de sus preferencias
		index_of_team = player_prefs[player].index(team)
		for i in range(index_of_team):
			other_team = player_prefs[player][i]
			# Other Team es un Team que Player preferia antes que el Team en el que esta, debo asegurarme que
			# todas las vacantes que tenia Other Team estan cubiertas por Players con mayor preferencia que Player
			for ot_pref in team_prefs[other_team]:
				if (ot_pref == player):
					# Encontre a player dentro de las preferencias de otro team
					break
				if (team_prefs[other_team].index(ot_pref) > team_prefs[other_team].index(player)):
					# Prefiere a player por sobre otros antes que player
					return False
	else:
		# No esta dentro de mis vacantes, los players anteriores prefieren otros equipos antes que Team
		# Me fijo Players anteriores dentro de mis preferencias
		index_of_player = team_prefs[team].index(player)
		for i in range(index_of_player):
			other_player = team_prefs[team][i]
			# Other Player es un jugador que Team preferia antes que el jugador que tiene, debo asegurarme que
			# Other Player esta en un equipo que prefiere antes que Team
			for op_pref in player_prefs[other_player]:
				if (op_pref == team):
					# Encontre a team dentro de las preferencias del jugador
					break
				if (player_prefs[other_player].index(op_pref) > player_prefs[other_player].index(team)):
					# Prefiere a otro equipo antes que el equipo en el que esta
					return False
	return True

"""
Para verificar que el resultado obtenido es valido se deben verificar:
1) Hay 20 equipos con 10 personas para cada equipo
2) Para cada combinacion de (team, player) tiene que verificarse que:
2.1) Si para equipo, el jugador esta dentro de las 10 vacantes, tiene que pasar que el jugador no prefiera estar en otros equipos
2.2) Si hay jugadores previos, esos jugadores previos deben tener preferencia por otros equipos
"""
def is_stable_matching(matrix, team_prefs, player_prefs):
	# Verificar que haya 20 Teams con 10 Players para cada uno
	for k in matrix.keys():
		if (len(matrix[k]) != (N_PLAYERS / N_TEAMS)):
			return False

	for team in matrix.keys():
		for player in matrix[team]:
			stable = is_stable(team, player, team_prefs, player_prefs)
			if (not stable):
				return False
	return True

def get_matrix(sm):
	matrix = {}
	for k in sm.keys():
		if k[0] in matrix:
			matrix[k[0]].append(k[1])
		else:
			matrix[k[0]] = [k[1]]
	for k in matrix.keys():
		matrix[k].sort()
	return matrix

def print_matrix(matrix):
	for k in matrix.keys():
		print str(k) + " : " + str(matrix[k])

def main():
	generate_instance()
	team_prefs, player_prefs = get_preferences()
	sm = gale_shapley(team_prefs, player_prefs)
	matrix = get_matrix(sm)
	assert(is_stable_matching(matrix, team_prefs, player_prefs))
	print_matrix(matrix)


if __name__ == '__main__':
	main()