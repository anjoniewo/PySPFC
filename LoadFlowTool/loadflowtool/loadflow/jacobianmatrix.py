"""
Aus der Jakobimatrix J werden die Gleichungen des Slackknotens gestrichen:

=> dim(J) = (m, m) -> dim(Jk) = (m-2, m-2)

Unter-Jakobimatrix Jk und Leistungsgleichungen
	
			|                     |                    |    | ΔF2 |     | ΔP2 |
			|                     |                    |    |  .  |     |     |
			|    Jk1 = δPi/δFj    |   Jk2 = δPi/δEj    |    |  .  |     |     |
			|                     |                    |    |  .  |     |     |
			|                     |                    |    | ΔFn |     | ΔPn |
	[Jk] =  |------------------------------------------|  * |-----|  =  |-----|
			|                     |                    |    | ΔE2 |     | ΔQ2 |
			|                     |                    |    |  .  |     |     |
			|   Jk3 = δQi/δFj     |    Jk4 = δQi/δEj   |    |  .  |     |     |
			|                     |                    |    |  .  |     |     |
			|                     |                    |    | ΔEn |     | ΔQn |

Fuer Referenz- (Slack) und Lastknoten (P-Q) gelten folgende Gleichungen:
Summe ueber alle mit dem Knoten verbundenen Knoten ->

Si = Pi + jQi
Pi = ∑  (Ei * (Ej * Gij - Fj * Bij) + Fi * (Fj * Gij + Ej * Bij))
Qi = ∑  (Fi * (Ej * Gij - Fj * Bij) - Ei * (Fj * Gij + Ej * Bij))

Fuer spannungsgeregelte Knoten (P-U) gilt:

Ui^2 = Ei^2 + Fi^2

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
