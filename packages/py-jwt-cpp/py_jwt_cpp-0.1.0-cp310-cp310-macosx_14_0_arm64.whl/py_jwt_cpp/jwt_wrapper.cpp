#include <pybind11/pybind11.h>
#include <pybind11/stl.h>   // For Python-C++ STL conversions
#include <jwt-cpp/jwt.h>    // Include jwt-cpp
#include <string>

namespace py = pybind11;

std::string encode(const std::map<std::string, std::string>& claims, const std::string& private_key) {
    auto token = jwt::create();

    // Add claims from the input map to the JWT
    for (const auto& [claim, value] : claims) {
        token.set_payload_claim(claim, jwt::claim(value));
    }

    // Sign the JWT using RS256
    return token.sign(jwt::algorithm::rs256("", private_key, "", ""));
}

// pybind11 module
PYBIND11_MODULE(jwt_cpp, m) {
    m.def("cpp_encode", &encode, py::arg("payload"), py::arg("private_key"),
          "Encode a JWT with given payload and RS256 private key.");
}
