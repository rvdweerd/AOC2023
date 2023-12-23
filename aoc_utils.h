//
// Created by rvdw on 19-12-23.
//

#ifndef AOC23_AOC_UTILS_H
#define AOC23_AOC_UTILS_H

#endif //AOC23_AOC_UTILS_H

#pragma once
#include <vector>
#include <string>
#include <fstream>
#include <iostream>
#include <map>
#include <type_traits>
#include <set>
#include <algorithm>
#include <stdlib.h>

namespace aoc
{
    long long int powi(unsigned long long int base, unsigned long long int exp)
    {
        unsigned long long int res = 1;
        while (exp) {
            if (exp & 1)
                res *= base;
            exp >>= 1;
            base *= base;
        }
        return res;
    }
    enum directions {
        R = 0,
        D,
        L,
        U
    };
    using LLI = long long int;
    using ULL = unsigned long long;
    auto PosHash = [](int pos_0, int pos_1)->ULL { return (ULL(pos_0) << 32 | pos_1); };

    /*std::pair<int, int> i2coord(int index, size_t w, size_t h) {
        return { index % w, index / h };
    }
    int coord2i(std::pair<int, int> coord, size_t w, size_t h) {
        return w * coord.second + coord.first;
    }*/

    class units {
    public:
        units()
        {}
        units(int ore, int clay, int obs, int geo)
                :
                ORE(ore),
                CLA(clay),
                OBS(obs),
                GEO(geo)
        {}
    public:
        int ORE = 0;
        int CLA = 0;
        int OBS = 0;
        int GEO = 0;
        int operator/(const units& rhs) const
        {
            int m1 = ORE == 0 ? 999999999 : rhs.ORE / ORE;
            int m2 = CLA == 0 ? 999999999 : rhs.CLA / CLA;
            int m3 = OBS == 0 ? 999999999 : rhs.OBS / OBS;
            int m4 = GEO == 0 ? 999999999 : rhs.GEO / GEO;
            return std::min(std::min(m1,m2),std::min(m3,m4));
        }
        units& operator*=(int rhs)
        {
            ORE *= rhs;
            CLA *= rhs;
            OBS *= rhs;
            GEO *= rhs;
            return *this;
        }
        units operator*(int rhs) const
        {
            return units(*this) *= rhs;
        }
        units& operator-=(const units& rhs)
        {
            ORE -= rhs.ORE;
            CLA -= rhs.CLA;
            OBS -= rhs.OBS;
            GEO -= rhs.GEO;
            return *this;
        }
        units& operator+=(const units& rhs)
        {
            ORE += rhs.ORE;
            CLA += rhs.CLA;
            OBS += rhs.OBS;
            GEO += rhs.GEO;
            return *this;
        }
        units operator+(const units& rhs) const
        {
            return units(*this) += rhs;
        }
        units operator-(const units& rhs) const
        {
            return units(*this) -= rhs;
        }
    };

    template <typename T>
    class _Vec2 {
    public:
        _Vec2()
        {}
        _Vec2(T x, T y)
                :
                x(x),
                y(y)
        {}
        _Vec2(const _Vec2& vect)
                :
                _Vec2(vect.x, vect.y)
        {}
        _Vec2 operator-() const
        {
            return _Vec2(-x, -y);
        }
        _Vec2& operator=(const _Vec2& rhs)
        {
            x = rhs.x;
            y = rhs.y;
            return *this;
        }
        _Vec2& operator+=(const _Vec2& rhs)
        {
            x += rhs.x;
            y += rhs.y;
            return *this;
        }
        _Vec2& operator-=(const _Vec2& rhs)
        {
            x -= rhs.x;
            y -= rhs.y;
            return *this;
        }
        _Vec2 operator+(const _Vec2& rhs) const
        {
            return _Vec2(*this) += rhs;
        }
        _Vec2 operator-(const _Vec2& rhs) const
        {
            return _Vec2(*this) -= rhs;
        }
        bool operator==(const _Vec2& rhs) const
        {
            return x == rhs.x && y == rhs.y;
        }
        bool operator!=(const _Vec2& rhs) const
        {
            return !(*this == rhs);
        }
        _Vec2& operator/=(const T& rhs)
        {
            x /= rhs;
            y /= rhs;
            return *this;
        }
        _Vec2 operator/(const T& rhs) const
        {
            return _Vec2(*this) /= rhs;
        }
    public:
        T x;
        T y;
    };
    typedef _Vec2<int> Vei2;


    void LoadGridInput(std::string filepath, std::vector<std::vector<char>>& grid, std::map<int, char>& cellvalues, bool convertChar2Int)
    {
        int x = 0;
        int y = 0;
        int width = 0;
        std::ifstream in(filepath);
        while (!in.eof())
        {
            std::vector<char> lineinput;
            for (char ch = in.get(); ch != '\n' && !in.eof(); ch = in.get())
            {
                int entry = ch;
                if (convertChar2Int) {
                    entry -= '0';
                }
                lineinput.push_back(entry);
                cellvalues[x + y * width] = entry;
                x++;
                if (x > width) {
                    width = x;
                }
            }
            grid.push_back(lineinput);
            x = 0;
            y++;
        }
        return;
    }

    std::vector<std::string> parse_string(const std::string& str, char delim)
    {
        std::vector<std::string> parsed_text;
        size_t last = 0;
        size_t next = 0;
        while ((next = str.find(delim, last)) != std::string::npos)
        {
            parsed_text.push_back(str.substr(last, next - last));
            last = next + 1;
        }
        parsed_text.push_back(str.substr(last));
        return parsed_text;
    }

    std::string remove_substring(std::string original, const std::string& substring)
    {
        std::size_t ind = original.find(substring); // Find the starting position of substring in the string
        if (ind != std::string::npos) {
            original.erase(ind, substring.length()); // erase function takes two parameter, the starting index in the string from where you want to erase characters and total no of characters you want to erase.
            //std::cout << original << "\n";
        }
        return original;
    }


}