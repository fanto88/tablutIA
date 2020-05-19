Mettere immagine della board di partenza qui
# Artificial Intelligence for Tablut Board Game
We created an Artificial Intelligence based on minimax alpha beta pruning algorithm to play a game called Tablut.
The project was created to participate in a university competition.

## Getting Started

### Cloning the repository
First of all you need to clone the repository to your local machine.

#### Getting Git
The first step is having git installed on your local machine. If you’re on a Debian-based distribution, 
such as Ubuntu, try apt:

```
sudo apt install git-all
```

#### Cloning the repository
Second step is to actually clone the repository using:
```
git clone https://github.com/fanto88/tablutIA
```

### Installing Python 3.7

### Download of the Server

### Starting the Player
Now that you have all the components needed you can finally start the player. In order to do so start the server first,
then go to the root of the cloned project and run this command:
```
python3.7 UniWarsLAscesaDiChesani.py [-c color] [-t timeout] [-s ipAddress:port]
```

Where ``` -c -t -s ``` are not mandatory. If omitted, the default values ​​will be used
``` 
-c Let you select the player color (White/Black). Default White
-t Let you express a max timeout in seconds for choosing the best action. Default 60
-s Let you define the server address. Default localhost:5800 if White player, otherwise localhost:5801
```