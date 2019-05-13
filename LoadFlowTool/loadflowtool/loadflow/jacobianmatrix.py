"""

Jakobimatrix und Leistungsgleichungen
	
			|                   |                   |   | ΔF1 |     | ΔP1 |
			|                   |                   |   |  .  |     |     |
			|   J1 = δPi/δFj    |   J2 = δPi/δEj    |   |  .  |     |     |
			|                   |                   |   |  .  |     |     |
			|                   |                   |   | ΔFn |     | ΔPn |
	[Jk] =  |---------------------------------------| * |-----|  =  |-----|
			|                   |                   |   | ΔE1 |     | ΔQ1 |
			|                   |                   |   |  .  |     |     |
			|   J3 = δQi/δFj    |    J4 = δQi/δEj   |   |  .  |     |     |
			|                   |                   |   |  .  |     |     |
			|                   |                   |   | ΔEn |     | ΔQn |

Summe ueber alle mit dem Knoten verbundenen Knoten:

Si = Pi + jQi
Pi = ∑  (Ei * (Ej * Gij - Fj * Bij) + Fi * (Fj * Gij + Ej * Bij))
Qi = ∑  (Fi * (Ej * Gij - Fj * Bij) - Ei * (Fj * Gij + Ej * Bij))

Definitionen:

Ui = Ei + jFi
Ei = Re{Ui}
Fi = Im{Ui}
Yi = Gi + jBi
Gi = Re{Yi}
Bi = Im{Yi}

"""


class JacobianMatrix:
	
	def __init__(self):
		self
