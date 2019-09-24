#   Copyright (C) 2019  Christian Klosterhalfen (TH Köln), Anjo Niewöhner (TH Köln)
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.


class Generator:
    """
        class to model generators connected to a grid node
    """

    def __init__(self, name, node, p_min, p_max, q_min, q_max):
        self.name = name
        self.node = node
        self.p_q_series = None
        self.p_min = p_min
        self.p_max = p_max
        self.q_min = q_min
        self.q_max = q_max

    def set_p_q_series(self, p_q_series):
        self.p_q_series = p_q_series
