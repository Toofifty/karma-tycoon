import json, os

PATH = "../data/units"

def main():    
    with open(PATH, 'r') as f:
        data = json.load(f)
        
    print data
    
    id = raw_input("id: ")
    name = raw_input("name: ")
    short_name = raw_input("short_name: ")
    type = raw_input("type (comment/post): ")
    init_cost = int(raw_input("init_cost: "))
    init_profit = int(raw_input("init_profit: "))
    init_time = int(raw_input("init_time (s): "))
    amount = int(raw_input("amount: "))
    print "unit created"
    
    data[type][id] = {"type":type, "name":name, 
            "short_name":short_name, "init_cost":init_cost,
            "init_profit":init_profit, "init_time":init_time,
            "amount":amount}
     
    with open(PATH, 'w') as f:
        json.dump(data, f, sort_keys=True,
            indent=4, separators=(',', ': '))
    more = raw_input("create more? (y/n)")
    if (more is "y"):
        main()
    
if __name__ == "__main__":
    main()