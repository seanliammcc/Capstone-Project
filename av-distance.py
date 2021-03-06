import numpy as np
import random as rand
import subprocess, platform

if platform.system()=="Windows":
    subprocess.Popen("cls", shell=True).communicate() #I like to use this instead of subprocess.call since for multi-word commands you can just type it out, granted this is just cls and subprocess.call should work fine 
else: #Linux and Mac
    print("\033c", end="")

# #servo 1

# distances = np.array([0.0, 20.23, 30.48, 40.64, 50.8, 60.96, 71.12, 81.28, 91.44]) #mm
# N_trials = 50000
# all_dist = np.zeros([N_trials])
# previous_rand = 0

# for i in range(0,N_trials):
#     shuffler = np.zeros([len(distances)])
#     shuffler[0] = 1
#     dist = 0
#     positions = [0, 1, 2, 3, 4, 5, 6, 7, 8]
#     for j in range(0,51):
#         num = rand.choice(positions)
#         # while num == previous_rand and len(positions) > 2: #prevents card from going into same slot
#         #     num = rand.choice(positions) 
#         shuffler[num] = shuffler[num] + 1
#         if shuffler[num] == 6:
#             positions.remove(num)
#         dist = dist + abs(distances[num] - distances[previous_rand])
#         previous_rand = num
#     #print(shuffler)
#     all_dist[i] = dist

# avg = np.average(all_dist)

# print("The average distance is: " + str(round(avg,2)) + "mm")
# print("In inches, this is: " + str(round(avg*0.0393701,2)) + "in")
# dist_per_card = avg*0.0393701/52
# print("The average distance per card is: " + str(round(avg*0.0393701/52,4)) + "in")
# print("To run in less than 30 seconds, this means that the servo must go hella fast.")
# time_per_card = 30/52
# dispense_time = .25
# servo_time = time_per_card - dispense_time
# print("The servo must move to the next position in " + str(round(servo_time,2)) + "s")
# pinion_pitch_d = 1 #mm
# theta = dist_per_card/(pinion_pitch_d/2)
# print("The servo must go " + str(theta) + " rad")
# print("The servo must go " + str(theta* 180/np.pi) + " deg")



#Servo 2
bike_width = 2.5 #in
ts = .25 #s
rod_d = 3.175 #mm
disp_len = 72.8980 #mm
spacing = (3.5473 - rod_d)
s2_speed = disp_len / ts
s2_theta = disp_len / (rod_d/2) * 180/np.pi
print("Servo 2 must move " + str(s2_theta) + " degrees")
print("This is " + str(s2_theta/360 / ts * 60) + " rotations per minute")

#Servo 3
larger_d = 4.0640 #mm
req_dist = disp_len / 2
s3_theta = req_dist/(larger_d/2) * 180/np.pi
print("Servo 3 must move " + str(s3_theta) + " degrees")
print("This is " + str(s3_theta/360 / ts * 60) + " rotations per minute")
    