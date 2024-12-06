from pybind11.setup_helpers import Pybind11Extension, build_ext
import os

def build(setup_kwarges):
    ext_modules = [
        Pybind11Extension(
            "py_jwt_cpp.jwt_cpp",
            ["py_jwt_cpp/jwt_wrapper.cpp"],
            include_dirs=[
                os.path.join("jwt-cpp", "include"),
                "/usr/local/include",
                "/usr/include",
                "/opt/homebrew/include",
            ],
            library_dirs=[
                "/usr/local/lib",
                "/usr/lib",
                "/opt/homebrew/lib"
            ],
            libraries=["ssl", "crypto"],
        ),
    ]
    setup_kwarges.update({
        "name": "jwt_cpp",
        "ext_modules": ext_modules,
        "cmdclass": {"build_ext": build_ext}
    })
