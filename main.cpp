#include <iostream>

#include <set>
#include <cctype>
#include <stack>
#include <queue>
#include <ranges>
#include <cassert>
//#include "aoc_utils.h"
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

namespace Day2 {
    class Solution {
    public:
        explicit Solution(std::string filename)
                :
                filename_(std::move(filename))
        {
        }
        void LoadData() {
            std::ifstream in(filename_);
            std::string str;
            while (std::getline(in, str)) {

                std::string delimiter1 = ",";
                std::string delimiter2 = "-";

                std::string token1 = str.substr(0, str.find(delimiter1));
                std::string token2 = str.substr(str.find(delimiter1) + 1);

                std::string token1a = token1.substr(0, token1.find(delimiter2));
                std::string token1b = token1.substr(token1.find(delimiter2) + 1);
                std::pair<int, int> range1 = {std::stoi(token1a), std::stoi(token1b)};

                std::string token2a = token2.substr(0, token2.find(delimiter2));
                std::string token2b = token2.substr(token2.find(delimiter2) + 1);
                std::pair<int, int> range2 = {std::stoi(token2a), std::stoi(token2b)};

            }
        }

        void Solve() {
            LoadData();

            std::cin.get();
        }
    private:
        std::string filename_;
    };
}

int main() {
    Day1::Solution("/home/rvdw/AOC23/day1_input.txt").Solve();
    //Day2::Solution("/home/rvdw/AOC23/day2_input.txt").Solve();
    return 0;
}
