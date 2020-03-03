from __future__ import print_function
import sys
import os
import random

############# INSTRUCTIONS FOR RUNNING THIS PROGRAM ON LINUX ###############
#
#	1. in the terminal, navigate to the folder
# 	containing this file
#
# 	2. set the random seed environment variable to 
# 	a value of your liking like this:
#
#		export RANDOM_SEED=<number of your choosing>
#
#	   for example:
#
#	    export RANDOM_SEED=13
#
#	3. run the following command:
#
#		python Project2.py <memory_size> <page_size> <number_of_jobs> <min_runtime> 	       <max_runtime> <min_program_memory> <max_program_memory>
#
#	   here's an example:
#		
#		python Project2.py 64000 1000 10 4 10 5000 17000
#
#	   NOTE: make sure that the minimum runtime is smaller than maximum runtime
#			 (same for minimum program memory as well). The program will crash 
#			 in that instance. Also don't make page size larger than overall 
#			 memory size.
#
###########################################################################

# we instantiate each job as an object and store
# each job object in a list
class Job:
	def __init__(self, program_name, runtime, memory_size):
		self.program_name = program_name
		self.memory_size = memory_size
		self.runtime = runtime

# this function is being defined here to make the code look
# less clunky than it already does. The page table is printed
# with a  space in between each page because I had to
# alter it to make it cleanly print the page table when 
#there are 10+ jobs
def print_page_table(simulated_memory_size, memory_list):
	print("    Page table:")
	print("        ", end='')
	
	# printing a space after each 4 pages
	for i in range(int(simulated_memory_size) / 1000):
		if (i > 0 and (i % 4 == 0) and (i % 16 != 0)):
			print("   ", end='')

		# if we still have programs to place in memory
		# then we print the appropriate entry. else,
		# we print "."
		if (i < len(memory_list)):
			print("{0:2} ".format(str(memory_list[i])), end='')
		else:
			print(".  ", end='')
		
		# this if statement prints the first
		# newline, and the one after this one
		# prints each consecutive new line. I
		# can't remember how each works... this
		# part was frustrating so I was just 
		# trying stuff pretty much at random
		# until it worked. 
		if (i > 0 and i < 16 and i % 15 == 0):
			print()
			print("        ", end='')

		if (i > 15 and (i + 1) % 16 == 0):
			print()
			print("        ", end='')

	# this print is solely for formatting 
	print()

