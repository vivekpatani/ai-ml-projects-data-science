import json
import math

def recommendor_similarity():

    similarity_measure_eucledian = {}
    similarity_measure_manhattan = {}
    similarity_measure_L_Max = {}

    with open('udata.json') as user_data:
        u_data = json.load(user_data)
        with open('udata_movie.json') as movie_file:
            #m_data = json.load(movie_file)
            for user in u_data:
                similarity_measure_eucledian.setdefault(user,{})
                similarity_measure_manhattan.setdefault(user,{})
                similarity_measure_L_Max.setdefault(user,{})
                for compared_user in u_data:
                    if compared_user != user:
                        similarity_quotient_eucledian = comparator_eucledian_test(u_data,user,compared_user)
                        similarity_measure_eucledian[user][compared_user] = similarity_quotient_eucledian

                        similarity_quotient_manhattan = comparator_manhattan_test(u_data,user,compared_user)
                        similarity_measure_manhattan[user][compared_user] = similarity_quotient_manhattan
                        
                        similarity_quotient_L_Max = comparator_L_Max_test(u_data,user,compared_user)
                        similarity_measure_L_Max[user][compared_user] = similarity_quotient_L_Max

                        
    for each in similarity_measure_eucledian:
        print(similarity_measure_eucledian[each])

    with open('similairty_data_eucledian.json','w') as similarity_data:
        json.dump(similarity_measure_eucledian,similarity_data,ensure_ascii=False,indent=4)

    for each in similarity_measure_manhattan:
        print(similarity_measure_manhattan[each])

    with open('similairty_data_manhattan.json','w') as similarity_data:
        json.dump(similarity_measure_manhattan,similarity_data,ensure_ascii=False,indent=4)

    for each in similarity_measure_L_Max:
        print(similarity_measure_L_Max[each])

    with open('similairty_data_L_Max.json','w') as similarity_data:
        json.dump(similarity_measure_L_Max,similarity_data,ensure_ascii=False,indent=4)


def comparator_eucledian_test(u_data,user,compared_user):

        similarity_measure_eucledian = {}
        for each_movie in u_data[user]:
            if each_movie in u_data[compared_user]:
                similarity_measure_eucledian[each_movie] = 1
        
        distance_measure = sum([pow(u_data[user][each_movie] - u_data[compared_user][each_movie], 2) for each_movie in similarity_measure_eucledian])
        return round(1 / (1 + math.sqrt(distance_measure)),2)

def comparator_manhattan_test(u_data,user,compared_user):

        similarity_measure = {}
        for each_movie in u_data[user]:
            if each_movie in u_data[compared_user]:
                similarity_measure_manhattan[each_movie] = 1

        distance_measure = sum([abs(u_data[user][each_movie] - u_data[compared_user][each_movie], 2) for each_movie in similarity_measure_manhattan])
        return round(1 / (1 + math.sqrt(distance_measure)),2)

def comparator_L_Max_test(u_data,user,compared_user):

        similarity_measure = {}
        for each_movie in u_data[user]:
            if each_movie in u_data[compared_user]:
                similarity_measure_L_Max[each_movie] = 1

        distance_measure = max([abs(u_data[user][each_movie] - u_data[compared_user][each_movie], 2) for each_movie in similarity_measure])
        return round(1 / (1 + math.sqrt(distance_measure)),2)


def main():
    recommendor_similarity()
    
if __name__ == "__main__":
    main()
