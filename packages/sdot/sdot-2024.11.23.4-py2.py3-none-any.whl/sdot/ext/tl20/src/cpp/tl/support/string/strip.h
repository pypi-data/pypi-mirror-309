#pragma once

#include "../common_types.h"

BEG_TL_NAMESPACE

inline StrView strip( StrView res ) {
    while ( res.size() && res.back() == ' ' )
        res.remove_suffix( 1 );
    while ( res.size() && res.front() == ' ' )
        res.remove_prefix( 1 );
    return res;
}

END_TL_NAMESPACE
