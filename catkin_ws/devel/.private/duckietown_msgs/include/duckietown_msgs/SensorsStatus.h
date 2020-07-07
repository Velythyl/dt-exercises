// Generated by gencpp from file duckietown_msgs/SensorsStatus.msg
// DO NOT EDIT!


#ifndef DUCKIETOWN_MSGS_MESSAGE_SENSORSSTATUS_H
#define DUCKIETOWN_MSGS_MESSAGE_SENSORSSTATUS_H

#include <ros/service_traits.h>


#include <duckietown_msgs/SensorsStatusRequest.h>
#include <duckietown_msgs/SensorsStatusResponse.h>


namespace duckietown_msgs
{

struct SensorsStatus
{

typedef SensorsStatusRequest Request;
typedef SensorsStatusResponse Response;
Request request;
Response response;

typedef Request RequestType;
typedef Response ResponseType;

}; // struct SensorsStatus
} // namespace duckietown_msgs


namespace ros
{
namespace service_traits
{


template<>
struct MD5Sum< ::duckietown_msgs::SensorsStatus > {
  static const char* value()
  {
    return "d8dd1fcbd833d76004def4493c2acff3";
  }

  static const char* value(const ::duckietown_msgs::SensorsStatus&) { return value(); }
};

template<>
struct DataType< ::duckietown_msgs::SensorsStatus > {
  static const char* value()
  {
    return "duckietown_msgs/SensorsStatus";
  }

  static const char* value(const ::duckietown_msgs::SensorsStatus&) { return value(); }
};


// service_traits::MD5Sum< ::duckietown_msgs::SensorsStatusRequest> should match
// service_traits::MD5Sum< ::duckietown_msgs::SensorsStatus >
template<>
struct MD5Sum< ::duckietown_msgs::SensorsStatusRequest>
{
  static const char* value()
  {
    return MD5Sum< ::duckietown_msgs::SensorsStatus >::value();
  }
  static const char* value(const ::duckietown_msgs::SensorsStatusRequest&)
  {
    return value();
  }
};

// service_traits::DataType< ::duckietown_msgs::SensorsStatusRequest> should match
// service_traits::DataType< ::duckietown_msgs::SensorsStatus >
template<>
struct DataType< ::duckietown_msgs::SensorsStatusRequest>
{
  static const char* value()
  {
    return DataType< ::duckietown_msgs::SensorsStatus >::value();
  }
  static const char* value(const ::duckietown_msgs::SensorsStatusRequest&)
  {
    return value();
  }
};

// service_traits::MD5Sum< ::duckietown_msgs::SensorsStatusResponse> should match
// service_traits::MD5Sum< ::duckietown_msgs::SensorsStatus >
template<>
struct MD5Sum< ::duckietown_msgs::SensorsStatusResponse>
{
  static const char* value()
  {
    return MD5Sum< ::duckietown_msgs::SensorsStatus >::value();
  }
  static const char* value(const ::duckietown_msgs::SensorsStatusResponse&)
  {
    return value();
  }
};

// service_traits::DataType< ::duckietown_msgs::SensorsStatusResponse> should match
// service_traits::DataType< ::duckietown_msgs::SensorsStatus >
template<>
struct DataType< ::duckietown_msgs::SensorsStatusResponse>
{
  static const char* value()
  {
    return DataType< ::duckietown_msgs::SensorsStatus >::value();
  }
  static const char* value(const ::duckietown_msgs::SensorsStatusResponse&)
  {
    return value();
  }
};

} // namespace service_traits
} // namespace ros

#endif // DUCKIETOWN_MSGS_MESSAGE_SENSORSSTATUS_H