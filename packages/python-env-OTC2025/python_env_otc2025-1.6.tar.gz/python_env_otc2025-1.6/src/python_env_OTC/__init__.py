#
#

# @author: <sylvain.herledan@oceandatalab.com>
# @date: 2024-11-12

"""
This module checks that the Python environment is ready for the OTC 2025
interactive lectures based on SEAScope.
"""

import os
import sys
import json
import typing
import psutil
import GPUtil
import logging
import platform
import datetime
import traceback
import subprocess  # nosec

logger = logging.getLogger(__name__)


def get_context() -> typing.Dict[str, typing.Dict[str, str]]:
    """Get information about the operating system, hardware and environment"""
    ctx = {}

    ctx['env'] = dict(os.environ.items())
    ctx['os'] = platform.uname()._asdict()
    ctx['python'] = {'int_info': sys.int_info.__str__(),
                     'float_info': sys.float_info.__str__(),
                     'thread_info': sys.thread_info.__str__(),
                     'encoding': sys.getfilesystemencoding(),
                     'path': ','.join([x for x in sys.path if 0 < len(x)])}
    ctx['cpu'] = {'cores': psutil.cpu_count(logical=False),
                  'threads': psutil.cpu_count(logical=True)}
    try:
        ctx['cpu']['min_freq'] = psutil.cpu_freq().min
        ctx['cpu']['max_freq'] = psutil.cpu_freq().max
    except FileNotFoundError:
        # Access CPU frequency information may not be implemented on Apple M1
        # as Ziad mentioned:
        # https://github.com/giampaolo/psutil/issues/1892
        pass
    ctx['gpu'] = {_.name: '{} @ {}% ({} / {} MB) - {}C'.format(_.driver,
                                                               _.load * 100,
                                                               _.memoryUsed,
                                                               _.memoryTotal,
                                                               _.temperature)
                  for _ in GPUtil.getGPUs()}
    ctx['memory'] = psutil.virtual_memory()._asdict()
    ctx['network'] = dict(psutil.net_if_addrs().items())
    ctx['storage'] = {_.device: '{} ({})'.format(_.mountpoint, _.fstype)
                      for _ in psutil.disk_partitions()}

    return ctx


def check_python_version() -> typing.Tuple[bool, str]:
    """Check that Python version is at least 3.12"""

    if (3, 12) > sys.version_info:
        return False, sys.version
    return True, sys.version


def check_install_directory() -> typing.Tuple[bool, str]:
    """Check that the virtual environment is a sibling to the directory used
    as the SEAScope workspace.

    Installing the virtual environment there is not mandatory, but it will be
    much easier to provide instructions during the training if all students can
    find the virtual environment at the same location."""
    import os
    venv_path = os.environ.get('VIRTUAL_ENV', None)
    if venv_path is None:
        return False, 'Python virtual environment not loaded'

    otc25_path = os.path.dirname(venv_path)

    # Look for the seascope directory
    seascope_path = os.path.join(otc25_path, 'seascope')

    # Look for files and directories that should be in the SEAScope workspace,
    # assuming SEAScope has been executed at least once
    config_path = os.path.join(seascope_path, 'config.ini')
    colormaps_path = os.path.join(seascope_path, 'colormaps')
    state_path = os.path.join(seascope_path, 'state.db')

    if not os.path.isdir(seascope_path):
        return False, f'Directory "{seascope_path}" not found'
    if not os.path.isdir(colormaps_path):
        return False, f'Directory "{colormaps_path}" not found'

    if not os.path.isfile(config_path):
        return False, f'File "{config_path}" not found'

    if not os.path.isfile(state_path):
        return False, f'File "{state_path}" not found'

    msg = f'Environment "{venv_path}" is next to the SEAScope workspace'
    return True, msg


def check_numpy() -> typing.Tuple[bool, str]:
    """Check that the numpy package can be loaded"""
    import numpy
    version = numpy.__version__
    return True, version


def check_scipy() -> typing.Tuple[bool, str]:
    """Check that the scipy package can be loaded"""
    import scipy
    version = '{} (numpy: {})'.format(scipy.__version__,
                                      scipy.__numpy_version__)
    return True, version


