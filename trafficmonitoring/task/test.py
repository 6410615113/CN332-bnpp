

report_result = '../media/uploads/admin/98/object_tracking/loop.txt'
report_car = []
f = open(report_result, "r")
for x in f:
    report_car.append(x.split(','))
print(report_car)