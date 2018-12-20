# penguin_huddle
In this project, we try to simulate the huddling of Emperor Penguins

I'm using a Multiagent Based Software called "mesa" to create agents (penguins) and watch them come together to huddle.

There is no Machine Learning in the program at this point, the bots (penguins) move through a rule based logical system. 
The rules being: 
* Increase the number of neighbors. The grid is hexagonal, so the penguins can see and walk in 6 directions. The greater the neighbors, the less heat-loss.
* Move towards the hottest crowd. Problems arise when two or so groups are formed that are roughly the same size. They do not form a group in such cases)
