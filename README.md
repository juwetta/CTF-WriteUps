# CTF-WriteUps

This is a hard categary web challenge from FSIIECTF.

Should be a unique challenge, as it is closer to a programming challenge, rather than a web exploitation challenge...

Brief description: We need to answer 300 questions in order to get the flag. 
Every question will generate a bunch of point pairs. eg. (x1, y1), (x2, y2)

So, we need to check if all the point pairs is a single line. 
If its a sinlge line, answer 'yes', else 'no'.

So to get the flag, we made a python script.

# How the script works
we need to make sure the srcipt does a few things:
1. all the points are connected
2. the graph is eulerian
3. we also use bfs to see all points are connected.

The initial script only works for a few questions (up to 20 to 30 questions)
so we took the questions that the script couldnt solve and try to fix accordingly.
