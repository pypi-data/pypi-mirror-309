import warnings
from multiprocessing import Array, Pool, cpu_count

import numpy as np
import SimpleITK as sitk
from rich import print
from rich.progress import track
from scipy.optimize import curve_fit

from asltk.asldata import ASLData
from asltk.mri_parameters import MRIParameters
from asltk.utils import (
    asl_model_buxton,
    asl_model_multi_dw,
    asl_model_multi_te,
)

# Global variables to assist multi cpu threading
cbf_map = None
att_map = None
brain_mask = None
asl_data = None
ld_arr = None
pld_arr = None
te_arr = None
tblgm_map = None
t2bl = None
t2gm = None


class CBFMapping(MRIParameters):
    def __init__(self, asl_data: ASLData) -> None:
        """Basic CBFMapping constructor.

        Notes:
            The ASLData is the base data used in the object constructor.
            In order to create the CBF map correctly, a proper ASLData must be
            provided. Check whether the ASLData given as input is defined
            correctly

        Examples:
            The default MRIParameters are used as default in the object
            constructor
            >>> asl_data = ASLData(pcasl='./tests/files/pcasl_mte.nii.gz',m0='./tests/files/m0.nii.gz')
            >>> cbf = CBFMapping(asl_data)
            >>> cbf.get_constant('T1csf')
            1400.0

            If the user want to change the MRIParameter value, for a specific
            object, one can change it directly:
            >>> cbf.set_constant(1600.0, 'T1csf')
            >>> cbf.get_constant('T1csf')
            1600.0
            >>> default_param = MRIParameters()
            >>> default_param.get_constant('T1csf')
            1400.0

        Args:
            asl_data (ASLData): The ASL data object (ASLData)
        """
        super().__init__()
        self._asl_data = asl_data
        if self._asl_data('m0') is None:
            raise ValueError(
                'ASLData is incomplete. CBFMapping need pcasl and m0 images.'
            )

        self._brain_mask = np.ones(self._asl_data('m0').shape)
        self._cbf_map = np.zeros(self._asl_data('m0').shape)
        self._att_map = np.zeros(self._asl_data('m0').shape)

    def set_brain_mask(self, brain_mask: np.ndarray, label: int = 1):
        """Defines whether a brain a mask is applied to the CBFMapping
        calculation

        A image mask is simply an image that defines the voxels where the ASL
        calculation should be made. Basically any integer value can be used as
        proper label mask.

        A most common approach is to use a binary image (zeros for background
        and 1 for the brain tissues). Anyway, the default behavior of the
        method can transform a integer-pixel values image to a binary mask with
        the `label` parameter provided by the user

        Args:
            brain_mask (np.ndarray): The image representing the brain mask label (int, optional): The label value used to define the foreground tissue (brain). Defaults to 1.
        """
        _check_mask_values(brain_mask, label, self._asl_data('m0').shape)

        binary_mask = (brain_mask == label).astype(np.uint8) * label
        self._brain_mask = binary_mask

    def get_brain_mask(self):
        """Get the brain mask image

        Returns:
            (np.ndarray): The brain mask image
        """
        return self._brain_mask

    def create_map(
        self,
        ub=[1.0, 5000.0],
        lb=[0.0, 0.0],
        par0=[1e-5, 1000],
        cores: int = cpu_count(),
    ):
        """Create the CBF and also ATT maps

        Note:
            By default the ATT map is already calculated using the same Buxton
            formalism. Once the CBFMapping.create_map() method is called, both
            CBF and ATT maps are given in the output.

        Note:
            The CBF maps is given in two formats: the original pixel scale,
            resulted from the non-linear Buxton model fitting, and also
            a normalized version with the correct units of mL/100 g/min. In the
            output dictionary the user can select the 'cbf' and 'cbf_norm'
            options

        Args:
            ub (list, optional): The upper limit values. Defaults to [1.0, 5000.0].
            lb (list, optional): The lower limit values. Defaults to [0.0, 0.0].
            par0 (list, optional): The initial guess parameter for non-linear fitting. Defaults to [1e-5, 1000].
            cores (int, optional): Defines how many CPU threads can be used for the class. Defaults is using all the availble threads.

        Returns:
            (dict): A dictionary with 'cbf', 'att' and 'cbf_norm'
        """
        if (cores < 0) or (cores > cpu_count()) or not isinstance(cores, int):
            raise ValueError(
                'Number of proecess must be at least 1 and less than maximum cores availble.'
            )
        if (
            len(self._asl_data.get_ld()) == 0
            or len(self._asl_data.get_pld()) == 0
        ):
            raise ValueError('LD or PLD list of values must be provided.')
        # TODO Testar se retirando esse if do LD PLD sizes, continua rodando... isso é erro do ASLData

        global asl_data, brain_mask
        asl_data = self._asl_data
        brain_mask = self._brain_mask

        BuxtonX = [self._asl_data.get_ld(), self._asl_data.get_pld()]

        x_axis, y_axis, z_axis = (
            self._asl_data('m0').shape[2],
            self._asl_data('m0').shape[1],
            self._asl_data('m0').shape[0],
        )

        cbf_map_shared = Array('d', z_axis * y_axis * x_axis, lock=False)
        att_map_shared = Array('d', z_axis * y_axis * x_axis, lock=False)

        with Pool(
            processes=cores,
            initializer=_cbf_init_globals,
            initargs=(cbf_map_shared, att_map_shared, brain_mask, asl_data),
        ) as pool:
            pool.starmap(
                _cbf_process_slice,
                [
                    (i, x_axis, y_axis, z_axis, BuxtonX, par0, lb, ub)
                    for i in track(
                        range(x_axis), description='CBF/ATT processing...'
                    )
                ],
            )

        self._cbf_map = np.frombuffer(cbf_map_shared).reshape(
            z_axis, y_axis, x_axis
        )
        self._att_map = np.frombuffer(att_map_shared).reshape(
            z_axis, y_axis, x_axis
        )

        return {
            'cbf': self._cbf_map,
            'cbf_norm': self._cbf_map * (60 * 60 * 1000),
            'att': self._att_map,
        }


