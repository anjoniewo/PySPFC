from unittest import TestCase
import numpy as np
from LoadFlowTool.loadflowtool.grid.grid import Grid
from LoadFlowTool.loadflowtool.grid.gridnode import GridNode
from LoadFlowTool.loadflowtool.grid.gridline import GridLine
from LoadFlowTool.loadflowtool.loadflow.jacobianmatrix import JacobianMatrix
from LoadFlowTool.loadflowtool.utils import print_matrix
from .test_gridNode import TestGridNode
from .test_gridline import TestGridLine


class TestJacobianMatrix(TestCase):

    def create_test_data(self):
        grid_node_list = list()
        grid_node_list.append(
            GridNode("K0", 0,
                     TestGridNode.create_gridnode_parameter_list(p_load=1, q_load=0.5, volt=1, theta=0, p_inject=None,
                                                                 q_inject=None)))
        grid_node_list.append(
            GridNode("K1", 2, TestGridNode.create_gridnode_parameter_list(p_inject=1.5, p_load=0, q_load=0, volt=1,
                                                                          q_inject=None, theta=None)))
        grid_node_list.append(
            GridNode("K2", 1,
                     TestGridNode.create_gridnode_parameter_list(p_inject=0, q_inject=0, q_load=-1, p_load=-1,
                                                                 theta=None, volt=None)))

        grid_node_list.append(
            GridNode("K3", 1,
                     TestGridNode.create_gridnode_parameter_list(p_inject=0, q_inject=0, q_load=-1, p_load=-1,
                                                                 theta=None, volt=None)))

        grid_node_list.append(
            GridNode("K4", 1,
                     TestGridNode.create_gridnode_parameter_list(p_inject=0, q_inject=0, q_load=-1, p_load=-1,
                                                                 theta=None, volt=None)))

        grid_line_list = list()
        grid_line_list.append(GridLine(50, "K0", "K1", TestGridLine.test_create_line_parameters(1, 0, 0.1, None, None)))
        grid_line_list.append(GridLine(50, "K1", "K2", TestGridLine.test_create_line_parameters(1, 0, 0.1, None, None)))
        grid_line_list.append(GridLine(50, "K0", "K2", TestGridLine.test_create_line_parameters(1, 0, 0.1, None, None)))
        grid_line_list.append(GridLine(50, "K2", "K3", TestGridLine.test_create_line_parameters(1, 0, 0.1, None, None)))
        grid_line_list.append(GridLine(50, "K3", "K4", TestGridLine.test_create_line_parameters(1, 0, 0.1, None, None)))
        grid_line_list.append(GridLine(50, "K2", "K4", TestGridLine.test_create_line_parameters(1, 0, 0.1, None, None)))

        return grid_node_list, grid_line_list

    def test_create_jacobi_matrix(self):
        grid_node_list, grid_line_list = self.create_test_data()
        grid = Grid(grid_node_list=grid_node_list, grid_line_list=grid_line_list)
        grid.calc_bus_admittance_matrix()

        jacobi = JacobianMatrix(grid_node_list, grid.get_bus_admittance_matrix())
        invers_jacobi = np.linalg.inv(jacobi.Jk)
        det_Jk = np.linalg.det(jacobi.Jk)
        print('\nJakobimatrix:')
        print_matrix(jacobi.Jk)
        print('\ninverse Jakobimatrix:')
        print_matrix(invers_jacobi)

        assert det_Jk, 12000
