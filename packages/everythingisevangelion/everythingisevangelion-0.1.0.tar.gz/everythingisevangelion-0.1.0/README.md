Everythingisevangelion
----------------------
A tool to find a path from a starting Wikipedia article to the "Neon Genesis Evangelion" article (or any article containing "Evangelion"). The path returned is the first one found, so results may vary.
----------------------
How to use?
----------------------
import eva
my_eva = eva.eva()
my_eva.search(*start article name*)
----------------------
Attributes:
● my_eva.start: The starting article for the search.
● my_eva.end: The end article (either "Neon Genesis Evangelion" or another article containing the word "Evangelion").
● my_eva.EndIsExact: True if the end article is exactly "Neon Genesis Evangelion".
● my_eva.checked: The number of links checked during the search process.
● my_eva.depth: The number of "clicks" (steps) it takes to reach the end article.
● my_eva.path: A list representing the path from the start article to the end article.