def _cbf_init_globals(
    cbf_map_, att_map_, brain_mask_, asl_data_
):   # pragma: no cover
    # indirect call method by CBFMapping().create_map()
    global cbf_map, att_map, brain_mask, asl_data
    cbf_map = cbf_map_
    att_map = att_map_
    brain_mask = brain_mask_
    asl_data = asl_data_


def _cbf_process_slice(
    i, x_axis, y_axis, z_axis, BuxtonX, par0, lb, ub
):   # pragma: no cover
    # indirect call method by CBFMapping().create_map()
    for j in range(y_axis):
        for k in range(z_axis):
            if brain_mask[k, j, i] != 0:
                m0_px = asl_data('m0')[k, j, i]

                def mod_buxton(Xdata, par1, par2):
                    return asl_model_buxton(
                        Xdata[0], Xdata[1], m0_px, par1, par2
                    )

                Ydata = asl_data('pcasl')[0, :, k, j, i]

                # Calculate the processing index for the 3D space
                index = k * (y_axis * x_axis) + j * x_axis + i

                try:
                    par_fit, _ = curve_fit(
                        mod_buxton, BuxtonX, Ydata, p0=par0, bounds=(lb, ub)
                    )
                    cbf_map[index] = par_fit[0]
                    att_map[index] = par_fit[1]
                except RuntimeError:
                    cbf_map[index] = 0.0
                    att_map[index] = 0.0


