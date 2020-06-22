import numpy
import pandas

# low engagement rate
def lowengr(x1,x2,x):
    if x <= x1:
        return 1
    elif x >= x2:
        return 0
    else: return (x2-x)/(x2-x1)

# average engagement rate
def avrgengr(x1,x2,x3,x4,x):
    if x >= x2 and x <= x3:
        return 1
    elif x < x1 or x >= x4:
        return 0
    elif x >= x1 and x < x2:
        return (x-x1)/(x2-x1)
    else: return (x4-x)/(x4-x3)

# high engagement rate
def highengr(x1,x2,x3,x4,x):
    if x >= x2 and x <= x3:
        return 1
    elif x < x1 or x >= x4:
        return 0
    elif x >= x1 and x <= x2:
        return (x-x1)/(x2-x1)
    else: return (x4-x)/(x4-x3)

# very high engagement rate
def vhighengr(x1,x2,x):
    if x <= x1:
        return 0
    elif x >= x2:
        return 1
    else: return (x-x1)/(x2-x1)

# low follower count
def lowfoll(x1,x2,x):
    if x <= x1:
        return 1
    elif x >= x2:
        return 0
    else: return (x2-x)/(x2-x1)

# average follower count
def avrgfoll(x1,x2,x3,x4,x):
    if x >= x2 and x <= x3:
        return 1
    elif x < x1 or x >= x4:
        return 0
    elif x >= x1 and x < x2:
        return (x-x1)/(x2-x1)
    else: return (x4-x)/(x4-x3)

# high follower count
def highfoll(x1,x2,x):
    if x <= x1:
        return 0
    elif x >= x2:
        return 1
    else: return (x-x1)/(x2-x1)

# will count the engagement rate of each influencer
def engagement(engr):
    # x1, x2, x
    lower = [1.2, 2.1, engr]
    vhigher = [5.2, 7.2, engr]
    # x1, x2, x3, x4, x
    avrger = [0.9, 1.8, 3.9, 4.6, engr]
    higher = [2.7, 4.2, 6, 8, engr]

    ler = lowengr(lower[0],lower[1],lower[2])
    aer = avrgengr(avrger[0],avrger[1],avrger[2],avrger[3],avrger[4])
    her = highengr(higher[0],higher[1],higher[2],higher[3],higher[4])
    vher = vhighengr(vhigher[0],vhigher[1],vhigher[2])

    return [vher,her,aer,ler]

# will count the follower count of each influencer
def follower(foll):
    # x1, x2, x
    lowfc = [18000, 35000, foll]
    highfc = [50000, 70000, foll]
    # x1, x2, x3, x4, x
    avrgfc = [15000, 30000, 63000, 75000, foll]

    lfc = lowfoll(lowfc[0],lowfc[1],lowfc[2])
    afc = avrgfoll(avrgfc[0],avrgfc[1],avrgfc[2],avrgfc[3],avrgfc[4])
    hfc = highfoll(highfc[0],highfc[1],highfc[2])

    return [hfc,afc,lfc]

# inference function
def inference(engr, foll):
    score = []
    for i in range (len(engr)):
        acc = []
        con = []
        rej = []

        for j in range(len(engr[i])):
            a = []
            f = [min(engr[i][j],foll[i][0]), min(engr[i][j],foll[i][1]), min(engr[i][j],foll[i][2])]
            
            # engr very high
            if j == 0:
                a.extend([{"ket":"Accepted","score":f[0]}, {"ket":"Accepted","score":f[1]}, {"ket":"Considered","score":f[2]}])
            # engr high
            elif j == 1:
                a.extend([{"ket":"Accepted","score":f[0]}, {"ket":"Accepted","score":f[1]}, {"ket":"Considered","score":f[2]}])
            # engr average
            elif j == 2:
                a.extend([{"ket":"Considered","score":f[0]}, {"ket":"Considered","score":f[1]}, {"ket":"Reject","score":f[2]}])
            # engr low
            else:
                a.extend([{"ket":"Reject","score":f[0]}, {"ket":"Reject","score":f[1]}, {"ket":"Reject","score":f[2]}])
            # endif
            
            for k in range(len(a)):
                if a[k]["ket"] == "Accepted":
                    acc.append(a[k]["score"])
                elif a[k]["ket"] == "Considered":
                    con.append(a[k]["score"])
                else:
                    rej.append(a[k]["score"])

                # endif
            # endfor
        # endfor

        score.append([max(acc),max(con),max(rej)])
    # endfor
    
    return score

# defuzzy function
def deFuzzyFunc(rawscore, acc, con, rej):
    score = []

    for i in range(len(rawscore)):
        tot = (rawscore[i][0]*acc + rawscore[i][1]*con + rawscore[i][2]*rej )/sum(rawscore[i])
        score.extend([tot])
    
    return score

# find best 20 to be accepted
# using Sugino Style
def accOrNot(score,id,foll,engr):
    f = open("Result.csv","w")
    arr1 = []
    arr2 = []
    arr3 = []
    print("List of people who got accepted :")
    for i in range(20):
        
        # if the influencer has the same score, will get the first one with the biggest follower count
        if score.count(max(score)) > 1:
            arr1 = score.copy()
            arr2 = foll.copy()
            arr3 = id.copy()
            arr4 = []
            arr5 = []
            for j in range(score.count(max(score))):
                # store influencer follower data has biggest score
                arr4.append(arr2[arr1.index(max(arr1))])
                arr5.append(arr3[arr1.index(max(arr1))])
                arr2.pop(arr1.index(max(arr1)))
                arr1.pop(arr1.index(max(arr1)))
                arr3.pop(arr1.index(max(arr1)))
            
            # get influencer id that has the biggest follower in the biggest score
            ids = arr4.index(max(arr4))
            idx = arr5[ids]
            index = id.index(idx)

        else:
            index = score.index(max(score))

        print("No ",i+1)
        print("Id : ",id[index])
        f.write(str(id[index])+ "\n")
        print("Follower Count : ",foll[index])
        print("Engagement Rate : ",engr[index])
        print("Total Score : ",score[index])
        print("")
        score.pop(index)
        id.pop(index)
        foll.pop(index)
        engr.pop(index)

def main():
    # stores data influencers.csv into influencers
    read = pandas.read_csv('influencers.csv')

    # get data from influencer.csv
    id = list(read['id'].values)
    foll = list(read['followerCount'].values)
    engr = list(read['engagementRate'].values)

    engagementRate,followerCount = [],[]

    # Fuzzification
    for i in range(len(foll)):
        engagementRate.append(engagement(engr[i]))
        followerCount.append(follower(foll[i]))

    # Inference
    rawscore = inference(engagementRate,followerCount)

    # Sugino Style
    Accepted = 100
    Considered = 75
    Rejected = 50

    # Defuzzification
    score = deFuzzyFunc(rawscore, Accepted, Considered, Rejected)

    accOrNot(score,id,foll,engr)

if __name__ == "__main__":
    main()
