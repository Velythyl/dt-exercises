#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/code/solution/src/interaction_pkg"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/code/solution/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/code/solution/install/lib/python3/dist-packages:/code/solution/build/interaction_pkg/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/code/solution/build/interaction_pkg" \
    "/usr/bin/python3" \
    "/code/solution/src/interaction_pkg/setup.py" \
     \
    build --build-base "/code/solution/build/interaction_pkg" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/code/solution/install" --install-scripts="/code/solution/install/bin"
