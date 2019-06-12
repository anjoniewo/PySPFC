import SchemDraw as schem
import SchemDraw.elements as e

schematic = schem.Drawing()
# schematic.add(e.T)
res_start_pts = [0, 4]
res_end_pts = [5, 4]
schematic.add(e.RES, label='100K$\Omega$', endpts=[res_start_pts, res_end_pts])
schematic.add(e.ARROW_I, d='down', rightlabel='Load 1', endpts=[[5, 4], [5, 4]])
# schematic.add(e.LINE, d='right', label='100 m', xy=[3, 4])
# schematic.add(e.DOT, toplabel="I'm a bus", xy=[2, 4])
schematic.draw()
# schematic.save('schematic.eps')
