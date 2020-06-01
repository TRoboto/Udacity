#include "processor.h"

#include "linux_parser.h"

// TODO: Return the aggregate CPU utilization
Processor::Processor() {
  iAll_ = LinuxParser::Jiffies();
  iIdle_ = LinuxParser::IdleJiffies();
}

// TODO: Return the aggregate CPU utilization
float Processor::Utilization() {
  float fAllOld = iAll_;
  float fIdleOld = iIdle_;
  iAll_ = LinuxParser::Jiffies();
  iIdle_ = LinuxParser::IdleJiffies();

  float rValue =
      (((iAll_ - fAllOld) - (iIdle_ - fIdleOld)) / (iAll_ - fAllOld));
  return (rValue > 0.0) ? rValue : 0.0;
}