def check_matplotlib() -> typing.Tuple[bool, str]:
    """Check that the matplotlib package can be loaded and that it can draw
    an offscreen plot"""
    import matplotlib
    version = '{} ({})'.format(matplotlib._get_version(),
                               matplotlib.get_backend())

    import matplotlib.pyplot
    matplotlib.pyplot.plot([x for x in range(0, 50)])
    matplotlib.pyplot.close()

    return True, version


def check_netCDF4() -> typing.Tuple[bool, str]:
    """Check that the netCDF4 package can be loaded and that netCDF file can
    be read"""
    import netCDF4
    version = '{} (netCDF4 {}, HDF5 {})'.format(netCDF4.__version__,
                                                netCDF4.__netcdf4libversion__,
                                                netCDF4.__hdf5libversion__)
    return True, version


def check_SEAScope() -> typing.Tuple[bool, str]:
    """Check that the SEAScope package can be loaded"""
    import SEAScope
    version = SEAScope.__version__
    return True, version


def check_idf_converter() -> typing.Tuple[bool, str]:
    """Check that the idf-converter package can be loaded"""
    import idf_converter
    version = idf_converter.__version__
    return True, version


def check_jupyterlab() -> typing.Tuple[bool, str]:
    """Check that the jupyterlab package can be loaded"""
    import jupyterlab
    version = jupyterlab.__version__
    return True, version


def check_cartopy() -> typing.Tuple[bool, str]:
    """Check that the cartopy package can be loaded AND used"""
    try:
        import cartopy.crs
        import matplotlib.pyplot

        ax = matplotlib.pyplot.axes(projection=cartopy.crs.PlateCarree())
        ax.coastlines()
    except:  # noqa
        _, e, _ = sys.exc_info()
        return False, str(e)

    return True, 'cartopy ok'


def check_fluxengine() -> typing.Tuple[bool, str]:
    """Check that the fluxengine is installed and has been patched"""
    try:
        import fluxengine
    except ImportError as e:
        return False, str(e)

    try:
        import fluxengine.core.fe_setup_tools
        dummy = {'k_parameterisation': 'k_Nightingale2000'}
        _ = fluxengine.core.fe_setup_tools.build_k_functor(dummy, None)
    except ImportError as e:
        return False, str(e)
    except AttributeError:
        return False, 'inspect.getargsspec not patched'

    try:
        import numpy
        import fluxengine.tools.reanalyse_fco2.v2_f_conversion
        conv_f = fluxengine.tools.reanalyse_fco2.v2_f_conversion
        data_array = {'year': numpy.array([0]),
                      'month': numpy.array([0]),
                      'day': numpy.array([0]),
                      'hour': numpy.array([0]),
                      'minute': numpy.array([0]),
                      'second': numpy.array([0]),
                      'longitude': numpy.array([0.0]),
                      'latitude': numpy.array([0.0]),
                      'sst': numpy.array([0.0]),
                      'salinity': numpy.array([0.0]),
                      'T_equ': numpy.array([0.0]),
                      'air_pressure': numpy.array([0.0]),
                      'air_pressure_equ': numpy.array([0.0]),
                      'salinity_sub': numpy.array([0.0]),
                      'air_pressure_sub': numpy.array([0.0]),
                      'fCO2': numpy.array([0.0])}
        _ = conv_f.v2_f_conversion_wrap(numpy.array([0.0]), data_array,
                                        numpy.array([1.0]), numpy.array([1.0]))
    except ImportError as e:
        return False, str(e)
    except AttributeError:
        return False, 'numpy deprecated aliases not patched'

    return True, 'FluxEngine installed and patched'


def check_xarray() -> typing.Tuple[bool, str]:
    """"""
    try:
        import xarray
        ds = xarray.tutorial.load_dataset("air_temperature")
        air = ds.air.isel(time=[0, 724]) - 273.15
    except:  # noqa
        _, e, _ = sys.exc_info()
        return False, str(e)

    try:
        # This is the map projection we want to plot *onto*
        import cartopy.crs
        map_proj = cartopy.crs.LambertConformal(central_longitude=-95,
                                                central_latitude=45)
    except:  # noqa
        return False, "partial test due to cartopy error"

        p = air.plot(
            transform=cartopy.crs.PlateCarree(),  # the data's projection
            col="time",
            col_wrap=1,  # multiplot settings
            aspect=ds.dims["lon"] / ds.dims["lat"],  # for a sensible figsize
            subplot_kws={"projection": map_proj},
            )  # the plot's projection

        # We have to set the map's options on all axes
        for ax in p.axes.flat:
            ax.coastlines()
            ax.set_extent([-160, -30, 5, 75])

    return True, 'xarray ok'


