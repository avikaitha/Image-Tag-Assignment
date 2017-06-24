from ast import literal_eval
with open("output.txt",'r') as f:
    content = f.readlines()
with open("tag_set",'r') as f:
    tag_set = f.readlines()
tag_set = [tag.strip() for tag in tag_set]
with open("new_photo_ids_test_100.txt",'r') as f:
    photo_list = f.readlines()
photo_list = [tag.strip() for tag in photo_list]

nf = open("Actual_output.txt",'w')
for ind,line in enumerate(content):
    line = line.split("->")
    no_of_tags = float(line[0].strip())
    tag_list = line[1].strip()
    tag_list = tag_list.strip("[]")
    tag_list = tag_list.split(' ')
    tag_list = [int(tag) for tag in tag_list if tag != '']
    tag_list = [tag_set[(tag+1)%len(tag_set)] for tag in tag_list]
    # print no_of_tags,tag_list, photo_list[ind]

    tag_str = " ".join(tag_list)
    print photo_list[ind]+" "+tag_str+" "+str(no_of_tags)+"\n"
    nf.write(photo_list[ind]+" "+tag_str+" "+str(no_of_tags)+"\n")


nf.close()