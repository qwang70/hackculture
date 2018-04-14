from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join
import pandas as pd

# constant
html_folder = "./html/" 
csv_folder = "./csv/" 
year = "13-14-Graybook/"
html_path = html_folder + year
csv_path = csv_folder + year
html_files = [f for f in listdir(html_path) if isfile(join(html_path, f)) \
             and "html" in f and "TOC" not in f]
titlesToInclude = [
   "ASSOC PROF UNIV LIBRARY",
   "ASST PROF (CT)",
   "ASST PROF UNIV LIBRARY",
   "PROF (CT)",
   "JL DOOB RES ASST PROF",
   "VST LECTURER",
   "ASSOC PROF (CT)",
   "RES PROF",
   "VST CLIN ASST PROF",
   "VST ASST PROF",
   "ASST DEAN",
   "SR LECTURER",
   "RES ASSOC PROF",
   "RES SCI",
   "ASST PROF (RT)",
   "CLIN PROF",
   "DEAN",
   "VST RES ASST PROF",
   "SR RES SCI",
   "ASSOC PROF (RT)",
   "PROF (RT)",
   "CLIN ASSOC PROF",
   "ASSOC DIR",
   "RES ASST PROF",
   "CLIN ASST PROF",
   "POSTDOC RES ASSOC",
   "LECTURER",
   "ASST PROF",
   "ASSOC PROF",
   "PROF"]
tenure_dict = {
    "": "No Info",
    "A": "Indefinite Tenure",
    "M": "Multi-Year Contract Agreement",
    "N": "Initial/Partial Term",
    "P": "Probationary Term",
    "Q": "Specified Term Appointment",
    "T": "Terminal Contract",
    "W": "Special"
}
labels = ["College", "Campus", "Department", "EmployeeName", "JobTitle", "Tenure",  "Salary"]
Urbana = ["KL", "KY", "LD", "NQ", "LT", "LN", "NA", "NT", "KM", "KT", "NU",\
         "KW", "KN", "MY", "KP", "NN", "KR", "KS", "LQ", "KU", "KV", "LB", \
         "NS", "NB", "LM", "NH", "LF", "LP", "LG", "LL", "NC", "LR", "NJ", \
         "LC", "NP", "NE", "NK", "JH", "LE"]
Chicago = ["JV", "GF", "FR", "JY", "FL", "JP", "JA", "FZ", "GA", "FV", "GE", "GC", \
          "GS", "FN", "FM", "FP", "FQ", "JM", "FS", "JD", "GH", "GT", "JT", "FT", \
          "GQ", "FW", "JS", "FX", "JB", "JU", "FY", "GL", "JK", "GN", "JL", "GP", \
          "HY", "JW", "JE", "JX", "JC", "JJ", "JF"]
Springfield = ["SC", "SG", "PE", "PL", "SA", "PG", "SF", "PJ", "PH", "SB", "PF", "SE", "PK"]
System = ["AF", "AE", "AC", "AG", "AH", "AA", "AR", "AM", "AD", "AN", "AP", "AQ", "AJ"]

# help function
def get_salary(dollar):
    d,c = dollar[1:].split('.')
    d = int(d.replace(',',''))
    c = int(c)
    return d + c*0.01

def get_campus(code):
    if code in Urbana:
        curr_campus = "Urbana-Champaign"
    elif code in Chicago:
        curr_campus = "Chicago"
    elif code in Springfield:
        curr_campus = "Springfield"
    elif code in System:
        curr_campus = "System"
    else:
        raise ValueError(code + " not in any list. need check")
    return curr_campus


employees = []
for html_file in html_files:
    with open(html_path + html_file) as fp:
        print("html file", html_file)
        soup = BeautifulSoup(fp, "html5lib")

        # initialize employee
        curr_dep = ''
        curr_employee = ''
        # get current campus
        code = html_file[:2]
        curr_campus = get_campus(code)
        # get college name
        college_col = soup.find("table").tbody.tr
        college = college_col.get_text(strip=True)
        college = college.split(" - ")[1]
        # get the next row
        curr_row = college_col.find_next_sibling("tr")
        while(curr_row):
            if len(curr_row.get_text(strip=True)) == 0:
                print(len(curr_row.get_text(strip=True)))
            elif curr_row.find("td") is None:
                curr_dep = curr_row.find("th").get_text(strip=True)
                curr_dep = curr_dep.split(" - ")[1]
                print(curr_dep)
            elif not curr_row.find("th") or\
                "Employee Total for All Jobs..." \
                not in curr_row.find("th").get_text(strip=True):
                # if the row indicate a new imployee
                if curr_row.find("th"):
                    curr_employee = curr_row.find("th").get_text(strip=True)
                # extract column information
                employee_info = curr_row.find_all("td")
                job_title = employee_info[0].get_text(strip=True)
                tenure = employee_info[1].get_text(strip=True)
                tenure = tenure_dict[tenure]
                fte = float(employee_info[4].get_text(strip=True))
                salary = get_salary(employee_info[5].get_text(strip=True))

                # if Proposed FTE is 1, which means full time
                # TODO: can be determined later
                if fte == 1 and job_title in titlesToInclude:
                    new_employee =  (college, curr_campus, curr_dep, curr_employee, job_title, tenure, salary) 
                    employees.append(new_employee)
            curr_row = curr_row.find_next_sibling("tr")
        # list to dataframe
df = pd.DataFrame.from_records(employees, columns=labels)                

# output csv
output_file = csv_path +  "employee.csv"
print(output_file)
df.to_csv(output_file)



