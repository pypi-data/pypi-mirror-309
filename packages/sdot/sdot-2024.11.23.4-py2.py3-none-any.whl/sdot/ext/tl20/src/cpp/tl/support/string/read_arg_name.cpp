#include "read_arg_name.h"
#include "strip.h"

BEG_TL_NAMESPACE

StrView read_arg_name( StrView &arg_names ) {
    int nb_open_par = 0;
    for( std::size_t i = 0; i < arg_names.size(); ++i ) {
        // "..."
        if ( arg_names[ i ] == '"' ) {
            while ( true ) {
                if ( ++i == arg_names.size() ) {
                    --i;
                    break;
                }
                if ( arg_names[ i ] == '\\' && i + 1 < arg_names.size() ) {
                    // TODO: multi char escape sequence
                    ++i;
                    continue;
                }
                if ( arg_names[ i ] == '"' )
                    break;
            }
            continue;
        }

        if ( arg_names[ i ] == '(' || arg_names[ i ] == '[' || arg_names[ i ] == '{' ) {
            ++nb_open_par;
            continue;
        }

        if ( arg_names[ i ] == ')' || arg_names[ i ] == ']' || arg_names[ i ] == '}' ) {
            --nb_open_par;
            continue;
        }

        if ( arg_names[ i ] == ',' && nb_open_par == 0 ) {
            StrView res = arg_names.substr( 0, i );
            arg_names.remove_prefix( i + 1 );
            return strip( res );
        }
    }

    StrView res = strip( arg_names );
    arg_names = {};
    return res;
}

END_TL_NAMESPACE
