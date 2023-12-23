#include <iostream>
#include <map>
#include <set>
#include <cctype>
#include <stack>
#include <queue>
#include <ranges>
#include <cassert>
#include "aoc_utils.h"
#include <cstdlib>
#include <utility>
#include <fstream>
#include <regex>
#include <string>

namespace Day1 {
    class Solution {
    public:
        explicit Solution(std::string filename)
                :
                filename_(std::move(filename))
        {
        }
        void LoadData() {
            std::ifstream in(filename_);
            std::vector<int> input;
            while (!in.eof())
            {
                std::string str;
                //for (char ch = in.get(); ch != '\n' && !in.eof(); ch = in.get())
                for (char ch = in.get(); !in.eof(); ch = in.get())
                {
                        str += ch;
                }
                std::cout << str;
            }
        }

        static std::vector<size_t> find_positions(std::string str, std::string sub) {
            std::vector<size_t> positions; // holds all the positions that sub occurs within str

            size_t pos = str.find(sub, 0);
            while(pos != std::string::npos)
            {
                positions.push_back(pos);
                pos = str.find(sub,pos+1);
            }
            return positions;
        }
        void process_string( std::string &str ) {
            for (size_t i = 0; i < 10; ++i) {
                auto positions = find_positions(str, digits_svec[i]);
                auto dig_len = digits_svec[i].size();
                for (auto pos: positions) {
                    if (pos <= most_left_digit.first) {
                        most_left_digit = {pos, i};
                    }
                    if (pos + dig_len >= most_right_digit.first) {
                        //if (pos >= most_left_digit.first + digits_svec[most_left_digit.second].size() ||
                        //    pos == most_left_digit.first)
                        {
                            most_right_digit = {pos + dig_len - 1, i};
                        }
                    }
                }
            }
        }
        void LoadData2() {
            std::ifstream in(filename_);
            std::string str;

            int count = 0;
            while (std::getline(in, str)) {
                most_left_digit = {9999999, 10};
                most_right_digit = {0, 10};
                process_string(str);

                std::string d_left;
                std::string d_right;
                auto line_len = str.size();
                for (auto i = 0; i < line_len; ++i) {
                    // Check most left digit
                    if (d_left.empty()) {
                        if (isdigit(str[i])) {
                            d_left = str[i];
                        }
                        else
                        {
                            if (most_left_digit.second != 10 && most_left_digit.first == i) {
                                d_left = digits_nvec[most_left_digit.second];
                            }
                        }
                    }
                    if (d_right.empty()) {
                        if (isdigit(str[line_len - i - 1])) {
                            d_right = str[line_len - i - 1];
                        }
                        else {
                            if (most_right_digit.second != 10 && most_right_digit.first == line_len - i - 1) {
                                d_right = digits_nvec[most_right_digit.second];
                            }
                        }
                    }
                    if (!d_left.empty() && !d_right.empty()){
                        break;
                    }
                }
                count += std::stoi(d_left + d_right);
                std::cout << str << " ----> " << d_left + d_right << '\n';
            }
            std::cout << "\nCount: " << count;
        }
        void Solve() {
            LoadData2();

            std::cin.get();
        }
    private:
        std::string filename_;
        std::vector<int> cal_carried_;
        const std::vector<std::string> digits_svec = {"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"};
        const std::vector<std::string> digits_nvec = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"};
        std::pair<size_t, size_t> most_left_digit = {9999999, 10};
        std::pair<size_t, size_t> most_right_digit = {0, 10};

    };
}

namespace Day3 {

