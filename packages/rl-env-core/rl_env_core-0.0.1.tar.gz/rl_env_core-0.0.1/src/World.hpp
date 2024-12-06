#ifndef WORLD_HPP_
#define WORLD_HPP_

#include "PlainObject.hpp"

#include <span>

class World {
    std::vector<PlainObject> objects_;
public:
    const std::vector<PlainObject>& objects() const {
        return objects_;
    }

    void add(PlainObject object) {
        objects_.push_back(std::move(object));
    }
};

#endif