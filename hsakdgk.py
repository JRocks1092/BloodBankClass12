from datetime import datetime
d = datetime.strptime("04-Jan-2021-02:45:12", "%d-%b-%Y")

# convert datetime format into %Y-%m-%d-%H:%M:%S
# format using strftime
print(d.strftime("%Y-%m-%d-%H:%M:%S"))
