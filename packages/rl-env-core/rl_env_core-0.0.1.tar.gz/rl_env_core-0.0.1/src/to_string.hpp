#ifndef VEC_TO_STRING_HPP_
#define VEC_TO_STRING_HPP_

#include <glm/vec3.hpp>
#include <glm/mat4x4.hpp>

#include <format>

std::string vec3_to_string(glm::dvec3 vec) {
    return std::format("Vec3({}, {}, {})", vec.x, vec.y, vec.z);
}

std::string vec4_to_string(glm::dvec4 vec) {
    return std::format("Vec4({}, {}, {}, {})", vec.x, vec.y, vec.z, vec.w);
}

std::string mat4x4_to_string(glm::dmat4x4 mat) {
    std::string res = "Mat4x4(\n";
    for (int i = 0; i < 4; ++i) {
        for (int j = 0; j < 4; ++j) {
            res += std::format("{}", mat[i][j]);

            if (j == 3) {
                res += ",\n";
            } else {
                res += ", ";
            }
        }
    }
    res += ")";
    return res;
}

#endif