    uint64_t yx2Hash(int32_t y, int32_t x) {
        assert(y>=0 && x>=0);
        return (uint64_t(y)<<32 | x);
    }
    std::pair<int32_t, int32_t> Hash2yx(uint64_t hash) {
        return {int32_t(hash >> 32), int32_t((hash << 32) >> 32)};
    }
    struct Coord {
            Coord(int32_t y, int32_t x)
                :
                y(y), x(x), hash(yx2Hash(y,x))
            {
            }
            int32_t y;
            int32_t x;
            uint64_t hash;
    };
    struct Digs {
        long long int val;
        std::vector<Coord> coor;
        int ID;
    };
    struct Symb {
        char ch;
        Coord coor;
    };

class Solution {
    public:
        explicit Solution(std::string filename)
                :
                filename_(std::move(filename))
        {
        }
        void CreateProximitySet() {
            for (const Symb& symb : symbols) {
                for (int32_t dy = -1; dy <= 1; ++dy) {
                    for (int32_t dx = -1; dx <= 1; ++dx) {
                        int32_t newx = symb.coor.x + dx;
                        int32_t newy = symb.coor.y + dy;
                        if (newx >= 0 && newy >= 0 ) {
                            proximity_coords.emplace(yx2Hash(newy,newx));
                        }
                    }
                }

            }
        }
        void AddDigitToMap(const Digs& d) {
            for (auto c : d.coor){
                hash2id[c.hash] = d.ID;
            }
        }
        void LoadData() {
            std::ifstream in(filename_);
            std::string str;
            int32_t y = 0;
            int digit_count = 0;
            while (std::getline(in, str)) {
                field.push_back(str);
                int32_t x = 0;
                std::string digit_str;
                std::vector<Coord> digit_coords;
                bool digit_active = false;
                for (char c: str) {
                    if (isdigit(c)) {
                        digit_active = true;
                        digit_str += c;
                        digit_coords.emplace_back(y, x);
                    } else {
                        if (digit_active) {
                            digit_active = false;
                            digits.push_back({std::stoi(digit_str), digit_coords, digit_count});
                            id2value[digit_count] = std::stoi(digit_str);
                            digit_count++;
                            AddDigitToMap(digits.back());
                            digit_str.clear();
                            digit_coords.clear();
                        }
                        if (c != '.') {
                            symbols.push_back({c, {y, x}});
                        }
                    }
                    x++;
                    //std::cout << c;
                }
                if (digit_active) {
                    digit_active = false;
                    digits.push_back({std::stoi(digit_str), digit_coords, digit_count});
                    id2value[digit_count] = std::stoi(digit_str);
                    digit_count++;
                    AddDigitToMap(digits.back());
                    digit_str.clear();
                    digit_coords.clear();
                }
                y++;
                //std::cout << std::endl;
            }
            field_width = field[0].size();
            field_height = field.size();
            CreateProximitySet();
        }
        [[nodiscard]] bool IsAdjacentToSymbol(const Digs& digit) const {
            for (const Coord& h : digit.coor) {
                if (proximity_coords.find(h.hash) != proximity_coords.end()) {
                    return true;
                }
            }
            return false;
        }
        void SolvePart1() {
            long long int count1 = 0;
            long long int count2 = 0;
            for (const Digs& digit : digits) {
                count1 += digit.val;
                if (IsAdjacentToSymbol(digit)) {
                    count2 += digit.val;
                }
                else {
                    //std::cout << digit.val << std::endl;
                }
            }
            std::cout << "  Full sum of values    : " << count1;
            std::cout << "\n  Sum of adjacent values: " << count2 << std::endl;
        }
        void SolvePart2() {
            long long int count = 0;
            for (const Symb& symb : symbols){
                std::set<int> val_ids;
                if (symb.ch == '*') {
                    for (int32_t dy = -1; dy <= 1; ++dy) {
                        for (int32_t dx = -1; dx <= 1; ++dx) {
                            int32_t newx = symb.coor.x + dx;
                            int32_t newy = symb.coor.y + dy;
                            if (newx >= 0 && newy >= 0) {
                                if (hash2id.find(yx2Hash(newy, newx)) != hash2id.end()){
                                    val_ids.emplace(hash2id[yx2Hash(newy, newx)]);
                                }
                            }
                        }
                    }
                }
                if (val_ids.size() == 2){
                    //std::cout<<"Value pair: ";
                    long long int prod = 1;
                    for (int id : val_ids){
                        //std::cout << id2value[id] << ", ";
                        prod *= id2value[id];
                    }
                    //std::cout << std::endl;
                    count += prod;
                }
            }
            std::cout << "  Sum of ratios         : " << count << std::endl;
        }
        void Solve() {
            LoadData();
            SolvePart1();
            SolvePart2();
            //std::cin.get();
        }
    private:
        size_t field_width;
        size_t field_height;
        std::string filename_;
        std::vector<std::string> field;
        std::vector<Digs> digits;
        std::vector<Symb> symbols;
        std::set<uint64_t> proximity_coords;
        std::map<int,long long int> id2value;
        std::map<uint64_t, int> hash2id;
    };
}

