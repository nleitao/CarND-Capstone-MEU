#!/usr/bin/env python

import rospy
from geometry_msgs.msg import PoseStamped
from styx_msgs.msg import Lane, Waypoint

import math

'''
This node will publish waypoints from the car's current position to some `x` distance ahead.

As mentioned in the doc, you should ideally first implement a version which does not care
about traffic lights or obstacles.

Once you have created dbw_node, you will update this node to use the status of traffic lights too.

Please note that our simulator also provides the exact location of traffic lights and their
current status in `/vehicle/traffic_lights` message. You can use this message to build this node
as well as to verify your TL classifier.

TODO (for Yousuf and Aaron): Stopline location for each traffic light.
'''

LOOKAHEAD_WPS = 200 # Number of waypoints we will publish. You can change this number


class WaypointUpdater(object):
    def __init__(self):

        rospy.init_node('waypoint_updater')

        # final=Lane
        # self.posex=0
        
        rospy.Subscriber('/current_pose', PoseStamped, self.pose_cb)
        rospy.Subscriber('/base_waypoints', Lane, self.waypoints_cb)

        # TODO: Add a subscriber for /traffic_waypoint and /obstacle_waypoint below


        self.final_waypoints_pub = rospy.Publisher('final_waypoints', Lane, queue_size=1)


        # TODO: Add other member variables you need below

        rospy.spin()

    def pose_cb(self, msg):
        # TODO: Implement
        #
        # rate=rospy.Rate(10)
        # while not rospy.is_shutdown():

        #     print("current pose")
        #     print(msg.pose.position.x)
        #     print(msg.pose.position.y)
        #     print(msg.pose.position.z)

        #     rate.sleep()
        self.pose=msg.pose.position
        self.posex=msg.pose.position.x
        self.posey=msg.pose.position.y
        self.posez=msg.pose.position.z


        
        
        
        

        # print("inside",self.posex)

        pass

    def waypoints_cb(self, waypoints):
        # TODO: Implement

        # print(waypoints.waypoints[0].twist.twist.linear.x)

        # print(len(waypoints.waypoints))

        # print(waypoints)   


        # global final
        # final=waypoints 
        start_time=0
        rate=rospy.Rate(6)

        while not start_time:
            start_time=rospy.Time.now().to_sec()
            

        while not rospy.is_shutdown():

            rate.sleep()

            dl = lambda a, b: math.sqrt((a.x-b.x)**2 + (a.y-b.y)**2  + (a.z-b.z)**2)
            distance=9999
            index=None

            for i in range(len(waypoints.waypoints)):
                point_distance=dl(waypoints.waypoints[i].pose.pose.position,self.pose)
                if point_distance<distance:
                    distance=point_distance
                    index=i
            

            subset=waypoints
            subset.header=waypoints.header
            subset.waypoints=waypoints.waypoints[i:i+LOOKAHEAD_WPS]



            self.final_waypoints_pub.publish(subset)


        pass





    def traffic_cb(self, msg):
        # TODO: Callback for /traffic_waypoint message. Implement
        pass

    def obstacle_cb(self, msg):
        # TODO: Callback for /obstacle_waypoint message. We will implement it later
        pass

    def get_waypoint_velocity(self, waypoint):
        return waypoint.twist.twist.linear.x

    def set_waypoint_velocity(self, waypoints, waypoint, velocity):
        waypoints[waypoint].twist.twist.linear.x = velocity

    def distance(self, waypoints, wp1, wp2):
        dist = 0
        dl = lambda a, b: math.sqrt((a.x-b.x)**2 + (a.y-b.y)**2  + (a.z-b.z)**2)
        for i in range(wp1, wp2+1):
            dist += dl(waypoints[wp1].pose.pose.position, waypoints[i].pose.pose.position)
            wp1 = i
        return dist

if __name__ == '__main__':
    try:
        WaypointUpdater()
    except rospy.ROSInterruptException:
        rospy.logerr('Could not start waypoint updater node.')
