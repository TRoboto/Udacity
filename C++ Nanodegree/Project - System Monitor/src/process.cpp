#include "process.h"

#include <unistd.h>

#include <cctype>
#include <sstream>
#include <string>
#include <vector>

#include "linux_parser.h"

using std::string;
using std::to_string;
using std::vector;

Process::Process(int pid) : pid_(pid) {}
// TODO: Return this process's ID
int Process::Pid() { return pid_; }

// TODO: Return this process's CPU utilization
// void Process::CpuInitialization(long iActive, long iAll) {

//   cpu_ = float((iActive - iActive_)) / (iAll - iAll_);

//   iAll_ = iAll;
//   iActive_ = iActive;
// }
void Process::CpuInitialization() {
  long total_time = LinuxParser::ActiveJiffies(Pid());
  float seconds = LinuxParser::UpTime() - UpTime();
  if (seconds != 0)
    cpu_ = total_time / sysconf(_SC_CLK_TCK) / seconds;
  else
    cpu_ = 0;
}

float Process::CpuUtilization() const { return cpu_; }

// TODO: Return the command that generated this process
string Process::Command() { return LinuxParser::Command(Pid()); }

// TODO: Return this process's memory utilization
string Process::Ram() { return LinuxParser::Ram(Pid()); }

// TODO: Return the user (name) that generated this process
string Process::User() { return LinuxParser::User(Pid()); }

// TODO: Return the age of this process (in seconds)
long int Process::UpTime() { return LinuxParser::UpTime(Pid()); }

// TODO: Overload the "less than" comparison operator for Process objects
// REMOVE: [[maybe_unused]] once you define the function
bool Process::operator<(Process const& a) const {
  return CpuUtilization() > a.CpuUtilization();
}