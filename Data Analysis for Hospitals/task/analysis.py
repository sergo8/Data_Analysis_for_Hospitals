import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', 8)

# Read files
general = pd.read_csv('test/general.csv')
prenatal = pd.read_csv('test/prenatal.csv')
sports = pd.read_csv('test/sports.csv')

# Assignment of the same column names
prenatal.columns = general.columns.values
sports.columns = general.columns.values

# Concatenation of tables
concatenated = pd.concat([general, prenatal, sports], ignore_index=True)

# Deleting of column: 'Unnamed: 0'
concatenated.drop(columns='Unnamed: 0', inplace=True)
concatenated.dropna(axis=0, thresh=1, inplace=True)


# function to use in the aggregation
def replace_gender(gender):
    if gender == 'female' or gender == 'woman':
        return 'f'
    elif gender == 'male' or gender == 'man':
        return 'm'


# replace all genders to one universal type: "m"/"f"
concatenated.gender = concatenated.gender.aggregate(replace_gender)
concatenated.loc[concatenated.hospital == 'prenatal', 'gender'] = 'f'

# fill all NaN with numeric 0
concatenated.fillna(0, inplace=True)

# Question 1:
hospital = concatenated.hospital.value_counts().idxmax()

# Question 2:
fraction_of_stomach = concatenated.loc[concatenated.hospital == 'general', 'diagnosis'].value_counts() / \
         concatenated.loc[concatenated.hospital == 'general', 'diagnosis'].count()
fraction_of_stomach = round(fraction_of_stomach['stomach'], 3)

# Question 3:
fraction_from_sports = concatenated.loc[concatenated.hospital == 'sports', 'diagnosis'].value_counts() / \
         concatenated.loc[concatenated.hospital == 'sports', 'diagnosis'].count()
fraction_from_sports = round(fraction_from_sports['dislocation'], 3)

# Question 4:
median_age_table = concatenated.pivot_table(columns='hospital', values='age')
median_age_diff = round(median_age_table['general'] - median_age_table['sports'], 1)[0]

# Question 5:
blood_test = concatenated.pivot_table(index='hospital', columns='blood_test', aggfunc='count').age
blood_test.fillna(0, inplace=True)

max_num_of_tests = round(blood_test.t.max())
row_id_max = blood_test.t.idxmax()

# print(f"""The answer to the 1st question is {hospital}
# The answer to the 2nd question is {fraction_of_stomach}
# The answer to the 3rd question is {fraction_from_sports}
# The answer to the 4th question is {median_age_diff}
# The answer to the 5th question is {row_id_max}, {max_num_of_tests} blood tests""")
#
# Select list of ages
age_list = concatenated['age'].tolist()
# Build histogram
bins = [0, 15, 35, 55, 70, 80]
plt.figure(1)
plt.hist(age_list, edgecolor="black", bins=bins)
plt.title("Patient's age")
plt.ylabel("Number of people")
plt.xlabel("Age")
#
# plt.show()
#

# Select list of diagnoses
diagnoses_list = concatenated['diagnosis'].value_counts().values
labels = concatenated['diagnosis'].value_counts().index.values
# Build pie chart
plt.figure(2)
plt.pie(diagnoses_list, autopct='%.1f%%', shadow=True, startangle=0)
plt.legend(labels)
#
# plt.show()

# Select lists of heights per hospital
height_general = concatenated.loc[concatenated.hospital == 'general', 'height'].values
height_sports = concatenated.loc[concatenated.hospital == 'sports', 'height'].values
height_prenatal = concatenated.loc[concatenated.hospital == 'prenatal', 'height'].values

data = [height_general, height_sports, height_prenatal]
# Build violin chart
plt.figure(3)
plt.violinplot(data)


plt.show()

print(f"""The answer to the 1st question: 15 - 35
The answer to the 2nd question: pregnancy
The answer to the 3rd question: It's because different measurement systems""")