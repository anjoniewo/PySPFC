"""
Jakobimatrix und Leistungsgleichungen

			|                   |                   |
			|                   |                   |
			|   J1 = δPi/δFj    |   J2 = δPi/δEj    |
			|                   |                   |
			|                   |                   |
	[Jk] =  |----------------------------------------
			|                   |                   |
			|                   |                   |
			|   J3 = δQi/δFj    |    J4 = δQi/δEj   |
			|                   |                   |
			|                   |                   |

Summe ueber alle mit dem Knoten verbundenen Knoten:

Si = Pi + jQi
Pi = ∑  (Ei * (Ej * Gij - Fj * Bij) + Fi * (Fj * Gij + Ej * Bij))
Qi = ∑  (Fi * (Ej * Gij - Fj * Bij) - Ei * (Fj * Gij + Ej * Bij))

Definitionen:

E = Re{U}
F = Im{U}
G = Re{Y}
B = Im{Y}
"""


class JacobianMatrix:
	
	def __init__(self):
		self
