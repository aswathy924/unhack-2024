import json

with open('.\MilestoneInputs\Input\Milestone0.json','r') as file:
    data = json.load(file)

steps = data['steps']
machines = data['machines']
wafers = data['wafers']


no_steps = len(steps)
schedule = []
time = {}

n=0
start_time = 0

while no_steps > 0:
    steps_wafer = steps[n]
    wafer_count = wafers[0]['quantity']
    wafer_num = 1

    while wafer_count > 0 :
        
        for i in range(len(machines)):
            if machines[i]["step_id"] == steps_wafer['id']:
                machine = machines[i]
                break
        
        #print(machine)

        if (machine['initial_parameters']['P1'] in range(steps_wafer['parameters']['P1'][0] , steps_wafer['parameters']['P1'][1]+1)): #and machine_working[machine["machine_id"]] == False:
           
            wafer_id = wafers[0]['type'] + "-" + str(wafer_num)
            step_id = steps_wafer['id']
            machine_id = machine['machine_id']
            end_time = wafers[0]['processing_times'][step_id]
            schedule.append({'wafer_id': wafer_id,'step': step_id,'machine':machine_id,"start_time":start_time,"end_time":end_time+start_time})

            time[wafer_id] = end_time

        wafer_count -= 1
        wafer_num += 1
        start_time += end_time

    start_time = time[wafer_id]
    no_steps -= 1
    n += 1  

for i in schedule:
    print(i)

schedule = {'schedule': schedule}
json_obj = json.dumps(schedule,indent=1)
with open(".\output\Milestone0.json",'w') as outfile:
    outfile.write(json_obj)