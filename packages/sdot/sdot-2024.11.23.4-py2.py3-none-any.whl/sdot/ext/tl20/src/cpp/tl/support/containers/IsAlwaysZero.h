#pragma once

#include "../tl_namespace.h"

BEG_TL_NAMESPACE

///
template<class T>
struct IsAlwaysZero {
    enum { value = false };
};

// ::ct_value
template<class T> requires ( requires { T::ct_value(); } && T::ct_value() == 0 )
struct IsAlwaysZero<T>  {
    enum { value = true };
};

END_TL_NAMESPACE
