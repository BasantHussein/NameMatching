import operator
from translate import Translator


def similarity(namelist, target):
    """

            Parameters
                    [namelist,target: compute the similarity of the target based on distance, letter's form, phonetics and keyboard similarity]
               ----------

               Returns
               -------
                   [name_list_scores: dictionary for each name in namelist and its ratio]
           """
    # keyboard similarity matrix
    KDS = {
        'columns': ['ط', 'ظ', 'ض', 'ص', 'ش', 'س', 'ز', 'ر', 'ذ', 'د', 'خ', 'ح', 'ج', 'ت', 'ب', 'أ', 'ا'],
        'value':
            [[0.6, 0.7, 0.6, 0.7, 0.6, 0.7, 0.7, 0.8, 0.5, 0.5, 0.7, 0.7, 0.6, 0.9, 0.8, 1.0, 1.0],
             [0.6, 0.7, 0.6, 0.7, 0.6, 0.7, 0.7, 0.8, 0.5, 0.5, 0.7, 0.7, 0.6, 0.9, 0.8, 1.0, 1.0],
             [0.4, 0.5, 0.7, 0.8, 0.8, 0.8, 0.6, 0.9, 0.6, 0.3, 0.6, 0.5, 0.4, 0.8, 1.0, 0.8, 0.8],
             [0.7, 0.7, 0.5, 0.6, 0.5, 0.6, 0.8, 0.7, 0.4, 0.6, 0.8, 0.7, 0.7, 1.0, 0.8, 0.9, 0.9],
             [0.9, 0.8, 0.2, 0.3, 0.2, 0.2, 0.8, 0.4, 0.1, 0.9, 0.8, 0.9, 1.0, 0.7, 0.4, 0.6, 0.6],
             [0.9, 0.8, 0.3, 0.3, 0.2, 0.3, 0.8, 0.5, 0.2, 0.8, 0.9, 1.0, 0.9, 0.7, 0.5, 0.7, 0.7],
             [0.8, 0.8, 0.3, 0.4, 0.3, 0.4, 0.8, 0.6, 0.2, 0.8, 1.0, 0.9, 0.8, 0.8, 0.6, 0.7, 0.7],
             [0.9, 0.8, 0.1, 0.2, 0.1, 0.2, 0.7, 0.3, 0.0, 1.0, 0.8, 0.8, 0.9, 0.6, 0.3, 0.5, 0.5],
             [0.1, 0.1, 0.9, 0.8, 0.8, 0.8, 0.2, 0.6, 1.0, 0.0, 0.2, 0.2, 0.1, 0.4, 0.6, 0.5, 0.5],
             [0.4, 0.5, 0.7, 0.8, 0.7, 0.8, 0.6, 1.0, 0.6, 0.3, 0.6, 0.5, 0.4, 0.7, 0.9, 0.8, 0.8],
             [0.8, 0.9, 0.3, 0.4, 0.3, 0.4, 1.0, 0.6, 0.2, 0.7, 0.8, 0.8, 0.8, 0.8, 0.6, 0.7, 0.7],
             [0.3, 0.3, 0.9, 0.9, 0.9, 1.0, 0.4, 0.8, 0.8, 0.2, 0.4, 0.3, 0.2, 0.6, 0.8, 0.7, 0.7],
             [0.2, 0.2, 0.9, 0.9, 1.0, 0.9, 0.3, 0.7, 0.8, 0.1, 0.3, 0.2, 0.2, 0.5, 0.8, 0.6, 0.6],
             [0.2, 0.3, 0.9, 1.0, 0.9, 0.9, 0.4, 0.8, 0.8, 0.2, 0.4, 0.3, 0.3, 0.6, 0.8, 0.7, 0.7],
             [0.2, 0.2, 1.0, 0.9, 0.9, 0.9, 0.3, 0.7, 0.9, 0.1, 0.3, 0.3, 0.2, 0.5, 0.7, 0.6, 0.6],
             [0.9, 1.0, 0.2, 0.3, 0.2, 0.3, 0.9, 0.5, 0.1, 0.8, 0.8, 0.8, 0.8, 0.7, 0.5, 0.7, 0.7],
             [1.0, 0.9, 0.2, 0.2, 0.2, 0.3, 0.8, 0.4, 0.1, 0.9, 0.8, 0.9, 0.9, 0.7, 0.4, 0.6, 0.6]],

        'index': ['ط', 'ظ', 'ض', 'ص', 'ش', 'س', 'ز', 'ر', 'ذ', 'د', 'خ', 'ح', 'ج', 'ت', 'ب', 'أ', 'ا']

    }
    # phonetics similarity matrix
    PS = {
        'columns': ['ي', 'ى', 'ا', 'أ', 'ء', 'ط', 'ت', 'ذ', 'ض', 'ز', 'ظ', 'س', 'ص', 'ث', 'ن', 'م', 'ق', 'ك', 'ج', 'د',
                    'ع', 'ر'],

        'value':
            [[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.2],
             [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.2],
             [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.4, 0, 0, 0, 0.2, 0],
             [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.4, 0, 0, 0, 0.2, 0],
             [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.4, 0, 0, 0, 0.2, 0],
             [0, 0, 0, 0, 0, 1, 0.8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0.8, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 1, 0.8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0.8, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0.8, 0, 1, 0.8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0.8, 0, 0.8, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0.8, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.8, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.8, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0.6, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.6, 1, 0, 0, 0, 0, 0, 0],
             [0, 0, 0.4, 0.4, 0.4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0.6, 0.4, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.6, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.4, 0, 1, 0.4, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.6, 1, 0, 0],
             [0, 0, 0.2, 0.2, 0.2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
             [0.2, 0.2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]

             ],
        'index': ['ي', 'ى', 'ا', 'أ', 'ء', 'ط', 'ت', 'ذ', 'ض', 'ز', 'ظ', 'س', 'ص', 'ث', 'ن', 'م', 'ق', 'ك', 'ج', 'د',
                  'ع', 'ر']

    }
    # letter's form similarity
    target_l = list(target)
    for s in range(0, len(target_l)):
        if target_l[s] == 'أ':
            target_l[s] = 'ا'
        if target_l[s] == 'آ':
            target_l[s] = 'ا'
        if target_l[s] == 'ي':
            target_l[s] = 'ى'
        target = ''.join(target_l)
    # similarity dict
    name_list_scores = {}

    # loop through the name list
    for x in range(len(namelist)):
        source = namelist[x]
        m = len(source)
        n = len(target)
        sim = 0
        count = 0
        psim = 0
        count2 = 0

        # Create a zero matrix table of size m+1*n+1
        dist_arr = [[0 for z in range(n + 1)] for z in range(m + 1)]

        # loop through the matrix
        for i in range(m + 1):
            for j in range(n + 1):

                # fill the first row and column of the matrix
                if i == 0:
                    dist_arr[i][j] = j
                elif j == 0:
                    dist_arr[i][j] = i

                    # If characters are same, take the diagonal
                elif source[i - 1] == target[j - 1]:
                    dist_arr[i][j] = dist_arr[i - 1][j - 1]
                    sim += 1
                    count += 1

                # If character are different
                else:
                    replace_cell = dist_arr[i - 1][j - 1]
                    dist_arr[i][j] = 1 + min(dist_arr[i][j - 1],  # Insert
                                             dist_arr[i - 1][j],  # Remove
                                             dist_arr[i - 1][j - 1])  # Replace

                    if dist_arr[i][j] == replace_cell + 1 and i <= m - 1 and j <= n - 1:
                        # keyboard similarity
                        if target[j] in KDS['index'] and source[i] in KDS['columns']:
                            target_index = KDS['index'].index(target[j])
                            source_index = KDS['columns'].index(source[i])
                            sim += KDS['value'][target_index][source_index]
                            count += 1
                        # phonetics similarity
                        if target[j] in PS['index'] and source[i] in PS['columns']:
                            target_index = PS['index'].index(target[j])
                            source_index = PS['columns'].index(source[i])
                            psim += PS['value'][target_index][source_index]
                            count2 += 1

        # distance
        dist = dist_arr[m][n]
        # distance ratio
        dist_ratio = ((m + n) - dist) / (m + n)
        # keyboard ratio
        if count == 0:
            count = 1
        sim_ratio = sim / count
        # phonatics ratio and total similarity ratio
        if psim > 0:
            psim_ratio = psim / count2
            total_ratio = (dist_ratio + sim_ratio + psim_ratio) / 3
        else:
            total_ratio = (dist_ratio + sim_ratio) / 2

        # dictionary for each name and its ratio
        name_list_scores[source] = round(total_ratio, 2)

    return name_list_scores


def NameMatching(name):
    """

            Parameters
                [name: the name to be checked if exists or there are matching names]
            ----------

            Returns
            -------
                [True or sorted_sim_scores : True if it's a perfect match, sorted_sim_scores if there is no perfect match ]
    """
    # list of names
    namelist = ['احمد مصطفي عمر', 'احمد علي عمر', 'احمد عادل عمر', 'محمد احمد احمد', 'محمد علي احمد', 'محمد احمد سيد',
                'مصطفي هادي عبد العال', 'مصطفي محمد كمال', 'مصطفي فوزي محمد', 'حسين سيد رزق', 'حسين احمد رزق',
                'حسين متولي رزق', 'عبد الرحمان محمد جمال', 'عبد الرحمان راتب جمال', 'عبد الرحمان محمد محسن',
                'اسماء سعد الدين', 'اسماء احمد عبدالله', 'اسماء محمد سليم', 'راندا خالد عبد العزيز',
                'راندا محمد عبد العزيز', 'راندا وائل عبد العزيز', 'بسنت شوقي محمد', 'بسنت محمد محمد',
                'بسنت عادل عبدالله', 'محمد علي علي', 'محمد عصام خليل', 'سمير وليام']
    # check language and translates it if English
    if name.isascii():
        translator = Translator(from_lang="english", to_lang="arabic")
        name = translator.translate(name)
    # check the name existence in namelist "perfect match"
    if name in namelist:
        return True
    # compute the min edit distance and only save whose ratio is >=0.53 & sort them desc in a dictionary
    else:
        sim_scores = similarity(namelist, name)
        matching_names = {}
        for k, val in sim_scores.items():
            if val >= 0.53:
                matching_names[k] = val

        sorted_sim_scores = dict(sorted(matching_names.items(), key=operator.itemgetter(1), reverse=True))
    return sorted_sim_scores


# input the name
name = input()

# matching name
print(NameMatching(name))
