#ifndef OBJECT_HPP_
#define OBJECT_HPP_

#include "BBox.hpp"
#include "Triangle.hpp"

#include <glm/vec3.hpp>
#include <glm/gtc/quaternion.hpp>
#include <glm/mat4x4.hpp>

#include <array>
#include <variant>
#include <memory>
#include <concepts>

class PlainObject {
    class Octree {
        struct Leaf {
            bool filled = false;
        };

        using Branch = std::array<Octree, 8>;

        std::variant<Leaf, std::unique_ptr<Branch>> node{Leaf{}};

        inline static const BBox bounding_box{{0, 0, 0}, 1};
        inline static const std::array children_bounding_boxes {
            BBox{{0  , 0  , 0  }, 0.5},
            BBox{{0  , 0  , 0.5}, 0.5},
            BBox{{0  , 0.5, 0  }, 0.5},
            BBox{{0  , 0.5, 0.5}, 0.5},
            BBox{{0.5, 0  , 0  }, 0.5},
            BBox{{0.5, 0  , 0.5}, 0.5},
            BBox{{0.5, 0.5, 0  }, 0.5},
            BBox{{0.5, 0.5, 0.5}, 0.5}
        };

        static glm::dvec3 in_child_coordinates(glm::dvec3 pos, int child_id) {
            return 2.0 * (pos - children_bounding_boxes[child_id].origin());
        }

        static BBox in_child_coordinates(BBox p, int child_id) {
            return {in_child_coordinates(p.origin(), child_id), 2.0 * p.size()};
        }

        static void generate_quad(std::vector<Triangle>& mesh, glm::dvec3 pos, double scale,
                glm::dvec3 a, glm::dvec3 b, glm::dvec3 c, glm::dvec3 d) {
            mesh.emplace_back(pos + scale * a, pos + scale * b, pos + scale * c);
            mesh.emplace_back(pos + scale * b, pos + scale * d, pos + scale * c);
        }
    public:
        Octree() = default;

        Octree(const Octree& other) {
            std::visit([this]<typename T>(const T& node) {
                if constexpr (std::same_as<T, Leaf>) {
                    this->node = node;
                } else {
                    this->node = std::make_unique<Branch>(*node);
                }
            }, other.node);
        }

        Octree& operator = (Octree& other) {
            std::visit([this]<typename T>(const T& node) {
                if constexpr (std::same_as<T, Leaf>) {
                    this->node = node;
                } else {
                    this->node = std::make_unique<Branch>(*node);
                }
            }, other.node);
            return *this;
        }

        bool is_filled(glm::dvec3 pos) const {
            return std::visit([pos]<typename T>(const T& node) {
                if constexpr (std::same_as<T, Leaf>) {
                    return node.filled;
                } else {
                    for (int i = 0; i < std::ssize(children_bounding_boxes); ++i) {
                        if (children_bounding_boxes[i].contains(pos)) {
                            return (*node)[i].is_filled(in_child_coordinates(pos, i));
                        }
                    }
                    return false;
                }
            }, node);
        }

        void fill(BBox p, bool filled, int max_depth) {
            if (bounding_box.is_disjoint(p)) {
                return;
            }

            if (max_depth <= 0 || bounding_box.is_subset(p)) {
                node = Leaf{filled};
                return;
            }

            auto branch = std::make_unique<Branch>();
            for (int i = 0; i < std::ssize(children_bounding_boxes); ++i) {
                (*branch)[i].fill(in_child_coordinates(p, i), filled, max_depth - 1);
            }
            node = std::move(branch);
        }

        std::string debug_tree_repr(std::string indent) const {
            return std::visit([indent]<typename T>(const T& node) -> std::string {
                if constexpr (std::same_as<T, Leaf>) {
                    return indent + (node.filled ? "filled\n" : "empty\n");
                } else {
                    std::string res = indent + "branch\n";
                    for (int i = 0; i < std::ssize(children_bounding_boxes); ++i) {
                        res += (*node)[i].debug_tree_repr(indent + "    ");
                    }
                    return res;
                }
            }, node);
        }