class MultiTE_ASLMapping(MRIParameters):
    def __init__(self, asl_data: ASLData) -> None:
        """Basic MultiTE_ASLMapping constructor

        Notes:
            The ASLData is the base data used in the object constructor.
            In order to create the CBF map correctly, a proper ASLData must be
            provided. Check whether the ASLData given as input is defined
            correctly. In particular, it must provide the `te_values` list of
            values in the ASLData object

        Examples:
            The default MRIParameters are used as default in the object
            constructor
            >>> asl_data = ASLData(pcasl='./tests/files/pcasl_mte.nii.gz',m0='./tests/files/m0.nii.gz', te_values=[13.2, 25.7, 50.4])
            >>> mte = MultiTE_ASLMapping(asl_data)
            >>> mte.get_constant('T1csf')
            1400.0

            If the user want to change the MRIParameter value, for a specific
            object, one can change it directly:
            >>> mte.set_constant(1600.0, 'T1csf')
            >>> mte.get_constant('T1csf')
            1600.0
            >>> default_param = MRIParameters()
            >>> default_param.get_constant('T1csf')
            1400.0

        Args:
            asl_data (ASLData): The ASL data object (ASLData)

        Raises:
            ValueError: Raises when an incomplete ASLData object is provided
        """
        super().__init__()
        self._asl_data = asl_data
        self._basic_maps = CBFMapping(asl_data)
        if self._asl_data.get_te() is None:
            raise ValueError(
                'ASLData is incomplete. MultiTE_ASLMapping need a list of TE values.'
            )

        self._brain_mask = np.ones(self._asl_data('m0').shape)
        self._cbf_map = np.zeros(self._asl_data('m0').shape)
        self._att_map = np.zeros(self._asl_data('m0').shape)
        self._t1blgm_map = np.zeros(self._asl_data('m0').shape)

    def set_brain_mask(self, brain_mask: np.ndarray, label: int = 1):
        """Defines whether a brain a mask is applied to the CBFMapping
        calculation

        A image mask is simply an image that defines the voxels where the ASL
        calculation should be made. Basically any integer value can be used as
        proper label mask.

        A most common approach is to use a binary image (zeros for background
        and 1 for the brain tissues). Anyway, the default behavior of the
        method can transform a integer-pixel values image to a binary mask with
        the `label` parameter provided by the user

        Args:
            brain_mask (np.ndarray): The image representing the brain mask label (int, optional): The label value used to define the foreground tissue (brain). Defaults to 1.
        """
        _check_mask_values(brain_mask, label, self._asl_data('m0').shape)

        binary_mask = (brain_mask == label).astype(np.uint8) * label
        self._brain_mask = binary_mask

    def get_brain_mask(self):
        """Get the brain mask image

        Returns:
            (np.ndarray): The brain mask image
        """
        return self._brain_mask

    def set_cbf_map(self, cbf_map: np.ndarray):
        """Set the CBF map to the MultiTE_ASLMapping object.

        Note:
            The CBF maps must have the original scale in order to calculate the
            T1blGM map correclty. Hence, if the CBF map was made using
            CBFMapping class, one can use the 'cbf' output.

        Args:
            cbf_map (np.ndarray): The CBF map that is set in the MultiTE_ASLMapping object
        """
        self._cbf_map = cbf_map

    def get_cbf_map(self) -> np.ndarray:
        """Get the CBF map storaged at the MultiTE_ASLMapping object

        Returns:
            (np.ndarray): The CBF map that is storaged in the
            MultiTE_ASLMapping object
        """
        return self._cbf_map

    def set_att_map(self, att_map: np.ndarray):
        """Set the ATT map to the MultiTE_ASLMapping object.

        Args:
            att_map (np.ndarray): The ATT map that is set in the MultiTE_ASLMapping object
        """
        self._att_map = att_map

    def get_att_map(self):
        """Get the ATT map storaged at the MultiTE_ASLMapping object

        Returns:
            (np.ndarray): _description_
        """
        return self._att_map

    def create_map(
        self,
        ub: list = [np.inf],
        lb: list = [0.0],
        par0: list = [400],
        cores=cpu_count(),
    ):
        """Create the T1 relaxation exchange between blood and Grey Matter (GM)
        , i.e. the T1blGM map resulted from the multi-compartiment TE ASL model.

        Reference:  Ultra-long-TE arterial spin labeling reveals rapid and
        brain-wide blood-to-CSF water transport in humans, NeuroImage,
        doi: 10.1016/j.neuroimage.2021.118755

        Note:
            The CBF and ATT maps can be provided before calling this method,
            using the proper set/get methods for each map. If the user does not
            provide these maps, a new calculation is automatically made using
            the default execution implemented at CBFMapping class.

        Note:
            The CBF map must be at the original scale to perform the correct
            multiTE-ASL model. Therefore, provide the 'cbf' output.

        The method assumes that the fine tunning map can be approached using
        the adpted initial guess (parameter par0). Hence, the generated T1blGM
        map applies a cut-off using only positive values (`>0`) and upper limit
        of four times the initial guess (`4 * par0`).

        Note:
            It is a good practive to apply a spatial smoothing in the output
            T1blGM map, in order to improve SNR. However, the `create_map`
            method does not applies any image filter as default.

        Args:
            ub (list, optional): The upper limit values. Defaults to [1.0, 5000.0].
            lb (list, optional): The lower limit values. Defaults to [0.0, 0.0].
            par0 (list, optional): The initial guess parameter for non-linear fitting. Defaults to [1e-5, 1000].
            cores (int, optional): Defines how many CPU threads can be used for the class. Defaults is using all the availble threads.

        Returns:
            (dict): A dictionary with 'cbf', 'att' and 'cbf_norm'
        """
        # # TODO As entradas ub, lb e par0 não são aplicadas para CBF. Pensar se precisa ter essa flexibilidade para acertar o CBF interno à chamada
        self._basic_maps.set_brain_mask(self._brain_mask)

        basic_maps = {'cbf': self._cbf_map, 'att': self._att_map}
        if np.mean(self._cbf_map) == 0 or np.mean(self._att_map) == 0:
            # If the CBF/ATT maps are zero (empty), then a new one is created
            print(
                '[blue][INFO] The CBF/ATT map were not provided. Creating these maps before next step...'
            )
            basic_maps = self._basic_maps.create_map()
            self._cbf_map = basic_maps['cbf']
            self._att_map = basic_maps['att']

        global asl_data, brain_mask, cbf_map, att_map, t2bl, t2gm
        asl_data = self._asl_data
        brain_mask = self._brain_mask
        cbf_map = self._cbf_map
        att_map = self._att_map
        ld_arr = self._asl_data.get_ld()
        pld_arr = self._asl_data.get_pld()
        te_arr = self._asl_data.get_te()
        t2bl = self.T2bl
        t2gm = self.T2gm

        x_axis = self._asl_data('m0').shape[2]   # height
        y_axis = self._asl_data('m0').shape[1]   # width
        z_axis = self._asl_data('m0').shape[0]   # depth

        tblgm_map_shared = Array('d', z_axis * y_axis * x_axis, lock=False)

        with Pool(
            processes=cores,
            initializer=_multite_init_globals,
            initargs=(
                cbf_map,
                att_map,
                brain_mask,
                asl_data,
                ld_arr,
                pld_arr,
                te_arr,
                tblgm_map_shared,
                t2bl,
                t2gm,
            ),
        ) as pool:
            pool.starmap(
                _tblgm_multite_process_slice,
                [
                    (i, x_axis, y_axis, z_axis, par0, lb, ub)
                    for i in track(
                        range(x_axis), description='multiTE-ASL processing...'
                    )
                ],
            )

        self._t1blgm_map = np.frombuffer(tblgm_map_shared).reshape(
            z_axis, y_axis, x_axis
        )

        # Adjusting output image boundaries
        self._t1blgm_map = self._adjust_image_limits(self._t1blgm_map, par0[0])

        return {
            'cbf': self._cbf_map,
            'cbf_norm': self._cbf_map * (60 * 60 * 1000),
            'att': self._att_map,
            't1blgm': self._t1blgm_map,
        }

    def _adjust_image_limits(self, map, init_guess):
        img = sitk.GetImageFromArray(map)
        thr_filter = sitk.ThresholdImageFilter()
        thr_filter.SetUpper(
            4 * init_guess
        )   # assuming upper to 4x the initial guess
        thr_filter.SetLower(0.0)
        img = thr_filter.Execute(img)

        return sitk.GetArrayFromImage(img)


