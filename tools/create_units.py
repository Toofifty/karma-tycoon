import json, os

PATH = "../data/units.kt"

def main():    
    with open(PATH, 'r') as f:
        data = json.load(f)
    
    print "enter q at any time to exit"
    
    id = raw_input("id: ")
    if id == "q": return
    
    name = raw_input("name: ")
    if name == "q": return
    
    short_name = raw_input("short_name: ").lower()
    if short_name == "q": return
    
    type = raw_input("type (comment/post): ").lower()
    if type == "q": return
    
    init_cost = raw_input("init_cost: ")
    if init_cost == "q": return
    init_cost = int(init_cost)
    
    time = raw_input("init_time (-m, -h, -d): ")
    if time == "q": return
    
    init_profit = raw_input("init_profit: ")
    if init_profit == "q": return
    init_profit = int(init_profit)
    print "unit created"
    
    if type == "l":
        type = "link"
        
    elif type == "c":
        type = "comment"
      
    if time.endswith("s"):
        time = int(time[:-1])
      
    elif time.endswith("m"):
        time = int(time[:-1]) * 60
        
    elif time.endswith("h"):
        time = int(time[:-1]) * (60 * 60)
        
    elif time.endswith("d"):
        time = int(time[:-1]) * (60 * 60 * 24)
        
    else:
        time = int(time)
    
    data[type].append({"id":id, "name":name, 
            "short_name":short_name, "init_cost":init_cost,
            "init_profit":init_profit, "init_time":time,
            "amount":0})
     
    with open(PATH, 'w') as f:
        json.dump(data, f, sort_keys=True,
            indent=4, separators=(',', ': '))
            
    more = raw_input("create more? (y/n)")
    if not more == "n":
        main()
    
if __name__ == "__main__":
    main()