#!usr/bin/env bash

#set -x

function create_qsub_command {
    # Step 9: Write a script either in Shell or Python that takes a directory path as input and
    # writes for each file in this directory an according qsub command to stdout.
    
    for file in $(ls $1):
    do
	echo "qsub coding_exercises_day1_step6.sh $file" > run.sh
    done
    
}

# Step 10: Collect all qsub commands into the runscript run.sh by using the redirect 
# ‘>’and execute the resulting script.
create_qsub_command . >> run.sh

chmod +x run.sh
./run.sh