def check_dask() -> typing.Tuple[bool, str]:
    """"""
    try:
        import dask.array

        x = dask.array.random.random((10000, 10000))
        y = (x + x.T) - x.mean(axis=1)

        _ = y.var(axis=0).compute()
    except:  # noqa
        _, e, _ = sys.exc_info()
        return False, str(e)

    try:
        import pandas
        import numpy
        import time
        import random

        def costly_simulation(list_param):
            time.sleep(random.random())
            return sum(list_param)

        input_params = pandas.DataFrame(numpy.random.random(size=(20, 4)),
                                        columns=['param_a', 'param_b',
                                                 'param_c', 'param_d'])
    except:  # noqa
        return False, "partial test due to pandas/numpy error"

    futures = []
    try:
        from dask.distributed import Client
        client = Client(threads_per_worker=4, n_workers=1)
        for parameters in input_params.values:
            future = client.submit(costly_simulation, parameters)
            futures.append(future)
        _ = client.gather(futures)
        client.close()
    except:  # noqa
        _, e, _ = sys.exc_info()
        return False, str(e)

    return True, 'dask ok'


def check_SEAScope_connection() -> typing.Tuple[bool, str]:
    """Check that it is possible to connect to SEAScope"""
    import SEAScope.upload

    with SEAScope.upload.connect('localhost', 11155):
        pass

    return True, 'Connection ok'


def check_upload() -> typing.Tuple[bool, str]:
    """Check that commands can be sent to SEAScope by creating an empty
    collection  using SEAScope bindings"""
    import SEAScope.upload
    import SEAScope.lib.utils

    name = 'Empty collection'
    collection_id, collection = SEAScope.lib.utils.create_collection(name)
    with SEAScope.upload.connect('localhost', 11155) as link:
        SEAScope.upload.collection(link, collection)

    return True, 'Collection created with ID = {}'.format(collection_id)


def check_download() -> typing.Tuple[bool, str]:
    """Check that information can be retrieved from SEAScope by getting the
    current datetime selected in the application using SEAScope bindings"""

    import struct
    import SEAScope.upload
    import SEAScope.cmds.get_current_datetime

    serializer = SEAScope.cmds.get_current_datetime.serialize
    deserializer = SEAScope.cmds.get_current_datetime.deserialize

    with SEAScope.upload.connect('localhost', 11155) as link:
        builder = None
        builder, serialized = serializer(builder)
        builder.Finish(serialized)
        buf = builder.Output()
        link.sendall(struct.pack('>Q', len(buf))+buf)

        # Retrieve result
        buf = link.recv(8)
        msg_len = struct.unpack('<Q', buf)
        buf = SEAScope.upload.read_response(link, msg_len[0])
        result = deserializer(buf)

    return True, 'Current datetime: {}'.format(result)


