from urllib.parse import unquote_plus
from munch import Munch
import subprocess
import sysconfig
import pybind11
import sys
import os

# helper to get n-th parent directory
def pdir( dir, n = 1 ):
    if n == 0:
        return dir
    return pdir( os.path.dirname( dir ), n - 1 )

def args_to_obj( ARGLIST ):
    args = Munch()
    for k, v in ARGLIST:
        if k in [ 'module_name', 'suffix' ]:
            args[ k ] = v
        else:
            args[ k ] = unquote_plus( v )
    return args

def download_and_unzip( link, src, dst ):
    p = pdir( os.getcwd(), n = 7 ) + "/ext"
    import dload
 
    print( "Download ", link )

    dload.save_unzip( link, p, delete_after = True )
    os.rename( p + "/" + src, p + "/" + dst )

# def git_clone( link ):
#     from git import Repo  # pip install gitpython

#     Repo.clone_from( ,  )

def construct( Environment, VariantDir, Configure, ARGLIST, name, used_arg_names, files ):
    # build directory
    cwd = os.getcwd()
    bad = pdir( cwd, 3 )

    VariantDir( 'build', bad )

    # common args
    args = {}
    for k, v in ARGLIST:
        if k in [ 'module_name', 'suffix' ]:
            args[ k ] = v
        else:
            args[ k ] = unquote_plus( v )

    module_name = args[ 'module_name' ]
    suffix = args[ 'suffix' ]

    # scalar_type = args[ 'scalar_type' ]
    # nb_dims = args[ 'nb_dims' ]
    # arch = args[ 'arch' ]

    # includes
    CPPPATH = [
        # src
        os.path.join( bad, 'src', 'cpp' ),

        # ext
        os.path.join( bad, 'ext', 'tl20', 'src', 'cpp' ),
        os.path.join( bad, 'ext', 'asimd', 'src' ),
        os.path.join( bad, 'ext', 'boost' ),
        os.path.join( bad, 'ext', 'eigen' ),

        # systelm
        sysconfig.get_paths()[ 'include' ], # Python.h
        pybind11.get_include(), # pybind11.h
    ]


    # CXXFLAGS
    CXXFLAGS = [
        f'-DSDOT_CONFIG_module_name={ module_name }',
        f'-DSDOT_CONFIG_suffix={ suffix }',

        '-Wdeprecated-declarations',
        '-std=c++20',
        '-fopenmp',

        '-fdiagnostics-color=always',
        
        '-ffast-math',
        '-O3',

        '-g3',
    ]

    if 'arch' in used_arg_names:
       CXXFLAGS.append( '-march=' + args[ 'arch' ].replace( '_', '-' ) )

    for name in used_arg_names:
        CXXFLAGS.append( f'"-DSDOT_CONFIG_{ name }={ args[ name ] }"' )

    # LIBS
    LIBS = [
        # 'Catch2Main',
        # 'Catch2',
        # 'gomp',
    ]

    # LIBPATH
    LIBPATH = [
        # '/home/hugo.leclerc/.vfs_build/ext/Catch2/install/lib',
        # '/home/leclerc/.vfs_build/ext/Catch2/install/lib'
    ]

    # .cpp files
    sources = files + [
        "build/ext/tl20/src/cpp/tl/support/display/DisplayItem_Pointer.cpp",
        "build/ext/tl20/src/cpp/tl/support/display/DisplayItem_Number.cpp",
        "build/ext/tl20/src/cpp/tl/support/display/DisplayItem_String.cpp",
        "build/ext/tl20/src/cpp/tl/support/display/DisplayItem_List.cpp",

        "build/ext/tl20/src/cpp/tl/support/display/DisplayParameters.cpp",
        "build/ext/tl20/src/cpp/tl/support/display/DisplayContext.cpp",
        "build/ext/tl20/src/cpp/tl/support/display/DisplayItem.cpp",

        "build/ext/tl20/src/cpp/tl/support/string/CompactReprWriter.cpp",
        "build/ext/tl20/src/cpp/tl/support/string/CompactReprReader.cpp",
        "build/ext/tl20/src/cpp/tl/support/string/read_arg_name.cpp",
        "build/ext/tl20/src/cpp/tl/support/string/va_string.cpp",
        
        "build/ext/tl20/src/cpp/tl/support/Displayer.cpp",

        'build/src/cpp/sdot/support/BigRational.cpp',
        "build/src/cpp/sdot/support/VtkOutput.cpp",
        "build/src/cpp/sdot/support/Mpi.cpp",

        'build/src/cpp/sdot/symbolic/instructions/Symbol.cpp',
        'build/src/cpp/sdot/symbolic/instructions/Value.cpp',
        'build/src/cpp/sdot/symbolic/instructions/Func.cpp',
        'build/src/cpp/sdot/symbolic/instructions/Inst.cpp',
        'build/src/cpp/sdot/symbolic/Expr.cpp',
    ]

    # Environment
    env = Environment( CPPPATH = CPPPATH, CXXFLAGS = CXXFLAGS, LIBS = LIBS, LIBPATH = LIBPATH, SHLIBPREFIX = '' )

    # check the libraries
    conf = Configure( env )
    if not conf.CheckCXXHeader( 'boost/multiprecision/cpp_int.hpp' ):
        download_and_unzip( "https://archives.boost.io/release/1.86.0/source/boost_1_86_0.zip", "boost_1_86_0", "boost" )
    if not conf.CheckCXXHeader( 'Eigen/Dense' ):
        download_and_unzip( "https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.zip", "eigen-3.4.0", "eigen" )
    if not conf.CheckCXXHeader( 'asimd/SimdVec.h' ):
        download_and_unzip( "https://github.com/hleclerc/asimd/archive/refs/tags/asimd-v0.0.1-alpha.zip", "asimd-asimd-v0.0.1-alpha", "asimd" )
    if not conf.CheckCXXHeader( 'tl/support/Displayer.h' ):
        download_and_unzip( "https://github.com/hleclerc/tl20/archive/refs/tags/v0.0.1.zip", "tl20-0.0.1", "tl20" )
    env = conf.Finish()

    # register the library
    env.SharedLibrary( module_name + env[ 'SHLIBSUFFIX' ], sources )
