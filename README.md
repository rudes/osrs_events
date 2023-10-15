# OSRS Games

discord bot for managing osrs events

## Deploy

```bash
# to launch
make up
# to clean up all the containers
make clean
```
## TODO

- global mod commands
    - admin
        - control settings
        - setup roles and enable/disable games
	- teams
		- gen team from WOM api
		- add member to team
		- remove member from team
		- set team captain
		- save team data to db
	- games/events
		- create a game
		- create a simple game
		- pause the game
		- close the game
		- set event reminders
		- change start date
		- list signed up players
- global user commands
	- /signup event (maybe a reaction system instead)
- tilerace
	- mods
		- teams
			- give roll
			- change challenges
			- change position
			- set path
		- games
			- view and change challenges
	- captains
		- /roll_back
		- /choice
	- players
		- /roll
		- /complete
		- /positions
		- /challenges

