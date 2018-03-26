#!/usr/bin/env python

from distutils.command.build_ext import build_ext as build_ext_orig
import os
import pathlib
from setuptools import setup, Extension


class CMakeExtension(Extension):
    def __init__(self, name):
        # don't invoke the original build_ext for this special extension
        super().__init__(name, sources=[])


class build_ext(build_ext_orig):
    def run(self):
        for ext in self.extensions:
            self.build_cmake(ext)
        # super().run() # Avoid vtkgdcmPython.cpython-36m-x86_64-linux-gnu.so

    def build_cmake(self, ext):
        cwd = pathlib.Path().absolute()

        # these dirs will be created in build_py, so if you don't have
        # any python sources to bundle, the dirs will be missing
        build_temp = pathlib.Path(self.build_temp)
        build_temp.mkdir(parents=True, exist_ok=True)
        extdir = pathlib.Path(self.get_ext_fullpath(ext.name))
        extdir = extdir.parent
        extdir.mkdir(parents=True, exist_ok=True)

        # example of cmake args
        config = 'Debug' if self.debug else 'Release'
        cmake_args = [
            '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + str(extdir.absolute()),
            '-DLIBRARY_OUTPUT_PATH=' + str(extdir.absolute()),
            '-DCMAKE_BUILD_TYPE=' + config,
            '-DGDCM_BUILD_SHARED_LIBS:BOOL=ON',
            '-DGDCM_DOCUMENTATION:BOOL=OFF',
            '-DGDCM_BUILD_DOCBOOK_MANPAGES:BOOL=OFF',
            '-DGDCM_USE_VTK:BOOL=ON',
            '-DGDCM_WRAP_PYTHON:BOOL=ON',
        ]

        # example of build args
        build_args = [
            '--config', config,
            '--target', ext.name,
            '--', '-j4',
        ]

        os.chdir(str(build_temp))
        self.spawn(['cmake', os.path.join(str(cwd), 'GDCM')] + cmake_args)
        if not self.dry_run:
            self.spawn(['cmake', '--build', '.'] + build_args)
        os.chdir(str(cwd))


setup(name='vtkgdcm',
      version='2.8.6-dev6',
      author='Jose Luis Cercos-Pita',
      author_email='jlcercos@gmail.com',
      url='https://github.com/sanguinariojoe/gdcm-pypi',
      description='Grassroots DiCoM is a C++ library for DICOM medical files.',
      long_description='Grassroots DiCoM is a C++ library for DICOM medical ' \
                       'files. It is accessible from Python, C#, Java and ' \
                       'PHP. It supports RAW, JPEG, JPEG 2000, JPEG-LS, RLE ' \
                       'and deflated transfer syntax.' \
                       'It comes with a super fast scanner implementation to ' \
                       ' quickly scan hundreds of DICOM files. ' \
                       'It supports SCU network operations (C-ECHO, C-FIND, ' \
                       'C-STORE, C-MOVE). PS 3.3 & 3.6 are distributed as ' \
                       'XML files. It also provides PS 3.15 certificates and ' \
                       'password based mecanism to anonymize and de-identify ' \
                       'DICOM datasets.',
      download_url='https://sourceforge.net/projects/gdcm',
      license='BSD v2',
      classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Healthcare Industry',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: BSD License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
      ],
      keywords='tomography gdcm',
      packages=[],
      install_requires=[
          'vtk',
      ],
      ext_modules=[CMakeExtension('vtkgdcmPython')],
      cmdclass={
          'build_ext': build_ext,
      },
)
