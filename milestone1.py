import json

with open('.\MilestoneInputs\Input\Milestone1.json','r') as file:
    data = json.load(file)

steps = data['steps']
machines = data['machines']
wafers = data['wafers']

schedule = []

wafer_num = 1
dict = {}

while wafer_num <= wafers[0]['quantity']:
    
    for step in list(wafers[0]['processing_times'].keys()):
        
        for i in range(len(machines)):
            if machines[i]["step_id"] == step:
                machine = machines[i]
                dict[(wafer_num,step,machine['machine_id'])] = False
    
    wafer_num += 1

print(dict)

wafer = []
w = 0
for i in range(1,wafers[0]['quantity']+1):
    wafer.append(i)

machine = []
m = 0
for i in range(len(machines)):
    machine.append(machines[i]['machine_id'])

time_w = {}
for i in range(1,wafers[0]['quantity']+1):
    time_w[str(i)] = 0

time_s = {}
for i in range(len(machines)):
    time_s[machines[i]['machine_id']] = 0

while len(dict) > 0:

    wafer_num = wafer[w]
    curr_machine = machine[m]

    for i in range(len(machines)):
        if machines[i]['machine_id'] == curr_machine:
            mach = machines[i]
            break

    curr_step = mach['step_id']

    for i in range(len(steps)):
        if steps[i]['id'] == curr_step:
            stp = steps[i]
            break

    exist = dict.get((wafer_num,curr_step,curr_machine),'n')

    if exist != 'n':

        if (mach['initial_parameters']['P1'] in range(stp['parameters']['P1'][0] , stp['parameters']['P1'][1]+1)):

            wafer_id = wafers[0]['type'] + "-" + str(wafer_num)
            step_id = stp['id']
            machine_id = mach['machine_id']
            start_time = max(time_w[str(wafer_num)],time_s[machine_id])
            end_time = wafers[0]['processing_times'][step_id]
            schedule.append({'wafer_id': wafer_id,'step': step_id,'machine':machine_id,"start_time":start_time,"end_time":end_time+start_time})

            time_s[machine_id] = start_time+end_time
            time_w[str(wafer_num)] = end_time

            dict.pop((wafer_num,step_id,machine_id))
            for key in list(dict.keys()):
                if key[0] == wafer_num and key[1] == step_id:
                    dict.pop(key)

            if w < len(wafer)-1:
                w += 1
            else:
                w = 0

            if m < len(machine)-1:
                m += 1
            else:
                m = 0

    else:
        if m < len(machine)-1:
            m += 1
        else:
            m = 0

for i in schedule:
    print(i)

        
schedule = {'schedule': schedule}
json_obj = json.dumps(schedule,indent=1)
with open(".\output\Milestone1.json",'w') as outfile:
    outfile.write(json_obj)