def check_complex_case() -> typing.Tuple[bool, str]:
    """Check that it is possible to get the list of granules displayed in
    SEAScope"""
    import time
    import struct
    import numpy
    import SEAScope.upload
    import SEAScope.lib.utils
    import SEAScope.cmds.list_visible_data
    import SEAScope.cmds.select_variable_by_label

    name = 'OTC 2025'
    collection_id, collection = SEAScope.lib.utils.create_collection(name)

    var_name = 'letters'
    field_name = 'dummy'
    variable = SEAScope.lib.utils.create_variable(collection, var_name,
                                                  [field_name, ], '', 1)
    variable['rendering']['lineThickness'] = 18
    variable['rendering']['colormap'] = 'jet'
    variable['rendering']['min'] = 0
    variable['rendering']['max'] = 13

    dt = datetime.datetime(2022, 9, 9, 12, 0, 0)

    start_dt = datetime.datetime(2022, 9, 9, 0, 0, 0)
    stop_dt = datetime.datetime(2022, 9, 10, 0, 0, 0)

    # O
    gcps = [{'lon': -14.179304523538159,
             'lat': 25.239302634266515,
             'i': 0,
             'j': 0},
            {'lon': -2.9989164312821006,
             'lat': 25.940693052587832,
             'i': 1,
             'j': 0},
            {'lon': 5.766862331817404,
             'lat': 19.910086807951796,
             'i': 2,
             'j': 0},
            {'lon': 8.704935224529619,
             'lat': 10.834664193594111,
             'i': 3,
             'j': 0},
            {'lon': 8.673792977008947,
             'lat': 2.436841808348357,
             'i': 4,
             'j': 0},
            {'lon': 4.853987485564513,
             'lat': -8.739756382691992,
             'i': 5,
             'j': 0},
            {'lon': -1.59499634043025,
             'lat': -14.914969684888247,
             'i': 6,
             'j': 0},
            {'lon': -12.082687457796244,
             'lat': -16.188449917900662,
             'i': 7,
             'j': 0},
            {'lon': -19.223273720866576,
             'lat': -13.386270895801843,
             'i': 8,
             'j': 0},
            {'lon': -25.116903936792596,
             'lat': -1.3623072700552539,
             'i': 9,
             'j': 0},
            {'lon': -24.894265383059565,
             'lat': 8.021972656588996,
             'i': 10,
             'j': 0},
            {'lon': -21.570485304614383,
             'lat': 17.885558973804777,
             'i': 11,
             'j': 0},
            {'lon': -14.42542782895863,
             'lat': 25.154743184794466,
             'i': 12,
             'j': 0}]

    granule_id, granule_o = SEAScope.lib.utils.create_granule(collection_id,
                                                              gcps,
                                                              start_dt,
                                                              stop_dt)
    values = numpy.arange(13)
    SEAScope.lib.utils.set_field(granule_o, field_name, values)

    # T
    gcps = [{'lon': 7.164629382722425,
             'lat': 26.478165761018012,
             'i': 0,
             'j': 0},
            {'lon': 35.97297052815094,
             'lat': 26.924392264778703,
             'i': 1,
             'j': 0},
            {'lon': 21.290237520326883,
             'lat': 27.520601184976407,
             'i': 2,
             'j': 0},
            {'lon': 20.790127654203964,
             'lat': -15.272454955857544,
             'i': 3,
             'j': 0}]

    granule_id, granule_t = SEAScope.lib.utils.create_granule(collection_id,
                                                              gcps,
                                                              start_dt,
                                                              stop_dt)
    values = numpy.arange(5)
    SEAScope.lib.utils.set_field(granule_t, field_name, values)

    # C
    gcps = [{'lon': 65.41761209665785,
             'lat': 17.50639468240986,
             'i': 0,
             'j': 0},
            {'lon': 59.623275755790885,
             'lat': 26.559491115918064,
             'i': 1,
             'j': 0},
            {'lon': 48.48731142734,
             'lat': 29.142265678855853,
             'i': 2,
             'j': 0},
            {'lon': 35.46570262377785,
             'lat': 20.57599780862948,
             'i': 3,
             'j': 0},
            {'lon': 31.977822127881232,
             'lat': 6.236424603764264,
             'i': 4,
             'j': 0},
            {'lon': 33.25877288029835,
             'lat': -8.28775410021441,
             'i': 5,
             'j': 0},
            {'lon': 44.29445978644969,
             'lat': -16.14145480131639,
             'i': 6,
             'j': 0},
            {'lon': 56.157648016210175,
             'lat': -15.76023633052859,
             'i': 7,
             'j': 0},
            {'lon': 61.05430283974611,
             'lat': -11.697146331037471,
             'i': 8,
             'j': 0}]

    granule_id, granule_c = SEAScope.lib.utils.create_granule(collection_id,
                                                              gcps,
                                                              start_dt,
                                                              stop_dt)
    values = numpy.arange(9)
    SEAScope.lib.utils.set_field(granule_c, field_name, values)

    select_serializer = SEAScope.cmds.select_variable_by_label.serialize
    serializer = SEAScope.cmds.list_visible_data.serialize
    deserializer = SEAScope.cmds.list_visible_data.deserialize

    with SEAScope.upload.connect('localhost', 11155) as link:
        SEAScope.upload.collection(link, collection)
        SEAScope.upload.granule(link, granule_o)
        SEAScope.upload.granule(link, granule_t)
        SEAScope.upload.granule(link, granule_c)
        SEAScope.upload.variable(link, variable)
        SEAScope.upload.current_datetime(link, dt)
        SEAScope.upload.location(link, 25, 0)

        # Select variable
        builder = None
        builder, serialized = select_serializer(builder,
                                                name,
                                                var_name,
                                                True, True)
        builder.Finish(serialized)
        buf = builder.Output()
        link.sendall(struct.pack('>Q', len(buf))+buf)

        # Wait for SEAScope to update its display
        time.sleep(3)

        # Request visible granules list
        builder = None
        builder, serialized = serializer(builder)
        builder.Finish(serialized)
        buf = builder.Output()
        link.sendall(struct.pack('>Q', len(buf))+buf)

        # Retrieve result
        buf = link.recv(8)
        msg_len = struct.unpack('<Q', buf)
        buf = SEAScope.upload.read_response(link, msg_len[0])
        result = deserializer(buf)

    return True, 'Visible granules: {}'.format(result.__str__())


