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
  std::fstream stream{kProcDirectory + kMeminfoFilename};
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
  long upTime;
  string line, value;
  std::fstream stream{kProcDirectory + kUptimeFilename};
  if (stream.is_open()) {
    std::getline(stream, line);
    std::istringstream linestream{line};
    linestream >> value;
    upTime = std::stol(value);
  }
  return upTime;
}

// TODO: Read and return the number of jiffies for the system
long LinuxParser::Jiffies() {
  // we can use
  // return LinuxParser::ActiveJiffies() + LinuxParser::IdleJiffies();
  // but this is faster since we only read the file once.
  string line;
  string cpu;
  string sUser, sNice, sSystem, sIdle, sIOwait, sIRQ, sSoftIRQ, sSteal, sGuest,
      sGuestNice;
  long jiffies;
  std::fstream stream{kProcDirectory + kStatFilename};
  if (stream.is_open()) {
    std::getline(stream, line);
    std::istringstream linestream{line};
    linestream >> cpu >> sUser >> sNice >> sSystem >> sIdle >> sIOwait >>
        sIRQ >> sSoftIRQ >> sSteal >> sGuest >> sGuestNice;
    jiffies = std::stol(sUser) + std::stol(sNice) + std::stol(sSystem) +
              std::stol(sIdle) + std::stol(sIOwait) + std::stol(sIRQ) +
              std::stol(sSoftIRQ) + std::stol(sSteal) + std::stol(sGuest) +
              std::stol(sGuestNice);
  }
  return jiffies;
}

// TODO: Read and return the number of active jiffies for a PID
// REMOVE: [[maybe_unused]] once you define the function
long LinuxParser::ActiveJiffies(int pid) {
  string line;
  string sUtime, sSTime, SCUTime, sCSTime;
  long jiffies;
  std::fstream stream{kProcDirectory + to_string(pid) + kStatFilename};
  if (stream.is_open()) {
    std::getline(stream, line);
    std::istringstream linestream{line};
    for (int i = 0; i < 15; i++) {
      linestream >> sUtime;
    }
    linestream >> sSTime >> SCUTime >> sCSTime;

    jiffies = std::stol(sUtime) + std::stol(sSTime) + std::stol(SCUTime) +
              std::stol(sCSTime);
  }
  return jiffies;
}

// TODO: Read and return the number of active jiffies for the system
long LinuxParser::ActiveJiffies() {
  string line;
  string cpu;
  string sUser, sNice, sSystem, sIdle, sIOwait, sIRQ, sSoftIRQ, sSteal, sGuest,
      sGuestNice;
  long jiffies;
  std::fstream stream{kProcDirectory + kStatFilename};
  if (stream.is_open()) {
    std::getline(stream, line);
    std::istringstream linestream{line};
    linestream >> cpu >> sUser >> sNice >> sSystem >> sIdle >> sIOwait >>
        sIRQ >> sSoftIRQ >> sSteal >> sGuest >> sGuestNice;
    jiffies = std::stol(sUser) + std::stol(sNice) + std::stol(sSystem) +
              std::stol(sIRQ) + std::stol(sSoftIRQ) + std::stol(sSteal) +
              std::stol(sGuest) + std::stol(sGuestNice);
  }
  return jiffies;
}

// TODO: Read and return the number of idle jiffies for the system
long LinuxParser::IdleJiffies() {
  string line;
  string cpu;
  string sUser, sNice, sSystem, sIdle, sIOwait, sIRQ, sSoftIRQ, sSteal, sGuest,
      sGuestNice;
  long jiffies;
  std::fstream stream{kProcDirectory + kStatFilename};
  if (stream.is_open()) {
    std::getline(stream, line);
    std::istringstream linestream{line};
    linestream >> cpu >> sUser >> sNice >> sSystem >> sIdle >> sIOwait >>
        sIRQ >> sSoftIRQ >> sSteal >> sGuest >> sGuestNice;
    jiffies = std::stol(sIdle) + std::stol(sIOwait);
  }
  return jiffies;
}

// TODO: Read and return CPU utilization
vector<string> LinuxParser::CpuUtilization() {
  vector<string> vCpuUtilization;
  long lPrevIdle = IdleJiffies();
  long lPrevActive = ActiveJiffies();
  long lPrevTotal = lPrevActive + lPrevIdle;
  sleep(10);
  long lIdle = IdleJiffies();
  long lActive = ActiveJiffies();
  long lTotal = lIdle + lActive;

  long total = lTotal - lPrevTotal;
  long idle = lIdle - lPrevIdle;
  vCpuUtilization.push_back(to_string((total - idle) / total));
  return vCpuUtilization;
}

// TODO: Read and return the total number of processes
int LinuxParser::TotalProcesses() {
  string line;
  string key, value;
  long total;
  std::fstream stream{kProcDirectory + kStatFilename};
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
  long running;
  std::fstream stream{kProcDirectory + kStatFilename};
  if (stream.is_open()) {
    while (std::getline(stream, line)) {
      std::istringstream linestream{line};
      linestream >> key >> value;
      if (key == "procs_running") {
        running = std::stol(value);
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
  std::fstream stream{kProcDirectory + to_string(pid) + kCmdlineFilename};
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
  std::fstream stream{kProcDirectory + to_string(pid) + kStatFilename};
  if (stream.is_open()) {
    while (std::getline(stream, line)) {
      std::istringstream linestream{line};
      linestream >> key >> value;
      if (key == "VmSize:")
        memory = stof(value) * 0.001; // convert from kb to mb
        break;
    }
  }
  return to_string(memory);
}

// TODO: Read and return the user ID associated with a process
// REMOVE: [[maybe_unused]] once you define the function
string LinuxParser::Uid(int pid) { 
  string line;
  string key, value;
  
  std::fstream stream{kProcDirectory + to_string(pid) + kStatFilename};
  if (stream.is_open()) {
    while (std::getline(stream, line)) {
      std::istringstream linestream{line};
      linestream >> key >> value;
      if (key == "Uid:")
        break;
    }
  }
  return value; }

// TODO: Read and return the user associated with a process
// REMOVE: [[maybe_unused]] once you define the function
string LinuxParser::User(int pid) { return string(); }

// TODO: Read and return the uptime of a process
// REMOVE: [[maybe_unused]] once you define the function
long LinuxParser::UpTime(int pid) { return 0; }