#pragma once

#include "../type_info/has_ct_value.h"
#include "WithDefaultOperators.h"
#include <cstdint>

BEG_TL_NAMESPACE

///
template<int i>
struct CtInt : public WithDefaultOperators {
    static constexpr int  value                 = i;

    static void           for_each_template_arg ( auto &&f ) { f( CtInt<i>() ); }
    static auto           template_type_name    () { return "CtInt"; }
    static constexpr bool always_equal          ( int v ) { return v == i; }
    static auto           to_string             () { return std::to_string( value ); }
    static constexpr int  ct_value              () { return value; } // used in default_operators
    void                  display               ( auto &ds ) const { ds << value; }

    static auto           apply_ct              ( int v, auto &&func, auto &&...args ) {
        if constexpr ( i == 0 )
            return func( CtInt<i>(), FORWARD( args )... );
        else {
            if ( i == v )
                return func( CtInt<i>(), FORWARD( args )... );
            else
                return CtInt<i-1>::apply_ct( v, FORWARD( func ), FORWARD( args )... );
        }
    }

    constexpr operator    std::uint64_t         () const { return value; }
    constexpr operator    std::uint32_t         () const { return value; }
    constexpr operator    std::uint16_t         () const { return value; }
    constexpr operator    std::uint8_t          () const { return value; }
    constexpr operator    std::int64_t          () const { return value; }
    constexpr operator    std::int32_t          () const { return value; }
    constexpr operator    std::int16_t          () const { return value; }
    constexpr operator    std::int8_t           () const { return value; }
    constexpr operator    bool                  () const { return value; }
};

template<> struct CtValueWrapperFor<int> { template<int i> static constexpr auto wrapper_for() { return CtInt<i>(); } };
template<int i> constexpr bool has_ct_value( const CtInt<i> & ) { return true; }

template<int i,int j> constexpr bool always_equal( CtInt<i>, CtInt<j> ) { return i == j; }
template<int i>       constexpr bool always_equal( CtInt<i>, int v ) { return v == i; }
template<int i>       constexpr bool always_equal( int v, CtInt<i> ) { return v == i; }

END_TL_NAMESPACE
