INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_QRT QRT)

FIND_PATH(
    QRT_INCLUDE_DIRS
    NAMES QRT/api.h
    HINTS $ENV{QRT_DIR}/include
        ${PC_QRT_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    QRT_LIBRARIES
    NAMES gnuradio-QRT
    HINTS $ENV{QRT_DIR}/lib
        ${PC_QRT_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(QRT DEFAULT_MSG QRT_LIBRARIES QRT_INCLUDE_DIRS)
MARK_AS_ADVANCED(QRT_LIBRARIES QRT_INCLUDE_DIRS)

