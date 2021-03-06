# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.netlib_scalapack import ScalapackBase


class Amdscalapack(ScalapackBase):
    """
    ScaLAPACK is a library of high-performance linear algebra routines
    for parallel distributed memory machines. It depends on external
    libraries including BLAS and LAPACK for Linear Algebra computations.

    AMD's optimized version of ScaLAPACK enables using BLIS and
    LibFLAME library that have optimized dense matrix functions and
    solvers for AMD EPYC processor family CPUs.
    """

    _name = 'amdscalapack'
    homepage = "https://developer.amd.com/amd-aocl/scalapack/"
    url = "https://github.com/amd/scalapack/archive/2.2.tar.gz"
    git = "https://github.com/amd/scalapack.git"

    maintainers = ['amd-toolchain-support']

    version('2.2', sha256='2d64926864fc6d12157b86e3f88eb1a5205e7fc157bf67e7577d0f18b9a7484c')

    variant(
        'build_type',
        default='Release',
        description='CMake build type',
        values=('Release', 'RelWithDebInfo'))

    def cmake_args(self):
        """ cmake_args function"""
        args = super(Amdscalapack, self).cmake_args()
        spec = self.spec

        args.extend([
            "-DUSE_DOTC_WRAPPER:BOOL=%s" % (
                'ON' if '%aocc ^amdblis' in spec else 'OFF'
            )
        ])

        args.extend([
            '-DUSE_F2C=ON',
            '-DLAPACK_FOUND=true',
            '-DCMAKE_C_COMPILER=%s' % spec['mpi'].mpicc,
            '-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc,
        ])

        return args