def perform_test(test_name: str,
                 test_func: typing.Callable[[], typing.Tuple[bool, str]],
                 results: typing.Dict[str, typing.Tuple[bool, str]],
                 ) -> None:
    """Execute a test and save the output in the "results" dictionary.
    If the test function fails due to an exception, the exception trace is
    saved in the results."""

    print(f'Checking {test_name}...')
    try:
        results[test_name] = test_func()
    except:  # noqa
        results[test_name] = (False, traceback.format_exc())


def read_report() -> None:
    """"""
    import json

    with open('python-env-OTC2025_report.json', 'rt') as f:
        report = json.load(f)

    ok = True
    for test_name, test_result in report['tests'].items():
        if test_result[0] is False:
            print('Test "{}" failed'.format(test_name))
            print('Error logs:')
            print(test_result[1])
            print('='*80)
            ok = False

    if ok is True:
        print('Everything is working as expected')
    else:
        print('\n')
        print('/!\\ ' * 20)
        print('\nSome things are not working as expected, please send the '
              'following file to <support-otc2025@oceandatalab.com>:\n')
        print(os.path.abspath('python-env-OTC2025_report.json'))


def start_notebook() -> None:
    """"""
    import shutil
    from pkg_resources import resource_filename

    notebook_path = resource_filename('python_env_OTC',
                                      'python-env-OTC2025_report.ipynb')
    shutil.copy(notebook_path, 'python-env-OTC2025_report.ipynb')
    try:
        subprocess.call(['jupyter', 'notebook', '--port', '12543',  # nosec
                         'python-env-OTC2025_report.ipynb'],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.STDOUT)
    except:  # noqa  # nosec
        pass


def stop_notebook() -> None:
    """"""
    try:
        subprocess.call(['jupyter', 'notebook', 'stop', '12543'],  # nosec
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.STDOUT)
    except KeyboardInterrupt:
        pass
    except:  # noqa  # nosec
        pass


def check_all(cli_args: typing.Optional[typing.Sequence[str]] = None
              ) -> None:
    """Run all tests and display results in a Jupyter notebook"""

    results: typing.Dict[str, typing.Tuple[bool, str]] = {}

    perform_test('python_version', check_python_version, results)
    #perform_test('install_directory', check_install_directory, results)
    perform_test('numpy', check_numpy, results)
    perform_test('scipy', check_scipy, results)
    perform_test('matplotlib', check_matplotlib, results)
    perform_test('netCDF4', check_netCDF4, results)
    perform_test('jupyterlab', check_jupyterlab, results)
    perform_test('SEAScope', check_SEAScope, results)
    perform_test('idf-converter', check_idf_converter, results)

    perform_test('cartopy', check_cartopy, results)
    perform_test('xarray', check_xarray, results)
    perform_test('dask', check_dask, results)
    perform_test('fluxengine', check_fluxengine, results)

    perform_test('SEAScope connection', check_SEAScope_connection, results)
    perform_test('SEAScope upload', check_upload, results)
    perform_test('SEAScope download', check_download, results)
    perform_test('SEAScope complex case', check_complex_case, results)

    print('Almost done: Jupyter should open in your web browser in a few '
          'seconds with the results of the tests')
    ctx = get_context()

    report = {'tests': results, 'context': ctx}

    filename = 'python-env-OTC2025_report.json'
    with open(filename, 'wt', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    start_notebook()