def _multite_init_globals(
    cbf_map_,
    att_map_,
    brain_mask_,
    asl_data_,
    ld_arr_,
    pld_arr_,
    te_arr_,
    tblgm_map_,
    t2bl_,
    t2gm_,
):   # pragma: no cover
    # indirect call method by CBFMapping().create_map()
    global cbf_map, att_map, brain_mask, asl_data, ld_arr, te_arr, pld_arr, tblgm_map, t2bl, t2gm
    cbf_map = cbf_map_
    att_map = att_map_
    brain_mask = brain_mask_
    asl_data = asl_data_
    ld_arr = ld_arr_
    pld_arr = pld_arr_
    te_arr = te_arr_
    tblgm_map = tblgm_map_
    t2bl = t2bl_
    t2gm = t2gm_


def _tblgm_multite_process_slice(
    i, x_axis, y_axis, z_axis, par0, lb, ub
):   # pragma: no cover
    # indirect call method by CBFMapping().create_map()
    for j in range(y_axis):
        for k in range(z_axis):
            if brain_mask[k, j, i] != 0:
                m0_px = asl_data('m0')[k, j, i]

                def mod_2comp(Xdata, par1):
                    return asl_model_multi_te(
                        Xdata[:, 0],
                        Xdata[:, 1],
                        Xdata[:, 2],
                        m0_px,
                        cbf_map[k, j, i],
                        att_map[k, j, i],
                        par1,
                        t2bl,
                        t2gm,
                    )

                Ydata = (
                    asl_data('pcasl')[:, :, k, j, i]
                    .reshape(
                        (
                            len(ld_arr) * len(te_arr),
                            1,
                        )
                    )
                    .flatten()
                )

                # Calculate the processing index for the 3D space
                index = k * (y_axis * x_axis) + j * x_axis + i

                try:
                    Xdata = _multite_create_x_data(
                        ld_arr,
                        pld_arr,
                        te_arr,
                    )
                    par_fit, _ = curve_fit(
                        mod_2comp,
                        Xdata,
                        Ydata,
                        p0=par0,
                        bounds=(lb, ub),
                    )
                    tblgm_map[index] = par_fit[0]
                except RuntimeError:   # pragma: no cover
                    tblgm_map[index] = 0.0


