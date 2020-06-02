#include "format.h"

#include <string>

using std::string;
using std::to_string;

// TODO: Complete this helper function
// INPUT: Long int measuring seconds
// OUTPUT: HH:MM:SS
// REMOVE: [[maybe_unused]] once you define the function
string Format::ElapsedTime(long seconds) {
  int h = seconds / (60 * 60);
  int m = (seconds / 60) % 60;
  int s = seconds % 60;

  string hh_str = h < 10 ? '0' + to_string(h) : to_string(h);
  string mm_str = m < 10 ? '0' + to_string(m) : to_string(m);
  string ss_str = s < 10 ? '0' + to_string(s) : to_string(s);

  return hh_str + ":" + mm_str + ":" + ss_str;
}