from urllib.parse import quote_plus
from pathlib import Path
from munch import Munch
import archspec.cpu
import subprocess
import platform
import numpy
import sys
import os

global_verbosity_level = 1
auto_rebuild = False
loader_cache = {}

activities = []
def push_activity_log( name ):
    activities.append( name )
    print( ' -> '.join( activities ), end = '\r' )
def pop_activity_log():
    s = ' -> '.join( activities )
    print( ' ' * len( s ), end = '\r' )
    activities.pop()


def set_auto_rebuild( value ):
    global auto_rebuild
    auto_rebuild = value

def normalized_dtype( dtype, raise_exception_if_not_found = True ):
    if dtype in [ "FP64", "double", numpy.float64, numpy.int32, numpy.int64 ]:
        return "FP64"
    if dtype in [ "FP128", numpy.float128 ]:
        return "FP128"
    if dtype in [ "FP32", "float", numpy.float32 ]:
        return "FP32"
    if raise_exception_if_not_found:
        raise RuntimeError( f"unknown dtype `{ dtype }`" )
    return None


def numpy_dtype_for( dtype ):
    if dtype in [ "FP128" ]:
        return numpy.float128
    if dtype in [ "FP64" ]:
        return numpy.float64
    if dtype in [ "FP32" ]:
        return numpy.float32
    return None


def type_score( dtype: str ):
    if dtype.startswith( "FP" ):
        return int( dtype[ 2: ] )
    raise RuntimeError( "TODO" )


def type_promote( dtypes ):
    if len( dtypes ) == 0:
        return None

    res = normalized_dtype( dtypes[ 0 ] )
    for dtype in map( normalized_dtype, dtypes[ 1: ] ):
        if type_score( dtype ) > type_score( res ):
            res = dtype

    return res


def get_build_dir( *kargs ):
    """
      find a directory to copy .cpp/.h and store .so/.dylib/... files
    """
    
    # try one in the sources (check the write access)
    res = Path( __file__ ).parent
    for karg in kargs:
        res = res / karg
    if os.access( res, os.W_OK ):
        return res 
    
    # else, try to create it
    try:
        os.makedirs( res )
        return res
    except OSError:
        pass

    # else, make something in the home 
    raise RuntimeError( "TODO: make a loc or tmp build dir" )

def module_for( name, base_dir = Path( __file__ ).parent, use_arch = False, **kwargs ):
    # sorted list of parameters
    plist = [ ( x, str( y ) ) for x, y in kwargs.items() ]
    plist.sort()

    # append 'os'
    plist.append( ( 'os', platform.system() ) )
    # if use_arch:
    #     plist.append( ( 'arch', archspec.cpu.generic_microarchitecture() ) )

    # other presentation for the parameters
    ilist = [ f"{ k }={ quote_plus( str( v ) ) }" for k, v in plist ]
    vlist = [ quote_plus( str( v ) ) for _, v in plist ]

    # names
    suffix = "_".join( vlist ).replace( "%", '_' )
    module_name = f'{ name }_bindings_for_{ suffix }'

    # in the cache
    if module_name in loader_cache:
        return loader_cache[ module_name ]

    # where to find/put the files
    build_dir = get_build_dir( 'variants', name, suffix )
    if build_dir not in sys.path:
        sys.path.insert( 0, str( build_dir ) )

    # if allowed, try to load directly the library
    module = None
    if not auto_rebuild:
        try:
            module = __import__( module_name )
        except ModuleNotFoundError:
            pass

    # else, build and load it
    if module is None:
        if global_verbosity_level:
            push_activity_log( f"compilation of { name } for { kwargs }" )

        # call scons
        ret_code = subprocess.call( [ 'scons', f"--sconstruct={ base_dir / ( name + '.SConstruct' ) }", '-s',
            f"module_name={ module_name }", 
            f"suffix={ suffix }"
        ] + ilist, cwd = str( build_dir ), shell = False )
        
        if ret_code:
            raise RuntimeError( f"Failed to compile the C++ { name } binding" )

        if global_verbosity_level:
            pop_activity_log()

        # import
        module = __import__( module_name )

    # change names
    res = Munch()
    for n, v in module.__dict__.items():
        if n.endswith( '_' + suffix ):
            n = n[ : -1 - len( suffix ) ]
        res[ n ] = v

    # store the module in the cache
    loader_cache[ module_name ] = res

    return res
