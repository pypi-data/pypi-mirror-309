#pragma once

#include "../Displayer.h"

BEG_TL_NAMESPACE

/**
 * TODO: uninitialized content
*/
template<class T>
class alignas( T ) Opt {
public:
    /**/     Opt          ( auto &&head, auto &&...tail );
    /**/     Opt          ( const Opt<T> &that );
    /**/     Opt          ( Opt<T> &&that );
    /**/     Opt          ();

    /**/    ~Opt          ();
    
    void     display      ( Displayer &ds ) const;

    Opt&     operator=    ( const Opt<T> &that );
    Opt&     operator=    ( Opt<T> &&that );
    Opt&     operator=    ( const T &that );
    Opt&     operator=    ( T &&that );

    explicit operator bool() const;
    const T *operator->   () const;
    const T &operator*    () const;

    void     clear        ();

private:
    const T& value        () const;
    T&       value        ();

    char     bytes        [ sizeof( T ) ];
    bool     ok;
};

END_TL_NAMESPACE

#include "Opt.tcc"
