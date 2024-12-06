#ifndef TRIANGLE_HPP_
#define TRIANGLE_HPP_

#include "to_string.hpp"

#include <glm/vec3.hpp>

#include <format>

struct Triangle {
    glm::dvec3 a;
    glm::dvec3 b;
    glm::dvec3 c;

    friend bool operator == (Triangle, Triangle) = default;

    std::string to_string() const {
        return std::format("Triangle({}, {}, {})", vec3_to_string(a), vec3_to_string(b), vec3_to_string(c));
    }
};

#endif