def _multite_create_x_data(ld, pld, te):   # pragma: no cover
    # array for the x values, assuming an arbitrary size based on the PLD
    # and TE vector size
    Xdata = np.zeros((len(pld) * len(te), 3))

    count = 0
    for i in range(len(pld)):
        for j in range(len(te)):
            Xdata[count] = [ld[i], pld[i], te[j]]
            count += 1

    return Xdata


class MultiDW_ASLMapping(MRIParameters):
    def __init__(self, asl_data: ASLData):
        super().__init__()
        self._asl_data = asl_data
        self._basic_maps = CBFMapping(asl_data)
        if self._asl_data.get_dw() is None:
            raise ValueError(
                'ASLData is incomplete. MultiDW_ASLMapping need a list of DW values.'
            )

        self._brain_mask = np.ones(self._asl_data('m0').shape)
        self._cbf_map = np.zeros(self._asl_data('m0').shape)
        self._att_map = np.zeros(self._asl_data('m0').shape)

        self._b_values = self._asl_data.get_dw()
        # self._A1 = np.zeros(tuple([len(self._b_values)]) + self._asl_data('m0').shape)
        self._A1 = np.zeros(self._asl_data('m0').shape)
        # self._D1 = np.zeros(tuple([1]) +self._asl_data('m0').shape)
        self._D1 = np.zeros(self._asl_data('m0').shape)
        self._A2 = np.zeros(self._asl_data('m0').shape)
        # self._A2 = np.zeros(tuple([len(self._b_values)])  + self._asl_data('m0').shape)
        # self._D2 = np.zeros(tuple([1]) +self._asl_data('m0').shape)
        self._D2 = np.zeros(self._asl_data('m0').shape)
        self._kw = np.zeros(self._asl_data('m0').shape)

    def set_brain_mask(self, brain_mask: np.ndarray, label: int = 1):
        """Defines whether a brain a mask is applied to the MultiDW_ASLMapping
        calculation

        A image mask is simply an image that defines the voxels where the ASL
        calculation should be made. Basically any integer value can be used as
        proper label mask.

        A most common approach is to use a binary image (zeros for background
        and 1 for the brain tissues). Anyway, the default behavior of the
        method can transform a integer-pixel values image to a binary mask with
        the `label` parameter provided by the user

        Args:
            brain_mask (np.ndarray): The image representing the brain mask label (int, optional): The label value used to define the foreground tissue (brain). Defaults to 1.
        """
        _check_mask_values(brain_mask, label, self._asl_data('m0').shape)

        binary_mask = (brain_mask == label).astype(np.uint8) * label
        self._brain_mask = binary_mask

    def get_brain_mask(self):
        """Get the brain mask image

        Returns:
            (np.ndarray): The brain mask image
        """
        return self._brain_mask

    def set_cbf_map(self, cbf_map: np.ndarray):
        """Set the CBF map to the MultiDW_ASLMapping object.

        Note:
            The CBF maps must have the original scale in order to calculate the
            T1blGM map correclty. Hence, if the CBF map was made using
            CBFMapping class, one can use the 'cbf' output.

        Args:
            cbf_map (np.ndarray): The CBF map that is set in the MultiDW_ASLMapping object
        """
        self._cbf_map = cbf_map

    def get_cbf_map(self) -> np.ndarray:
        """Get the CBF map storaged at the MultiDW_ASLMapping object

        Returns:
            (np.ndarray): The CBF map that is storaged in the
            MultiDW_ASLMapping object
        """
        return self._cbf_map

    def set_att_map(self, att_map: np.ndarray):
        """Set the ATT map to the MultiDW_ASLMapping object.

        Args:
            att_map (np.ndarray): The ATT map that is set in the MultiDW_ASLMapping object
        """
        self._att_map = att_map

    def get_att_map(self):
        """Get the ATT map storaged at the MultiDW_ASLMapping object

        Returns:
            (np.ndarray): _description_
        """
        return self._att_map

    def create_map(
        self,
        lb: list = [0.0, 0.0, 0.0, 0.0],
        ub: list = [np.inf, np.inf, np.inf, np.inf],
        par0: list = [0.5, 0.000005, 0.5, 0.000005],
    ):
        self._basic_maps.set_brain_mask(self._brain_mask)

        basic_maps = {'cbf': self._cbf_map, 'att': self._att_map}
        if np.mean(self._cbf_map) == 0 or np.mean(self._att_map) == 0:
            # If the CBF/ATT maps are zero (empty), then a new one is created
            print(
                '[blue][INFO] The CBF/ATT map were not provided. Creating these maps before next step...'
            )   # pragma: no cover
            basic_maps = self._basic_maps.create_map()   # pragma: no cover
            self._cbf_map = basic_maps['cbf']   # pragma: no cover
            self._att_map = basic_maps['att']   # pragma: no cover

        x_axis = self._asl_data('m0').shape[2]   # height
        y_axis = self._asl_data('m0').shape[1]   # width
        z_axis = self._asl_data('m0').shape[0]   # depth

        for i in track(
            range(x_axis), description='[green]multiDW-ASL processing...'
        ):
            for j in range(y_axis):
                for k in range(z_axis):
                    if self._brain_mask[k, j, i] != 0:
                        # Calculates the diffusion components for (A1, D1), (A2, D2)
                        def mod_diff(Xdata, par1, par2, par3, par4):
                            return asl_model_multi_dw(
                                b_values=Xdata,
                                A1=par1,
                                D1=par2,
                                A2=par3,
                                D2=par4,
                            )

                        # M(t,b)/M(t,0)
                        Ydata = (
                            self._asl_data('pcasl')[:, :, k, j, i]
                            .reshape(
                                (
                                    len(self._asl_data.get_ld())
                                    * len(self._asl_data.get_dw()),
                                    1,
                                )
                            )
                            .flatten()
                            / self._asl_data('m0')[k, j, i]
                        )

                        try:
                            # Xdata = self._b_values
                            Xdata = self._create_x_data(
                                self._asl_data.get_ld(),
                                self._asl_data.get_pld(),
                                self._asl_data.get_dw(),
                            )

                            par_fit, _ = curve_fit(
                                mod_diff,
                                Xdata[:, 2],
                                Ydata,
                                p0=par0,
                                bounds=(lb, ub),
                            )
                            self._A1[k, j, i] = par_fit[0]
                            self._D1[k, j, i] = par_fit[1]
                            self._A2[k, j, i] = par_fit[2]
                            self._D2[k, j, i] = par_fit[3]
                        except RuntimeError:
                            self._A1[k, j, i] = 0
                            self._D1[k, j, i] = 0
                            self._A2[k, j, i] = 0
                            self._D2[k, j, i] = 0

                        # Calculates the Mc fitting to alpha = kw + T1blood
                        m0_px = self._asl_data('m0')[k, j, i]

                        # def mod_2comp(Xdata, par1):
                        #     ...
                        #     # return asl_model_multi_te(
                        #     #     Xdata[:, 0],
                        #     #     Xdata[:, 1],
                        #     #     Xdata[:, 2],
                        #     #     m0_px,
                        #     #     basic_maps['cbf'][k, j, i],
                        #     #     basic_maps['att'][k, j, i],
                        #     #     par1,
                        #     #     self.T2bl,
                        #     #     self.T2gm,
                        #     # )

                        # Ydata = (
                        #     self._asl_data('pcasl')[:, :, k, j, i]
                        #     .reshape(
                        #         (
                        #             len(self._asl_data.get_ld())
                        #             * len(self._asl_data.get_te()),
                        #             1,
                        #         )
                        #     )
                        #     .flatten()
                        # )

                        # try:
                        #     Xdata = self._create_x_data(
                        #         self._asl_data.get_ld(),
                        #         self._asl_data.get_pld(),
                        #         self._asl_data.get_dw(),
                        #     )
                        #     par_fit, _ = curve_fit(
                        #         mod_2comp,
                        #         Xdata,
                        #         Ydata,
                        #         p0=par0,
                        #         bounds=(lb, ub),
                        #     )
                        #     self._kw[k, j, i] = par_fit[0]
                        # except RuntimeError:
                        #     self._kw[k, j, i] = 0.0

        # # Adjusting output image boundaries
        # self._kw = self._adjust_image_limits(self._kw, par0[0])

        return {
            'cbf': self._cbf_map,
            'cbf_norm': self._cbf_map * (60 * 60 * 1000),
            'att': self._att_map,
            'a1': self._A1,
            'd1': self._D1,
            'a2': self._A2,
            'd2': self._D2,
            'kw': self._kw,
        }

    def _create_x_data(self, ld, pld, dw):
        # array for the x values, assuming an arbitrary size based on the PLD
        # and TE vector size
        Xdata = np.zeros((len(pld) * len(dw), 3))

        count = 0
        for i in range(len(pld)):
            for j in range(len(dw)):
                Xdata[count] = [ld[i], pld[i], dw[j]]
                count += 1

        return Xdata


def _check_mask_values(mask, label, ref_shape):
    # Check wheter mask input is an numpy array
    if not isinstance(mask, np.ndarray):
        raise TypeError(f'mask is not an numpy array. Type {type(mask)}')

    # Check whether the mask provided is a binary image
    unique_values = np.unique(mask)
    if unique_values.size > 2:
        warnings.warn(
            'Mask image is not a binary image. Any value > 0 will be assumed as brain label.',
            UserWarning,
        )

    # Check whether the label value is found in the mask image
    label_ok = False
    for value in unique_values:
        if label == value:
            label_ok = True
            break
    if not label_ok:
        raise ValueError('Label value is not found in the mask provided.')

    # Check whether the dimensions between mask and input volume matches
    mask_shape = mask.shape
    if mask_shape != ref_shape:
        raise TypeError(
            f'Image mask dimension does not match with input 3D volume. Mask shape {mask_shape} not equal to {ref_shape}'
        )