def main():

	# each of these lists will hold a value relevant to
	# a job at a particular index. job 1's info will be 
	# at index 0, job 2's info will be at index 1, etc.
	jobs_list = []
	memory_list = []
	runtime_list = []
	job_names_list = []
	memorysize_list = []
	end_time_list = []

	# the command used to start this program
	# is treated as an array, and we can access
	# each parameter in the list using this sys
	# stuff
	random_seed = os.environ.get('RANDOM_SEED')
	simulated_memory_size = sys.argv[1]
	page_size = sys.argv[2]
	num_jobs = sys.argv[3]
	min_runtime = sys.argv[4]
	max_runtime = sys.argv[5]
	min_memory = sys.argv[6]
	max_memory = sys.argv[7]
	
	# printing information as required
	print("\nSimulator Parameters:")
	print("   Memory size: " + str(simulated_memory_size))
	print("   Page size: " + str(page_size))
	print("   Random seed: " + str(random_seed))
	print("   Number of jobs: " + str(num_jobs))
	print("   Runtime (min-max) timesteps: " + str(min_runtime) + "-" + str(max_runtime))
	print("   Memory (min-max): " + str(min_memory) + "-" + str(max_memory))
	print()

	# generating list of runtime of each job
	random.seed(random_seed)
	for i in range(int(num_jobs)):
		runtime_list.append(random.randint(int(min_runtime), int(max_runtime)))

	# each job is named in increasing order starting at 1
	for i in range(int(num_jobs)):
		job_names_list.append(i + 1)

	# generating list of memory size of each job...
	# we are using the round function to round each randomly generated
	# number to the nearest 1000
	for i in range(int(num_jobs)):
		memorysize_list.append(int(round(random.randint(int(min_memory), int(max_memory)), -3)))


	# adding jobs to jobs list and memory sizes to memory list
	remaining_memory = int(simulated_memory_size) / 1000
	for i in range(int(num_jobs)):

		# this if-else checks whether there is enough memory remaining
		# to add the job... if not, it will say so. if so, the job gets
		# added to jobs_list and the job gets added to memory (added to
		# memory list)
		if(remaining_memory < (memorysize_list[i] / 1000)):
			for j in range(i, int(num_jobs)):
				print("Job #" + str(j + 1) + " was not added... not enough space in memory!")
			print()
			# we are breaking here because (to quote the assignment): 
			# "Repeat until there aren't enough pages available to 
			# schedule the next job in the queue." If we didn't break
			# here and there was a job further down the line that had 
			# a smaller required memory size, it would be put into
			# the queue
			break
		else:
			jobs_list.append(Job(job_names_list[i], runtime_list[i], memorysize_list[i]))
			for j in range(memorysize_list[i] / 1000):
				memory_list.append(job_names_list[i])
			remaining_memory = remaining_memory - (memorysize_list[i] / 1000)
	
	# we need this number_of_jobs variable at the end of the 
	# program when we print out each job's start + end time.
	# I was originally using len(jobs_list) down there, but
	# as the simulation runs, len(jobs_list) shrinks down
	# to zero, and we need the original number of jobs
	# as the program runs.
	number_of_jobs = len(jobs_list)		

	# printing job queue
	print("Job Queue:")
	print("    Job #    Runtime    Memory")
	for i in range(len(jobs_list)):
		print("        {0} {1:>10} {2:>9}".format(str(jobs_list[i].program_name), str(jobs_list[i].runtime), str(jobs_list[i].memory_size)))

	# initializing end_time_list to all zeros... no particular
	# reason for using 0, we just need this list to have as
	# many indices as there are jobs added to the queue.
	for i in range(len(jobs_list)):
		end_time_list.append(0)

	# running the simulator below
	print("\nSimulator Starting:\n")
	# the simulator starts at t = 1
	time_step = 1

	# the simulator will end when the jobs list has no
	# more items in it
	while len(jobs_list) > 0:
		print("Time Step " + str(time_step) + ":")

		# all jobs start at t = 1, so we print out
		# that each job is starting when t = 1
		if (time_step == 1):
			for i in range(len(jobs_list)):
				print("    Job " + str(i + 1) + " Starting")

		# each time this while loop runs, we print out the
		# currently running job (which will always be the 
		# first element in jobs_list)
		print("    Job " + str(jobs_list[0].program_name) + " Running")

		# printing the page table each loop
		print_page_table(simulated_memory_size, memory_list)
		
		# if the job still has remaining runtime,
		# we decrement the job's current runtime
		# and put it in the back of the list
		if (jobs_list[0].runtime > 0):
			jobs_list[0].runtime = jobs_list[0].runtime - 1
			temp_job_variable = jobs_list[0]
			jobs_list.pop(0)
			jobs_list.append(temp_job_variable)

		# if the jobs has zero runtime remaining,
		# we print that it's completed and 
		# replace all instances of that job in the
		# memory_list with "." and remove the job
		# from jobs_list
		else:
			print("-------Job " + str(jobs_list[0].program_name) + " completed-------\n")
			for i in range(len(memory_list)):
				if memory_list[i] == jobs_list[0].program_name:
					memory_list[i] = "."

			# program names are assigned starting at 1, but each relevant 
			# index is 1 less than the program name, hence the "- 1" in the
			# end_time_list index below.
			end_time_list[jobs_list[0].program_name - 1] = time_step
			#end_time_list.append(time_step)
			
			# here, the job has 0 time left, so when we pop it
			# we don't need to put it back at the end of the list.
			jobs_list.pop(0)
		
		# one time slice elapses each time 
		# through the loop
		time_step = time_step + 1

	# displaying end job information
	print("\nJob Information:\n")
	print("    Job #    Start Time    End Time")
	for i in range(number_of_jobs):
		print("        {0:4} {1:10} {2:11}".format(str(i + 1), 1, end_time_list[i]))
	print()

# this runs the program... to be honest I don't
# understand how this works... usually I would just put
# "main()" here to start this program, but I have come
# to understand that this is the better way to do it.
if __name__ == "__main__":
	main()