namespace Day16 {
    class BeamPath {
    public:
        BeamPath(int x, int y, char dir)
                :
                pos(x,y), dir(dir)
        {}
        [[nodiscard]] bool out_of_bounds(const std::vector<std::string>& field) const {
            return (pos.x > field[0].size() - 1 || pos.y > field.size() - 1);
        }
        void Run(const std::vector<std::string>& field,
                 std::stack<BeamPath*>& path_stack,
                 std::vector<std::vector<char>>& beam_map,
                 std::set<u_int32_t>& visited
                 ) {
            while (true) {
                if (out_of_bounds(field)) return;
                u_int32_t state_hash = (pos.x << 16) | (pos.y << 8) | dir;
                if (visited.find(state_hash) != visited.end()) return;
                visited.insert(state_hash);
                beam_map[pos.y][pos.x] = '*';
                char field_char = field[pos.y][pos.x];
                switch (dir) {
                    case 'r':
                        if (field_char == '.') {
                            pos.x++;
                        }
                        else if (field_char == '\\') {
                            pos.y++;
                            dir = 'd';
                        }
                        else if (field_char == '\/') {
                            pos.y--;
                            dir = 'u';
                        }
                        else if (field_char == '-') {
                            pos.x++;
                            if (pos.x > field[0].size() - 1) return;
                        }
                        else if (field_char == '|') {
                            path_stack.emplace(new BeamPath(pos.x, pos.y-1, 'u'));
                            path_stack.emplace(new BeamPath(pos.x, pos.y+1, 'd'));
                            return;
                        }
                        break;
                    case 'l':
                        if (field_char == '.') {
                            pos.x--;
                            if (pos.x < 0) return;
                        }
                        else if (field_char == '\\') {
                            pos.y--;
                            dir = 'u';
                        }
                        else if (field_char == '\/') {
                            pos.y++;
                            dir = 'd';
                        }
                        else if (field_char == '-') {
                            pos.x--;
                            if (pos.x < 0) return;
                        }
                        else if (field_char == '|') {
                            path_stack.emplace(new BeamPath(pos.x, pos.y-1, 'u'));
                            path_stack.emplace(new BeamPath(pos.x, pos.y+1, 'd'));
                            return;
                        }
                        break;
                    case 'u':
                        if (field_char == '.') {
                            pos.y--;
                            if (pos.y < 0) return;
                        }
                        else if (field_char == '\\') {
                            pos.x--;
                            dir = 'l';
                        }
                        else if (field_char == '\/') {
                            pos.x++;
                            dir = 'r';
                        }
                        else if (field_char == '-') {
                            path_stack.emplace(new BeamPath(pos.x-1, pos.y, 'l'));
                            path_stack.emplace(new BeamPath(pos.x+1, pos.y, 'r'));
                            return;
                        }
                        else if (field_char == '|') {
                            pos.y--;
                            if (pos.y < 0) return;
                        }
                        break;
                    case 'd':
                        if (field_char == '.') {
                            pos.y++;
                            if (pos.y > field.size() - 1) return;
                        }
                        else if (field_char == '\\') {
                            pos.x++;
                            dir = 'r';
                        }
                        else if (field_char == '\/') {
                            pos.x--;
                            dir = 'l';
                        }
                        else if (field_char == '-') {
                            path_stack.emplace(new BeamPath(pos.x-1, pos.y, 'l'));
                            path_stack.emplace(new BeamPath(pos.x+1, pos.y, 'r'));
                            return;
                        }
                        else if (field_char == '|') {
                            pos.y++;

                        }
                        break;
                }
            }
        }
        ~BeamPath() = default;
        aoc::Vei2 pos;
        char dir;
    };

    class Solution {
    public:
    public:
        explicit Solution(std::string filename)
                :
                filename_(std::move(filename))
        {}
        void DrawField() {
            for (auto y=0; y<height;y++){
                for (auto x=0; x<width;x++){
                    if (beam_map[y][x]=='*') {
                        std::cout<<'*';
                    }
                    else {
                        std::cout<<field[y][x];
                    }
                }
                std::cout<<std::endl;
            }
            std::cout<<std::endl;
        }
        void LoadData() {
            std::ifstream in(filename_);
            std::string str;
            while (std::getline(in, str)) {
                field.push_back(str);
            }
            height = field.size();
            width = field[0].size();
            beam_map = std::vector<std::vector<char>>(height, std::vector<char>(width, '.'));
            DrawField();
        }
        void Reset() {
            set.clear();
            while (!path_stack.empty()) path_stack.pop();
            beam_map = std::vector<std::vector<char>>(height, std::vector<char>(width, '.'));
        }
        int GetScore(int x, int y, char dir) {
            Reset();
            path_stack.emplace(new BeamPath{x,y,dir});
            while (!path_stack.empty()) {
                BeamPath* p = path_stack.top(); path_stack.pop();
                p->Run(field, path_stack, beam_map, set);
                delete p;
            }
            int count=0;
            for (const auto& line : beam_map){
                for (auto c:line){
                    if (c == '*') count++;
                }
            }
            return count;
        }
        void SolvePart1() {
            int count = GetScore(0,0,'r');
            std::cout<<"Count: "<<count<<std::endl;
        }
        void SolvePart2() {
            int max_score = 0;
            for (auto i=0;i<width;i++){
                int s1 = GetScore(i,0,'d');
                int s2 = GetScore( i, height-1,'u');
                max_score = std::max(max_score,std::max(s1,s2));
            }
            for (auto j=0;j<height;j++){
                int s1 = GetScore(0,j,'r');
                int s2 = GetScore( width-1, j,'l');
                max_score = std::max(max_score,std::max(s1,s2));
            }
            std::cout<<"Max count: "<<max_score;
        }
        void Solve() {
            LoadData();
            SolvePart1();
            SolvePart2();
        }
    public:
        std::string filename_;
        std::vector<std::string> field;
        std::vector<std::vector<char>> beam_map;
        size_t width;
        size_t height;
        std::stack<BeamPath*> path_stack;
        std::set<u_int32_t> set;
    };
}

int main() {
    //Day1::Solution("/home/rvdw/AOC23/day1_input.txt").Solve();
    Day16::Solution("/home/rvdw/AOC23/day16_input.txt").Solve();
    return 0;
}
