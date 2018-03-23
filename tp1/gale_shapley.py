from random import shuffle
import os.path

N_PLAYERS = 200
N_TEAMS = 20
DIR_NAME = "gs-instance/"

def write_file(filename, preferences):
	with open(filename, 'wb') as f:
		for number in preferences:
			f.write(str(number) + '\n')

def get_numbers_from_file(filename):
	with open(filename, 'r') as f:
		content = f.readlines()
	return [int(x) for x in content]

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


def gale_shapley():
	raise NotImplementedError()


def main():
	generate_instance()
	player198 = get_numbers_from_file(DIR_NAME + "player_198.txt")
	team3 = get_numbers_from_file(DIR_NAME + "team_3.txt")
	team7 = get_numbers_from_file(DIR_NAME + "team_7.txt")
	print team3
	print team7
	print player198



if __name__ == '__main__':
	main()