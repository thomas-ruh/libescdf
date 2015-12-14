#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.
#

# Enhance help message (must be set before anything else)
m4_divert_text([HELP_END], [
More information on how to configure the build of Libescdf is available
in the doc/ subdirectory of the source tree, in particular in the
configuring-libescdf.md file.

Libescdf is part of a diverse software ecosystem. You can find more
information about it at https://esl.cecam.org/, the homepage of the
Electronic Structure Library Wiki.])

# Init Autoconf
AC_PREREQ([2.69])
AC_INIT([LibESCDF], [0.1], [https://github.com/ElectronicStructureLibrary/libescdf/issues], [libescdf])
AC_CONFIG_AUX_DIR([config/gnu])
AC_CONFIG_MACRO_DIR([config/m4])
AC_CONFIG_SRCDIR([src/escdf.h])

# Init Automake
AC_CANONICAL_TARGET
AM_INIT_AUTOMAKE([1.13 parallel-tests color-tests])
AM_CONFIG_HEADER([config.h])

# Generate timestamp
escdf_timestamp=`date '+%Y%m%dT%H%M%S%z'`
AC_SUBST(escdf_timestamp)

                    # ------------------------------------ #

#
# System utilities
#

# Check for common programs and features
AC_PROG_AWK
AC_PROG_GREP
AC_PROG_INSTALL
AC_PROG_LN_S
AC_PROG_MAKE_SET
AC_PROG_MKDIR_P
AC_PROG_SED

                    # ------------------------------------ #

#
# Default settings
#

# Note for developers: you may edit these parameters to tune the behaviour
# of the build system. Please do it with care.

# Optional features
escdf_debug_enable_def="no"

# MPI
escdf_mpi_enable_def="auto"

# HDF5 (serial and MPI cases are distinct)
escdf_hdf5_enable_def="yes"
escdf_hdf5_ser_incs_def=""
escdf_hdf5_ser_libs_def="-lhdf5"
escdf_hdf5_mpi_incs_def=""
escdf_hdf5_mpi_libs_def="-lhdf5_mpi -lhdf5"

# NETCDF
escdf_netcdf_enable_def="yes"
escdf_netcdf_incs_def=""
escdf_netcdf_libs_def="-lnetcdf"

                    # ------------------------------------ #

#
# Check consistency of defaults
#

# Default triggers for optional features must be yes or no, and not empty
for escdf_cfg_default in debug; do
  tmp_default=`eval echo \$\{escdf_${escdf_cfg_default}_enable_def\}`
  if test "${tmp_default}" != "no" -a \
          "${tmp_default}" != "yes"; then
    AC_MSG_ERROR([invalid default value: escdf_${escdf_cfg_default}_enable_def = ${tmp_default}])
  fi
done

# Default triggers for external dependencies must be yes, no, or auto
for escdf_cfg_default in hdf5 mpi netcdf; do
  tmp_default=`eval echo \$\{escdf_${escdf_cfg_default}_enable_def\}`
  if test "${tmp_default}" != "" -a \
          "${tmp_default}" != "auto" -a \
          "${tmp_default}" != "no" -a \
          "${tmp_default}" != "yes"; then
    AC_MSG_ERROR([invalid default value: escdf_${escdf_cfg_default}_enable_def = ${tmp_default}])
  fi
done

# Clean-up
unset tmp_default

                    # ------------------------------------ #

#
# Optional features
#

# Debugging
AC_ARG_ENABLE([debug],
  [AS_HELP_STRING([--enable-debug],
    [Enable verbose function output (default: ${escdf_debug_enable_def})])],
  [escdf_debug_enable="${enableval}"; escdf_debug_type="yon"],
  [escdf_debug_enable="${escdf_debug_enable_def}"; escdf_debug_type="def"])
AC_SUBST(enable_debug)

                    # ------------------------------------ #

#
# External dependencies
#

# HDF5 (mandatory)
AC_ARG_WITH([hdf5],
  [AS_HELP_STRING([--with-hdf5],
    [Install prefix of the HDF5 library (e.g. /usr/local). Since HDF5 is a mandatory dependency, --with-hdf5 without argument has no effect, while --without-hdf5 produces an error.])],
  [ if test "${withval}" = "no" -o "${withval}" = "yes"; then
      escdf_hdf5_enable="${withval}"
      escdf_hdf5_type="yon"
    else
      escdf_hdf5_enable="yes"
      escdf_hdf5_type="dir"
      escdf_hdf5_incs="-I${withval}/include"
      escdf_hdf5_libs="-L${withval}/lib"
    fi],
  [escdf_hdf5_enable="${escdf_hdf5_enable_def}"; escdf_hdf5_type="def";
    escdf_hdf5_incs=""; escdf_hdf5_libs=""])
AC_ARG_VAR([HDF5_INCLUDES],
  [Include flags for HDF5. Please note that this variable conflicts with the --with-hdf5 option.])
AC_ARG_VAR([HDF5_LIBS],
    [Library flags for HDF5. Please note that this variable conflicts with the --with-hdf5 option.])
AC_SUBST(with_hdf5)

# NETCDF (mandatory)
AC_ARG_WITH([netcdf],
  [AS_HELP_STRING([--with-netcdf],
    [Install prefix of the NETCDF library (e.g. /usr/local). NETCDF support will be enabled only if you use this option. You may use --with-netcdf without argument if NETCDF is installed as a system library, and --without-netcdf to disable NETCDF support completely.])],
  [ if test "${withval}" = "no" -o "${withval}" = "yes"; then
      escdf_netcdf_enable="${withval}"
      escdf_netcdf_type="yon"
      if test "${escdf_netcdf_enable}" = "yes"; then
        escdf_netcdf_incs="${escdf_netcdf_incs_def}"
        escdf_netcdf_libs="${escdf_netcdf_libs_def}"
      fi
    else
      escdf_netcdf_enable="yes"
      escdf_netcdf_type="dir"
      escdf_netcdf_incs="-I${withval}/include"
      escdf_netcdf_libs="-L${withval}/lib ${escdf_netcdf_libs_def}"
    fi],
  [escdf_netcdf_enable="${escdf_netcdf_enable_def}"; escdf_netcdf_type="def";
    escdf_netcdf_incs=""; escdf_netcdf_libs=""])
AC_ARG_VAR([NETCDF_INCLUDES],
  [Include flags for NETCDF. Please note that this variable conflicts with the --with-netcdf option.])
AC_ARG_VAR([NETCDF_LIBS],
    [Library flags for NETCDF. Please note that this variable conflicts with the --with-netcdf option.])
AC_SUBST(with_netcdf)

# MPI (optional)
AC_ARG_WITH([mpi],
  [AS_HELP_STRING([--with-mpi],
    [Install prefix of MPI (e.g. /usr/local). The default behaviour is to detect whether the specified compilers properly support MPI and to fall back to serial mode if not. You may use --with-mpi without argument to force MPI detection, in which case detection failures will result in errors, and --without-mpi to disable MPI support completely.])],
  [ if test "${withval}" = "no" -o "${withval}" = "yes"; then
      escdf_mpi_enable="${withval}"
      escdf_mpi_type="yon"
    else
      escdf_mpi_enable="yes"
      escdf_mpi_type="dir"
    fi],
  [escdf_mpi_enable="${escdf_mpi_enable_def}"; escdf_mpi_type="def"])
AC_ARG_VAR([MPICC], [MPI-aware C compiler (usually called 'mpicc'). Please note that this variable conflicts with the --with-mpi option.])
AC_ARG_VAR([MPIFC], [MPI-aware Fortran compiler (usually called 'mpif90'. Please note that this variable conflicts with the --with-mpi option.])
AC_SUBST(with_mpi)

                    # ------------------------------------ #

#
# Check option consistency
#

# All --enable-* options must be yes or no
for escdf_cfg_option in debug; do
  tmp_option=`eval echo \$\{enable_${escdf_cfg_option}\}`
  if test "${tmp_option}" != "" -a \
          "${tmp_option}" != "no" -a \
          "${tmp_option}" != "yes"; then
    AC_MSG_ERROR([--enable-${escdf_cfg_option} must be "yes" or "no"])
  fi
done
unset tmp_option

# HDF5 is mandatory
if test "${escdf_hdf5_enable}" = "no"; then
  AC_MSG_ERROR([Libescdf requires HDF5
                  Please see https://www.hdfgroup.org/HDF5/ for installation
                  instructions.])
fi
if test "${escdf_hdf5_enable}" = "auto"; then
  AC_MSG_NOTICE([setting HDF5 trigger to yes])
  escdf_hdf5_enable="yes"
fi

# NetCDF is mandatory
if test "${escdf_netcdf_enable}" = "no"; then
  AC_MSG_ERROR([Libescdf requires NETCDF
                  Please see http://www.unidata.ucar.edu/netcdf/ for
                  installation instructions.])
fi
if test "${escdf_netcdf_enable}" = "auto"; then
  AC_MSG_NOTICE([setting NETCDF trigger to yes])
  escdf_netcdf_enable="yes"
fi

# All *_INCLUDES and *_LIBS environment variables must be provided at once
tmp_hdf5_vars="${HDF5_INCLUDES}${HDF5_LIBS}"
if test -n "${tmp_hdf5_vars}" -a \
        \( -z "${HDF5_INCLUDES}" -o -z "${HDF5_LIBS}" \); then
  AC_MSG_ERROR([HDF5_INCLUDES and HDF5_LIBS must both be set])
fi
tmp_mpi_vars="${MPICC}${MPIFC}"
if test -n "${tmp_mpi_vars}" -a \
        \( -z "${MPICC}" -o -z "${MPIFC}" \); then
  AC_MSG_ERROR([MPICC and MPIFC must both be set])
fi
tmp_netcdf_vars="${NETCDF_INCLUDES}${NETCDF_LIBS}"
if test -n "${tmp_netcdf_vars}" -a \
        \( -z "${NETCDF_INCLUDES}" -o -z "${NETCDF_LIBS}" \); then
  AC_MSG_ERROR([NETCDF_INCLUDES and NETCDF_LIBS must both be set])
fi

# Environment variables conflict with --with-* options
if test -n "${tmp_hdf5_vars}" -a -n "${with_hdf5}"; then
  AC_MSG_ERROR([conflicting option settings
                  Please use HDF5_INCLUDES + HDF5_LIBS or --with-hdf5,
                  not both.])
fi
if test -n "${tmp_mpi_vars}" -a -n "${with_mpi}"; then
  AC_MSG_ERROR([conflicting option settings
                  Please use MPICC + MPIFC or --with-mpi,
                  not both.])
fi
if test -n "${tmp_netcdf_vars}" -a -n "${with_netcdf}"; then
  AC_MSG_ERROR([conflicting option settings
                  Please use NETCDF_INCLUDES + NETCDF_LIBS or --with-netcdf,
                  not both.])
fi

# When using environment variables, triggers must be set to yes
if test -n "${tmp_hdf5_vars}"; then
  escdf_hdf5_enable="yes"
  escdf_hdf5_type="env"
fi
if test -n "${tmp_mpi_vars}"; then
  escdf_mpi_enable="yes"
  escdf_mpi_type="env"
fi
if test -n "${tmp_netcdf_vars}"; then
  escdf_netcdf_enable="yes"
  escdf_netcdf_type="env"
fi

# Clean-up
unset tmp_hdf5_vars
unset tmp_mpi_vars
unset tmp_netcdf_vars

                    # ------------------------------------ #

#
# Substitute build-system variables
#

# Defaults
AC_SUBST(escdf_debug_enable_def)
AC_SUBST(escdf_hdf5_enable_def)
AC_SUBST(escdf_hdf5_ser_incs_def)
AC_SUBST(escdf_hdf5_ser_libs_def)
AC_SUBST(escdf_hdf5_mpi_incs_def)
AC_SUBST(escdf_hdf5_mpi_libs_def)
AC_SUBST(escdf_mpi_enable_def)
AC_SUBST(escdf_netcdf_enable_def)
AC_SUBST(escdf_netcdf_incs_def)
AC_SUBST(escdf_netcdf_libs_def)

# Triggers
AC_SUBST(escdf_debug_enable)
AC_SUBST(escdf_hdf5_enable)
AC_SUBST(escdf_mpi_enable)
AC_SUBST(escdf_netcdf_enable)

# Initialization types
AC_SUBST(escdf_debug_type)
AC_SUBST(escdf_hdf5_type)
AC_SUBST(escdf_mpi_type)
AC_SUBST(escdf_netcdf_type)

# Internal MPI parameters
AC_SUBST(escdf_mpi_cc_set)
AC_SUBST(escdf_mpi_cc_wrap)
AC_SUBST(escdf_mpi_fc_set)
AC_SUBST(escdf_mpi_fc_wrap)

# Build flags for external dependencies
AC_SUBST(escdf_hdf5_incs)
AC_SUBST(escdf_hdf5_libs)
AC_SUBST(escdf_netcdf_incs)
AC_SUBST(escdf_netcdf_libs)

                    # ------------------------------------ #

#
# Architecture setup
#

# Init MPI parameters, possibly setting and/or wrapping compilers
ESCDF_MPI_INIT

                    # ------------------------------------ #

#
# C language support
#

# Init C compiler and preprocessor
AC_PROG_CC
AC_PROG_CPP

# C compiler peculiarities (for Libtool)
AM_PROG_CC_C_O

# Required headers
AC_LANG_PUSH([C])
AC_CHECK_HEADERS([assert.h string.h])
AC_LANG_POP([C])

                    # ------------------------------------ #

#
# Fortran language support
#

# Init Fortran compiler
AC_PROG_FC

                    # ------------------------------------ #

#
# Libtool configuration
#

# Init Libtool (must be done once compilers are fully set)
LT_INIT
LT_PREREQ([2.4])
LTOBJEXT="lo"
AC_SUBST(LTOBJEXT)

                    # ------------------------------------ #

#
# Multicore architecture support
#

# Look for MPI
if test "${escdf_mpi_enable}" != "no"; then
  ESCDF_MPI_DETECT
  if test "${escdf_mpi_ok}" = "yes"; then
    AC_DEFINE([HAVE_MPI], 1, [Define to 1 to enable MPI support.])
    escdf_mpi_enable="yes"
  else
    if test "${escdf_mpi_enable}" = "auto"; then
      AC_MSG_NOTICE([disabling MPI support])
      escdf_mpi_enable="no"
    else
      AC_MSG_FAILURE([MPI support is broken - please check your configuration])
    fi
  fi
fi

# From now on, the MPI trigger must be yes or no
if test "${escdf_mpi_enable}" != "no" -a "${escdf_mpi_enable}" != "yes"; then
  AC_MSG_ERROR([unexpected MPI trigger value: '${escdf_mpi_enable}'])
fi

                    # ------------------------------------ #

#
# Adjust build parameters according to configure options
#

# Debugging support
if test "${escdf_debug_enable}" = "yes"; then
  AC_DEFINE([ESCDF_DEBUG], 1, [Define to 1 to enable internal debugging.])
fi

                    # ------------------------------------ #

#
# Look for external dependencies (the order strongly matters)
#

# Check for mathematical functions
AC_CHECK_LIB(m, sqrt, [], [
  AC_MSG_WARN([missing math library (sqrt not found)])])

# Set HDF5 includes
if test "${escdf_hdf5_type}" != "dir"; then
  if test -n "${HDF5_INCLUDES}"; then
    escdf_hdf5_incs="${HDF5_INCLUDES}"
  else
    if test "${escdf_mpi_enable}" = "yes"; then
      escdf_hdf5_incs="${escdf_hdf5_mpi_incs_def}"
    else
      escdf_hdf5_incs="${escdf_hdf5_ser_incs_def}"
    fi
  fi
fi

# Set HDF5 libraries (requires MPI to be fully set)
if test "${escdf_hdf5_type}" = "dir"; then
  if test "${escdf_mpi_enable}" = "yes"; then
    escdf_hdf5_libs="${escdf_hdf5_libs} ${escdf_hdf5_mpi_libs_def}"
  else
    escdf_hdf5_libs="${escdf_hdf5_libs} ${escdf_hdf5_ser_libs_def}"
  fi
else
  if test -n "${HDF5_LIBS}"; then
    escdf_hdf5_libs="${HDF5_LIBS}"
  else
    if test "${escdf_mpi_enable}" = "yes"; then
      escdf_hdf5_libs="${escdf_hdf5_mpi_libs_def}"
    else
      escdf_hdf5_libs="${escdf_hdf5_ser_libs_def}"
    fi
  fi
fi

# Look for HDF5
AC_MSG_CHECKING([how HDF5 parameters have been set])
AC_MSG_RESULT([${escdf_hdf5_type}])
AC_MSG_CHECKING([for HDF5 include flags])
AC_MSG_RESULT([${escdf_hdf5_incs}])
AC_MSG_CHECKING([for HDF5 library flags])
AC_MSG_RESULT([${escdf_hdf5_libs}])
ESCDF_HDF5_DETECT
if test "${escdf_hdf5_ok}" = "yes"; then
  CPPFLAGS="${CPPFLAGS} ${escdf_hdf5_incs}"
  LIBS="${escdf_hdf5_libs} ${LIBS}"
else
  AC_MSG_FAILURE([HDF5 is missing or incomplete])
fi

# Set NETCDF includes
if test "${escdf_netcdf_type}" != "dir"; then
  if test -n "${NETCDF_INCLUDES}"; then
    escdf_netcdf_incs="${NETCDF_INCLUDES}"
  else
    escdf_netcdf_incs="${escdf_netcdf_incs_def}"
  fi
fi

# Set NETCDF libraries
if test "${escdf_netcdf_type}" != "dir"; then
  if test -n "${NETCDF_LIBS}"; then
    escdf_netcdf_libs="${NETCDF_LIBS}"
  else
    escdf_netcdf_libs="${escdf_netcdf_libs_def}"
  fi
fi

# Look for NETCDF
AC_MSG_CHECKING([how NETCDF parameters have been set])
AC_MSG_RESULT([${escdf_netcdf_type}])
AC_MSG_CHECKING([for NETCDF include flags])
AC_MSG_RESULT([${escdf_netcdf_incs}])
AC_MSG_CHECKING([for NETCDF library flags])
AC_MSG_RESULT([${escdf_netcdf_libs}])
ESCDF_NETCDF_DETECT
if test "${escdf_netcdf_ok}" = "yes"; then
  CPPFLAGS="${CPPFLAGS} ${escdf_netcdf_incs}"
  LIBS="${escdf_netcdf_libs} ${LIBS}"
else
  AC_MSG_FAILURE([NETCDF is missing or incomplete])
fi

                    # ------------------------------------ #

# Write down YAML configuration
AC_OUTPUT([config/data/libescdf-config.yml])

# Inform Automake
AM_CONDITIONAL([DO_BUILD_MPI], [test "${escdf_mpi_enable}" = "yes"])

# Report configuration
AC_MSG_NOTICE([])
AC_MSG_NOTICE([Final build parameters])
AC_MSG_NOTICE([----------------------])
AC_MSG_NOTICE([])
AC_MSG_NOTICE([TSTAMP   = ${escdf_timestamp}])
AC_MSG_NOTICE([])
AC_MSG_NOTICE([DEBUG    = ${escdf_debug_enable} (init: ${escdf_debug_type})])
AC_MSG_NOTICE([])
AC_MSG_NOTICE([MPI      = ${escdf_mpi_enable} (init: ${escdf_mpi_type})])
AC_MSG_NOTICE([HDF5     = ${escdf_hdf5_enable} (init: ${escdf_hdf5_type})])
AC_MSG_NOTICE([NETCDF   = ${escdf_netcdf_enable} (init: ${escdf_netcdf_type})])
AC_MSG_NOTICE([])
AC_MSG_NOTICE([CPP      = ${CPP}])
AC_MSG_NOTICE([CPPFLAGS = ${CPPFLAGS}])
AC_MSG_NOTICE([CC       = ${CC}])
AC_MSG_NOTICE([MPICC    = ${MPICC}])
AC_MSG_NOTICE([CFLAGS   = ${CFLAGS}])
AC_MSG_NOTICE([FC       = ${FC}])
AC_MSG_NOTICE([MPIFC    = ${MPIFC}])
AC_MSG_NOTICE([FCFLAGS  = ${FCFLAGS}])
AC_MSG_NOTICE([LDFLAGS  = ${LDFLAGS}])
AC_MSG_NOTICE([LIBS     = ${LIBS}])
AC_MSG_NOTICE([])

# Output configuration
AC_CONFIG_FILES([
  Makefile
  doc/Makefile
  src/Makefile
  config/data/libescdf.pc])
AC_OUTPUT