        void generate_mesh(std::vector<Triangle>& mesh, glm::dvec3 pos, double scale) const {
            std::visit([&]<typename T>(const T& node) {
                if constexpr (std::same_as<T, Leaf>) {
                    if (!node.filled) {
                        return;
                    }

                    generate_quad(mesh, pos, scale, glm::dvec3{0, 0, 0}, glm::dvec3{0, 0, 1}, glm::dvec3{0, 1, 0}, glm::dvec3{0, 1, 1});
                    generate_quad(mesh, pos, scale, glm::dvec3{1, 0, 0}, glm::dvec3{1, 1, 0}, glm::dvec3{1, 0, 1}, glm::dvec3{1, 1, 1});
                    generate_quad(mesh, pos, scale, glm::dvec3{0, 0, 0}, glm::dvec3{0, 0, 1}, glm::dvec3{1, 0, 0}, glm::dvec3{1, 0, 1});
                    generate_quad(mesh, pos, scale, glm::dvec3{0, 1, 0}, glm::dvec3{1, 1, 0}, glm::dvec3{0, 1, 1}, glm::dvec3{1, 1, 1});
                    generate_quad(mesh, pos, scale, glm::dvec3{0, 0, 0}, glm::dvec3{0, 1, 0}, glm::dvec3{1, 0, 0}, glm::dvec3{1, 1, 0});
                    generate_quad(mesh, pos, scale, glm::dvec3{0, 0, 1}, glm::dvec3{1, 0, 1}, glm::dvec3{0, 1, 1}, glm::dvec3{1, 1, 1});
                } else {
                    for (int i = 0; i < std::ssize(children_bounding_boxes); ++i) {
                        (*node)[i].generate_mesh(mesh, pos + scale * children_bounding_boxes[i].origin(), scale / 2);
                    }
                }
            }, node);
        }
    };
    Octree octree{};

    bool changed = false;

    double scale_ = 1.0;
    glm::dvec3 position_{};
    glm::dquat rotation_{};
    glm::dvec3 origin_{};
public:
    bool have_changed() const {
        return changed;
    }

    void clear_changed() {
        changed = false;
    }

    bool is_filled(glm::dvec3 pos) const {
        glm::dvec4 in_tree = glm::inverse(transform()) * glm::dvec4{pos, 1.0};
        return octree.is_filled(glm::vec3{in_tree.x, in_tree.y, in_tree.z});
    }

    void fill(BBox p, int max_depth = 10) {
        octree.fill(p, true, max_depth);
        changed = true;
    }

    void carve(BBox p, int max_depth = 10) {
        octree.fill(p, false, max_depth);
        changed = true;
    }

    std::string debug_tree_repr() const {
        return octree.debug_tree_repr("|");
    }

    std::vector<Triangle> generate_mesh() const {
        std::vector<Triangle> res;
        octree.generate_mesh(res, glm::dvec3{0, 0, 0}, 1.0);
        return res;
    }

    double scale() const {
        return scale_;
    }

    void set_scale(double scale) {
        scale_ = scale;
    }

    void scale_by(double scale) {
        scale_ *= scale;
    }

    glm::dvec3 position() const {
        return position_;
    }

    void set_position(glm::dvec3 position) {
        position_ = position;
    }

    void move(glm::dvec3 offset) {
        position_ += offset;
    }

    glm::dquat rotation() const {
        return rotation_;
    }

    void set_rotation(glm::dquat rotation) {
        rotation_ = rotation;
    }

    void rotate(glm::dquat rotation) {
        rotation_ *= rotation;
    }

    glm::dvec3 origin() const {
        return origin_;
    }

    void set_origin(glm::dvec3 origin) {
        origin_ = origin;
    }

    glm::dmat4x4 transform() const {
        return glm::translate(glm::identity<glm::dmat4x4>(), position_)
             * glm::mat4_cast(rotation_)
             * glm::scale(glm::identity<glm::dmat4x4>(), glm::dvec3{scale_, scale_, scale_})
             * glm::translate(glm::identity<glm::dmat4x4>(), -origin_);
    }
};

#endif