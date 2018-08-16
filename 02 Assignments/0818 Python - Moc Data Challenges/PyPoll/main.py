#start by import the package we need
import os, csv

#define resources path
csv_path = os.path.join("..", "Resources", "election_data.csv")

#define variables
total_votes = 0
total_candidate = 0
candidate_list = []
candidate_vote = {}
candidate_avg = {}

#make csv file an iteratable object, including dictionary type of reader
with open(csv_path, newline="", encoding="UTF-8") as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=",")
    #define dictionary of candidates:
    for row in csv_reader:
        #find total vote
        total_votes += 1
        #find total candidate
        total_candidate = row["Candidate"]
        #create candidate list; if candidate exist + 1 vote, 
        #if candidate do not exist, append to the list
        if row["Candidate"] not in candidate_list:
            #add candidate to the list
            candidate_list.append(row["Candidate"])
            #new candidate earn first vote
            candidate_vote[row["Candidate"]] = 1
        else:
            #existing candidate vote addition
            candidate_vote[row["Candidate"]] += 1

#sort the candidate vote list
sorted_candidates = [k for k in sorted(candidate_vote, key=candidate_vote.get, reverse=True)]
#find the winner
winner = sorted_candidates[0]

#result output in console
print("\nElection Results")
print("-------------------------")
print(f"Total Votes: {total_votes}")
print("-------------------------")
for candidate_name,vote_count in candidate_vote.items():
    print(candidate_name + " " + str(round(vote_count / total_votes * 100, 2)) + "% (" + str(vote_count) + ")")
print("-------------------------")
print("Winner: " + winner)
print("-------------------------")