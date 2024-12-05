/// Klotski Engine by Dnomd343 @2024

// TODO: A stable Ranges or RangesUnion must be ordered and non-repeating.

// TODO: 说明range的u32是如何组合出来的

// Range是对 `space`, `1x2`, `2x1` 和 `1x1` 的抽象
// 对于这样子的一个序列，它可以和12种不同的head位置组合，去除一些无效情况，产生有效layout
// Ranges则是多个range的组合，它提供了spawn方法，用于从指定个数的1x1、1x2、2x1中找出所有可能的情况
// 它同时提供了derive方法，允许根据不同的head位置，派生出一批有效的layout
// 注意，在正常情况下，合法的Ranges是无重复且顺序排列的，但容器不保证这点以提供最佳性能。

// 更进一步的，对于多个各不相同的layout，如果将它们中head相同的组合起来，可以产生12组Ranges，也就是RangesUnion
// 为了方便head排序，3/7/11/15这四个无效head值将作为空Ranges被插入，存储在长度为16的Ranges数组中

#pragma once

#include <array>
#include <vector>
#include <cstdint>

#include "utils/utility.h"

namespace klotski::codec {
class CommonCode;
} // namespace klotski::codec

namespace klotski::cases {

class Ranges final : public std::vector<uint32_t> {
public:
    // ------------------------------------------------------------------------------------- //

    /// Append the ranges from another instance.
    Ranges& operator+=(const Ranges &ranges);

    /// Flip the ranges every two bits in low-high symmetry.
    KLSK_INLINE void reverse();

    /// Spawn klotski-ranges that match the specified block numbers.
    void spawn(int n, int n_2x1, int n_1x1);

    /// Derive the legal ranges from reversed ranges with specified head.
    void derive(int head, Ranges &output) const;

    /// Check whether the combination of head and reversed range is valid.
    static KLSK_INLINE int check(int head, uint32_t range);

    // ------------------------------------------------------------------------------------- //
};

class RangesUnion final : public std::array<Ranges, 16> {
public:
    // ------------------------------------------------------------------------------------- //

    /// Get the Ranges of specified head.
    Ranges& ranges(size_t head);

    /// Get the const Ranges of specified head.
    [[nodiscard]] const Ranges& ranges(size_t head) const;

    /// Export the RangesUnion as a CommonCode list.
    [[nodiscard]] std::vector<codec::CommonCode> codes() const;

    // ------------------------------------------------------------------------------------- //

    /// Get the number of ranges contained.
    [[nodiscard]] KLSK_INLINE size_t size() const;

    /// Append the ranges from another instance.
    RangesUnion& KLSK_INLINE operator+=(const RangesUnion &ranges_union);

    /// Obtain the CommonCode of the specified index.
    [[nodiscard]] KLSK_INLINE codec::CommonCode operator[](size_type n) const;

    // ------------------------------------------------------------------------------------- //

private:
    static constexpr auto Heads = std::to_array<uint64_t>({
        0x0, 0x1, 0x2, 0x4, 0x5, 0x6, 0x8, 0x9, 0xA, 0xC, 0xD, 0xE,
    });
};

} // namespace klotski::cases

#include "internal/ranges.inl"
#include "internal/ranges_union.inl"
