#include "linux_parser.h"

#include <dirent.h>
#include <unistd.h>

#include <string>
#include <vector>

using std::stof;
using std::string;
using std::to_string;
using std::vector;

// DONE: An example of how to read data from the filesystem
string LinuxParser::OperatingSystem() {
  string line;
  string key;
  string value;
  std::ifstream filestream(kOSPath);
  if (filestream.is_open()) {
    while (std::getline(filestream, line)) {
      std::replace(line.begin(), line.end(), ' ', '_');
      std::replace(line.begin(), line.end(), '=', ' ');
      std::replace(line.begin(), line.end(), '"', ' ');
      std::istringstream linestream(line);
      while (linestream >> key >> value) {
        if (key == "PRETTY_NAME") {
          std::replace(value.begin(), value.end(), '_', ' ');
          return value;
        }
      }
    }
  }
  return value;
}

// DONE: An example of how to read data from the filesystem
string LinuxParser::Kernel() {
  string os, kernel;
  string line;
  std::ifstream stream(kProcDirectory + kVersionFilename);
  if (stream.is_open()) {
    std::getline(stream, line);
    std::istringstream linestream(line);
    linestream >> os >> kernel;
  }
  return kernel;
}

// BONUS: Update this to use std::filesystem
vector<int> LinuxParser::Pids() {
  vector<int> pids;
  DIR* directory = opendir(kProcDirectory.c_str());
  struct dirent* file;
  while ((file = readdir(directory)) != nullptr) {
    // Is this a directory?
    if (file->d_type == DT_DIR) {
      // Is every character of the name a digit?
      string filename(file->d_name);
      if (std::all_of(filename.begin(), filename.end(), isdigit)) {
        int pid = stoi(filename);
        pids.push_back(pid);
      }
    }
  }
  closedir(directory);
  return pids;
}

// TODO: Read and return the system memory utilization
float LinuxParser::MemoryUtilization() {
  float memTotal, memFree;
  string line;
  string key, value;
  std::ifstream stream{kProcDirectory + kMeminfoFilename};
  if (stream.is_open()) {
    while (std::getline(stream, line)) {
      std::istringstream linestream(line);
      linestream >> key >> value;
      if (key == "MemTotal:") {
        memTotal = stof(value);
      } else if (key == "MemFree:") {
        memFree = stof(value);
        break;
      }
    }
  }
  return (memTotal - memFree) / memTotal;
}

// TODO: Read and return the system uptime
long LinuxParser::UpTime() {
  string line, value;
  std::ifstream stream{kProcDirectory + kUptimeFilename};
  if (stream.is_open()) {
    std::getline(stream, line);
    std::istringstream linestream(line);
    linestream >> value;
  }
  return std::stol(value);
}

// TODO: Read and return the number of jiffies for the system
long LinuxParser::Jiffies() {
  return LinuxParser::ActiveJiffies() + LinuxParser::IdleJiffies();
}

// TODO: Read and return the number of active jiffies for a PID
// REMOVE: [[maybe_unused]] once you define the function
long LinuxParser::ActiveJiffies(int pid) {
  string line;
  string sUtime, sSTime, SCUTime, sCSTime;
  long jiffies;
  std::ifstream stream{kProcDirectory + to_string(pid) + kStatFilename};
  if (stream.is_open()) {
    std::getline(stream, line);
    std::istringstream linestream{line};
    for (int i = 0; i < 14; i++) linestream >> sUtime;

    linestream >> sSTime >> SCUTime >> sCSTime;

    jiffies = std::stol(sUtime) + std::stol(sSTime) + std::stol(SCUTime) +
              std::stol(sCSTime);
  }
  return jiffies;
}

// TODO: Read and return the number of active jiffies for the system
long LinuxParser::ActiveJiffies() {
  vector<string> time = CpuUtilization();
  return (stol(time[CPUStates::kUser_]) + stol(time[CPUStates::kNice_]) +
          stol(time[CPUStates::kSystem_]) + stol(time[CPUStates::kIRQ_]) +
          stol(time[CPUStates::kSoftIRQ_]) + stol(time[CPUStates::kSteal_]) +
          stol(time[CPUStates::kGuest_]) + stol(time[CPUStates::kGuestNice_]));
}

