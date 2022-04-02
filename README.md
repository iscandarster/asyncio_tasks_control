# Test of asyncio extended task control
#### From Caleb Hattingh's O'Reilly book Using Asyncio in Python: Understanding Python's Asynchronous Programming Features


### Shows 2 possibilities:
 - 1 One task shuts down after completed its job and then shuts down other tasks,
 - 2 Shutdown of all tasks when interrupted by signal

 ### For both cases:
 - All tasks only stop after 'except CancelledError' has fully finished

Example of output for both cases:

~~~
$ python3 tasks_example.py 
Task one__running_for_ever is running...
Task two__stop_after_job_done 3
Task three__stop_loop_at_the_end running
Task one__running_for_ever is running...
Task two__stop_after_job_done 2
Task one__running_for_ever is running...
Task one__running_for_ever is running...
Task three__stop_loop_at_the_end running
Task two__stop_after_job_done 1
Task one__running_for_ever is running...
Task one__running_for_ever is running...
Task two__stop_after_job_done has finished
Task two__stop_after_job_done cancelling other tasks
Task three__stop_loop_at_the_end got CancelledError
Task one__running_for_ever got CancelledError
Task one__running_for_ever CancelledError is shutting down...3
Task three__stop_loop_at_the_end awaiting to stop
Task one__running_for_ever CancelledError is shutting down...2
Task three__stop_loop_at_the_end awaiting to stop
Task one__running_for_ever CancelledError is shutting down...1
Task three__stop_loop_at_the_end awaiting to stop
Task three__stop_loop_at_the_end awaiting to stop
Task one__running_for_ever CancelledError has finished
Task three__stop_loop_at_the_end awaiting to stop
Task three__stop_loop_at_the_end CancelledError has finished and has stopped the loop
Task main has finished

$ python3 tasks_example.py 
Task one__running_for_ever is running...
Task two__stop_after_job_done 3
Task three__stop_loop_at_the_end running
Task one__running_for_ever is running...
Task two__stop_after_job_done 2
Task one__running_for_ever is running...
^CGot signal: Signals.SIGINT, shutting down all tasks.
Task three__stop_loop_at_the_end got CancelledError
Task one__running_for_ever got CancelledError
Task one__running_for_ever CancelledError is shutting down...3
Task two__stop_after_job_done got CancelledError
Task three__stop_loop_at_the_end awaiting to stop
Task one__running_for_ever CancelledError is shutting down...2
Task three__stop_loop_at_the_end awaiting to stop
Task one__running_for_ever CancelledError is shutting down...1
Task two__stop_after_job_done CancelledError has finished
Task three__stop_loop_at_the_end awaiting to stop
Task three__stop_loop_at_the_end awaiting to stop
Task one__running_for_ever CancelledError has finished
Task three__stop_loop_at_the_end awaiting to stop
Task three__stop_loop_at_the_end CancelledError has finished and has stopped the loop
Task main has finished

~~~
