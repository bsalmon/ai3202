#Assignment 5 
###### CSCI 3202
###### Brian Salmon


Program can be run through the command line with the filename, world, and an epsilon value.
For example:
```
  python assignment5_mdp.py World1MDP.txt 0.5
```
Returns:
  ```
user@cu-cs-vm:~/ai/ai3202/Assignment5$ python assignment5_mdp.py World1MDP.txt 0.5
Location: (0,0)  Utility: 5.629
Location: (1,0)  Utility: 6.361
Location: (2,0)  Utility: 7.607
Location: (3,0)  Utility: 8.664
Location: (4,0)  Utility: 9.830
Location: (5,0)  Utility: 11.316
Location: (6,0)  Utility: 12.888
Location: (6,1)  Utility: 14.875
Location: (6,2)  Utility: 16.942
Location: (6,3)  Utility: 19.124
Location: (6,4)  Utility: 22.930
Location: (7,4)  Utility: 26.591
Location: (7,5)  Utility: 29.352
Location: (8,5)  Utility: 33.400
Location: (9,5)  Utility: 38.039
Location: (9,6)  Utility: 43.902
End: (9,7)  Reward: 50.000
```

### Answer to Question:

  Increasing the epsilon value from 0.5 caused the utility to lower. An epsilon value of 450 or greater changed the solution path entirely. However the new path is suboptimal because it crosses over two extra mountains compared to the first path. Any epsilon value greater than 160,999,999,999,989,999 results in an error and fails to move beyond the first node.
  
  When e = 160999999999989999:
  ```
user@cu-cs-vm:~/ai/ai3202/Assignment5$ python assignment5_mdp.py World1MDP.txt 160999999999989999
Location: (0,0)  Utility: 0.362
Location: (0,1)  Utility: 0.450
Location: (0,2)  Utility: 0.875
Location: (0,3)  Utility: 1.302
Location: (1,3)  Utility: 1.808
Location: (1,4)  Utility: 2.511
Location: (1,5)  Utility: 2.099
Location: (2,5)  Utility: 2.915
Location: (3,5)  Utility: 3.766
Location: (4,5)  Utility: 4.734
Location: (4,6)  Utility: 6.214
Location: (4,7)  Utility: 7.783
Location: (5,7)  Utility: 12.199
Location: (6,7)  Utility: 16.942
Location: (7,7)  Utility: 24.920
Location: (8,7)  Utility: 36.000
End: (9,7)  Reward: 50.000
```
When e = 160999999999990000:
```
user@cu-cs-vm:~/ai/ai3202/Assignment5$ python assignment5_mdp.py World1MDP.txt 160999999999990000
Final Location: (0,0) Utility: 0.000
user@cu-cs-vm:~/ai/ai3202/Assignment5$ 
```
  
