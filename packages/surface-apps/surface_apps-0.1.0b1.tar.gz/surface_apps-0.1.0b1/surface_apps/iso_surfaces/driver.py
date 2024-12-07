# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#  Copyright (c) 2024 Mira Geoscience Ltd.                                     '
#                                                                              '
#  This file is part of surface-apps package.                                  '
#                                                                              '
#  All rights reserved.                                                        '
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

from __future__ import annotations

import logging
import sys

import numpy as np
from geoapps_utils.utils.formatters import string_name
from geoh5py.data.data import Data
from geoh5py.objects import ObjectBase, Surface
from geoh5py.shared.utils import fetch_active_workspace
from geoh5py.ui_json import InputFile

from surface_apps.driver import BaseSurfaceDriver
from surface_apps.iso_surfaces.params import IsoSurfaceParameters
from surface_apps.iso_surfaces.utils import entity_to_grid, extract_iso_surfaces


logger = logging.getLogger(__name__)


class IsoSurfacesDriver(BaseSurfaceDriver):
    """
    Driver for the detection of iso-surfaces within geoh5py objects.

    :param parameters: Application parameters.
    """

    _parameter_class = IsoSurfaceParameters

    def __init__(self, parameters: IsoSurfaceParameters | InputFile):
        super().__init__(parameters)

    def make_surfaces(self):
        """Make surface objects from iso-surfaces detected in source data."""

        with fetch_active_workspace(self.params.geoh5, mode="r+"):
            logger.info("Generating iso-surfaces ...")
            levels = self.params.detection.contours

            if len(levels) >= 1:
                surfaces = self.iso_surface(
                    self.params.source.objects,
                    self.params.source.data,
                    levels,
                    resolution=self.params.detection.resolution,
                    max_distance=self.params.detection.max_distance,
                    horizon=self.params.source.horizon,
                )

                results = []
                for surface, level in zip(surfaces, levels, strict=False):
                    if len(surface[0]) > 0 and len(surface[1]) > 0:
                        results += [
                            Surface.create(
                                self.params.geoh5,
                                name=string_name(
                                    self.params.source.data.name + f"_{level:.2e}"
                                ),
                                vertices=surface[0],
                                cells=surface[1],
                                parent=self.out_group,
                            )
                        ]

    @staticmethod
    def iso_surface(
        entity: ObjectBase,
        data: Data,
        levels: list,
        *,
        resolution: float = 100,
        max_distance: float = np.inf,
        horizon: Surface | None = None,
    ):
        """
        Generate 3D iso surface from an entity vertices or centroids and values.

        :param entity: Any entity with 'vertices' or 'centroids' attribute.
        :param data: Data objects whose values will be used to create iso-surfaces.
        :param levels: List of iso values
        :param max_distance: Maximum distance from input data to generate iso surface.
            Only used for input entities other than BlockModel.
        :param resolution: Grid size used to generate the iso surface.
            Only used for input entities other than BlockModel.
        :param horizon: Clipping surface to restrict interpolation from bleeding
            into the air.


        :returns surfaces: List of surfaces (one per levels) defined by
            vertices and cell indices.
            [(vertices, cells)_level_1, ..., (vertices, cells)_level_n]
        """

        logger.info("Converting entity and values to regular grid ...")
        grid, values = entity_to_grid(entity, data, resolution, max_distance, horizon)
        logger.info("Running marching cubes on levels ...")
        surfaces = extract_iso_surfaces(entity, grid, levels, values)

        return surfaces


if __name__ == "__main__":
    file = sys.argv[1]
    ifile = InputFile.read_ui_json(file)
    driver = IsoSurfacesDriver(ifile)
    driver.run()