// TODO: Read and return the number of idle jiffies for the system
long LinuxParser::IdleJiffies() {
  vector<string> time = CpuUtilization();
  return (stol(time[CPUStates::kIdle_]) + stol(time[CPUStates::kIOwait_]));
}

// TODO: Read and return CPU utilization
vector<string> LinuxParser::CpuUtilization() {
  std::vector<string> vals;
  string line;
  string value;
  std::ifstream filestream(kProcDirectory + kStatFilename);
  if (filestream.is_open()) {
    std::getline(filestream, line);
    std::istringstream linestream(line);
    while (linestream >> value) {
      if (value != "cpu") {
        vals.push_back(value);
      }
    }
  }
  return vals;
}

// TODO: Read and return the total number of processes
int LinuxParser::TotalProcesses() {
  string line;
  string key, value;
  long total;
  std::ifstream stream{kProcDirectory + kStatFilename};
  if (stream.is_open()) {
    while (std::getline(stream, line)) {
      std::istringstream linestream{line};
      linestream >> key >> value;
      if (key == "processes") {
        total = std::stol(value);
        break;
      }
    }
  }
  return total;
}

// TODO: Read and return the number of running processes
int LinuxParser::RunningProcesses() {
  string line;
  string key, value;
  int running;
  std::ifstream stream{kProcDirectory + kStatFilename};
  if (stream.is_open()) {
    while (std::getline(stream, line)) {
      std::istringstream linestream{line};
      linestream >> key >> value;
      if (key == "procs_running") {
        running = std::stoi(value);
        break;
      }
    }
  }
  return running;
}

// TODO: Read and return the command associated with a process
// REMOVE: [[maybe_unused]] once you define the function
string LinuxParser::Command(int pid) {
  string line;
  std::ifstream stream{kProcDirectory + to_string(pid) + kCmdlineFilename};
  if (stream.is_open()) {
    std::getline(stream, line);
  }
  return line;
}

// TODO: Read and return the memory used by a process
// REMOVE: [[maybe_unused]] once you define the function
string LinuxParser::Ram(int pid) {
  string line;
  string key, value;
  long memory;
  std::ifstream stream{kProcDirectory + to_string(pid) + kStatusFilename};
  if (stream.is_open()) {
    while (std::getline(stream, line)) {
      std::istringstream linestream{line};
      linestream >> key >> value;
      if (key == "VmSize:") {
        memory = stol(value) / 1024;  // convert from kb to mb
        break;
      }
    }
  }
  return to_string(memory);
}

// TODO: Read and return the user ID associated with a process
// REMOVE: [[maybe_unused]] once you define the function
string LinuxParser::Uid(int pid) {
  string line;
  string key, value;

  std::ifstream stream{kProcDirectory + to_string(pid) + kStatusFilename};
  if (stream.is_open()) {
    while (std::getline(stream, line)) {
      std::istringstream linestream{line};
      linestream >> key >> value;
      if (key == "Uid:") break;
    }
  }
  return value;
}

// TODO: Read and return the user associated with a process
// REMOVE: [[maybe_unused]] once you define the function
string LinuxParser::User(int pid) {
  string line;
  string name, pass, strUid;
  string pUid = Uid(pid);

  std::ifstream stream{kPasswordPath};
  if (stream.is_open()) {
    while (std::getline(stream, line)) {
      std::replace(line.begin(), line.end(), ':', ' ');
      std::istringstream linestream{line};
      linestream >> name >> pass >> strUid;
      if (strUid == pUid) break;
    }
  }
  return name;
}

// TODO: Read and return the uptime of a process
// REMOVE: [[maybe_unused]] once you define the function
long LinuxParser::UpTime(int pid) {
  string line;
  string value;
  long uptime;
  std::ifstream stream{kProcDirectory + to_string(pid) + kStatFilename};
  if (stream.is_open()) {
    std::getline(stream, line);
    std::istringstream linestream{line};
    for (int i = 0; i < 22; i++) linestream >> value;
  }
  uptime = std::stol(value);
  uptime /= sysconf(_SC_CLK_TCK);
  return uptime;
}