from __future__ import print_function, unicode_literals
from bs4 import BeautifulSoup
import sys
import re
import requests
import traceback
from PyInquirer import style_from_dict, Token, prompt, Validator, ValidationError

style = style_from_dict({
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#673AB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#2196f3 bold',
    Token.Question: '',
})

internship_types = {
  '.NET Development': '.net%20development',
  '3D Printing': '3d%20printing',
  'Accounts': 'accounts',
                    'Acting': 'acting',
                    'Aerospace Engineering': 'aerospace%20engineering',
                    'Agriculture & Food Engineering': 'agriculture%20and%20food%20engineering',
                    'Analytics': 'analytics',
                    'Android App Development': 'android%20app%20development',
                    'Angular.js Development': 'angular.js%20development',
                    'Animation': 'animation', 'Architecture': 'architecture',
                    'Artificial Intelligence (AI)': 'artificial%20intelligence%20(ai)',
                    'ASP.NET Development': 'asp.net',
                    'Automobile Engineering': 'automobile%20engineering',
                    'Backend Development': 'backend%20development',
                    'Big Data': 'big%20data',
                    'Bioinformatics': 'bioinformatics',
                    'Biology': 'biology',
                    'Biotechnology Engineering': 'biotechnology%20engineering',
                    'Blogging': 'blogging',
                    'Brand Management': 'brand%20management',
                    'CAD Design': 'cad%20design',
                    'Campus Ambassador': 'campus%20ambassador',
                    'Chartered Accountancy (CA)': 'chartered%20accountancy%20(ca)',
                    'Chemical Engineering': 'chemical%20engineering', 'Chemistry': 'chemistry', 'Cinematography': 'cinematography', 'Civil Engineering': 'civil', 'Client Servicing': 'client%20servicing', 'Cloud Computing': 'cloud%20computing', 'Commerce': 'commerce', 'Company Secretary (CS)': 'company%20secretary%20(cs)', 'Computer Science': 'computer%20science', 'Computer Vision': 'computer%20vision', 'Content Writing': 'content%20writing', 'Copywriting': 'copywriting', 'Creative Design': 'creative%20design', 'Creative Writing': 'creative%20writing', 'Customer Service': 'customer%20service', 'Cyber Security': 'cyber%20security', 'Data Entry': 'data%20entry', 'Data Science': 'data%20science', 'Database Building': 'database%20building', 'Design': 'design', 'Digital Marketing': 'digital%20marketing', 'Editorial': 'editorial', 'Electrical Engineering': 'electrical%20engineering', 'Electronics Engineering': 'electronics%20engineering', 'Embedded Systems': 'embedded%20systems', 'Energy Science & Engineering': 'energy%20science%20and%20engineering', 'Engineering': 'engineering', 'Engineering Design': 'engineering%20design', 'Engineering Physics': 'engineering%20physics', 'Environmental Sciences': 'environmental%20sciences', 'Event Management': 'event%20management', 'Facebook Marketing': 'facebook%20marketing', 'Fashion Design': 'fashion%20design', 'Film Making': 'film%20making', 'Finance': 'finance', 'Front End Development': 'front%20end%20development', 'Full Stack Development': 'full%20stack%20development', 'Fundraising': 'fundraising', 'Game Development': 'game%20development', 'General Management': 'general%20management', 'Government': 'government', 'Graphic Design': 'graphic%20design', 'Hospitality': 'hospitality', 'Hotel Management': 'hotel%20management', 'Human Resources (HR)': 'human%20resources%20(hr)', 'Humanities': 'humanities', 'Image Processing': 'image%20processing', 'Industrial & Production Engineering': 'industrial%20%26%20production%20engineering', 'Industrial Design': 'industrial%20design', 'Information Technology': 'information%20technology', 'Instrumentation & Control Engineering': 'instrumentation%20and%20control%20engineering', 'Interior Design': 'interior%20design', 'Internet of Things (IoT)': 'internet%20of%20things%20(iot)', 'iOS App Development': 'ios%20app%20development', 'Java Development': 'java%20development', 'Javascript Development': 'javascript%20development', 'Journalism': 'journalism', 'Law': 'law', 'Legal Research': 'legal%20research', 'Machine Learning': 'machine%20learning', 'Magento Development': 'magento%20development', 'Manufacturing Engineering': 'manufacturing%20engineering', 'Market/Business Research': 'market%2Fbusiness%20research', 'Marketing': 'marketing', 'Material Science': 'material%20science', 'Mathematics': 'mathematics', 'Mathematics & Computing': 'mathematics%20and%20computing', 'MBA': 'mba', 'Mechanical Engineering': 'mechanical%20engineering', 'Mechatronics': 'mechatronics', 'Media': 'media', 'Medicine': 'medicine', 'Merchandise Design': 'merchandise%20design', 'Metallurgical Engineering': 'metallurgical%20engineering', 'Mobile App Development': 'mobile%20app%20development', 'Motion Graphics': 'motion%20graphics', 'Naval Architecture and Ocean Engineeering': 'naval%20architecture%20and%20ocean%20engineeering', 'Network Engineering': 'network%20engineering', 'NGO': 'ngo', 'Node.js Development': 'node.js%20development', 'Operations': 'operations', 'Pharmaceutical': 'pharmaceutical', 'Photography': 'photography', 'PHP Development': 'php%20development', 'Physics':
                    'physics', 'Political/Economics/Policy Research': 'political%2Feconomics%2Fpolicy%20research', 'Public Relations (PR)': 'public%20relations%20(pr)', 'Product Management': 'product%20management', 'Programming': 'programming', 'Psychology': 'psychology', 'Python/Django Development': 'python%2Fdjango%20development', 'Recruitment': 'recruitment', 'Robotics': 'robotics', 'Ruby on Rails': 'ruby%20on%20rails', 'Sales': 'sales', 'Science': 'science', 'Search Engine Optimization (SEO)': 'search%20engine%20optimization%20(seo)', 'Social Media Marketing': 'social%20media%20marketing', 'Social Work': 'social%20work', 'Software Development': 'software%20development', 'Software Testing': 'software%20testing', 'Statistics': 'statistics', 'Strategy': 'strategy', 'Supply Chain Management (SCM)': 'supply%20chain%20management%20(scm)', 'Talent Acquisition': 'talent%20acquisition', 'Teaching': 'teaching', 'Telecalling': 'telecalling', 'Travel & Tourism': 'travel%20and%20tourism', 'UI/UX Design': 'ui%2Fux%20design', 'Video Making/Editing': 'video%20making%2Fediting', 'Videography': 'videography', 'Volunteering': 'volunteering', 'Web Development':
                    'web%20development', 'Wordpress Development': 'wordpress%20development'}

locations = {
    'Agra': 'in-agra', 'Ahmedabad': 'in-ahmedabad', 'Ahmednagar': 'in-ahmednagar', 'Ajmer': 'in-ajmer', 'Akola': 'in-akola', 'Akurdi':
    'in-akurdi', 'Alibag': 'in-alibag', 'Aligarh': 'in-aligarh', 'Allahabad': 'in-allahabad', 'Alwal': 'in-alwal', 'Alwar': 'in-alwar',
    'Ambala': 'in-ambala', 'Ambala Cantt': 'in-ambala%20cantt', 'Ameerpet': 'in-ameerpet', 'Amravati': 'in-amravati', 'Amritsar': 'in-amritsar', 'Amroha': 'in-amroha', 'Anand': 'in-anand', 'Assam': 'in-assam', 'Aurangabad': 'in-aurangabad', 'Ayyalur': 'in-ayyalur', 'Badarpur': 'in-badarpur', 'Bangalore': 'in-bangalore', 'Banglore':
    'in-banglore', 'Bardhaman': 'in-bardhaman', 'Bathinda': 'in-bathinda', 'Beed': 'in-beed', 'Begumpet': 'in-begumpet', 'Belgharia': 'in-belgharia', 'Bhopal': 'in-bhopal', 'Bhubaneswar': 'in-bhubaneswar', 'Bidhannagar': 'in-bidhannagar', 'Bihar': 'in-bihar', 'Bijapur': 'in-bijapur', 'Bilaspur': 'in-bilaspur', 'Bokaro': 'in-bokaro', 'Bokaro Steel City': 'in-bokaro%20steel%20city', 'Borivali': 'in-borivali', 'California City': 'in-california%20city', 'Central': 'in-central', 'Chakan': 'in-chakan', 'Chamoli': 'in-chamoli', 'Chandannagar': 'in-chandannagar', 'Chandigarh': 'in-chandigarh', 'Chandrapur': 'in-chandrapur', 'Chandrasekharpur': 'in-chandrasekharpur', 'Chennai': 'in-chennai', 'Chicago': 'in-chicago', 'Chinchwadgaon': 'in-chinchwadgaon', 'Chinnalapatti': 'in-chinnalapatti', 'Chittoor': 'in-chittoor', 'Chomu': 'in-chomu', 'Cochin': 'in-cochin',
    'Coimbatore': 'in-coimbatore', 'Coimbatore North': 'in-coimbatore%20north', 'Cook County': 'in-cook%20county', 'Cumbum': 'in-cumbum', 'Dahisar': 'in-dahisar', 'Dakshin Dinajpur': 'in-dakshin%20dinajpur', 'Dakshina Kannada': 'in-dakshina%20kannada', 'Darmstadt': 'in-darmstadt', 'Dehradun': 'in-dehradun', 'Delhi': 'in-delhi', 'Dera Bassi': 'in-dera%20bassi', 'Dewas': 'in-dewas', 'Dhanbad': 'in-dhanbad', 'Dindigul': 'in-dindigul', "District D'Ernakulam": 'in-district%20d%27ernakulam', 'District De Bangalore Urbain': 'in-district%20de%20bangalore%20urbain', 'Dombivli': 'in-dombivli', 'Dr. Ambedkar Nagar': 'in-dr.%20ambedkar%20nagar', 'Dubai': 'in-dubai', 'Durgapur': 'in-durgapur', 'Dwarka': 'in-dwarka', 'East Godavari':
    'in-east%20godavari', 'East Sikkim': 'in-east%20sikkim', 'East Singhbhum': 'in-east%20singhbhum', 'Ernakulam': 'in-ernakulam', 'Erode': 'in-erode', 'Etawah': 'in-etawah', 'Faridabad': 'in-faridabad', 'Faridkot': 'in-faridkot', 'Fazilka': 'in-fazilka', 'Ferozepur': 'in-ferozepur', 'Frankfurt': 'in-frankfurt', 'Galveston County':
    'in-galveston%20county', 'Gandhinagar': 'in-gandhinagar', 'Gandhipuram': 'in-gandhipuram', 'Gautam Buddh Nagar': 'in-gautam%20buddh%20nagar', 'Gautam Buddha Nagar': 'in-gautam%20buddha%20nagar', 'Genève': 'in-gen%C3%A8ve', 'Geneva': 'in-geneva', 'Ghaziabad': 'in-ghaziabad', 'Gondia': 'in-gondia', 'Goregaon': 'in-goregaon', 'Greater Noida': 'in-greater%20noida', 'Guntur': 'in-guntur', 'Gurdaspur': 'in-gurdaspur', 'Gurgaon': 'in-gurgaon', 'Gurgoan': 'in-gurgoan', 'Guwahati': 'in-guwahati', 'Gwalior': 'in-gwalior', 'Gwalior West': 'in-gwalior%20west', 'Haridwar': 'in-haridwar', 'Harris County': 'in-harris%20county', 'Haryana': 'in-haryana', 'Hesaraghatta': 'in-hesaraghatta', 'Hooghly': 'in-hooghly', 'Hoshiarpur': 'in-hoshiarpur', 'Houston': 'in-houston', 'Hyderabad': 'in-hyderabad', 'Indore': 'in-indore', 'Jabalpur': 'in-jabalpur', 'Jaipur': 'in-jaipur', 'Jalandhar': 'in-jalandhar', 'Jamshedpur': 'in-jamshedpur',
    'Jodhpur': 'in-jodhpur', 'Jorhat': 'in-jorhat', 'Kakinada': 'in-kakinada', 'Kalyan': 'in-kalyan', 'Kamrup': 'in-kamrup', 'Kanchipuram': 'in-kanchipuram', 'Kanpur': 'in-kanpur', 'Kapurthala': 'in-kapurthala', 'Karimnagar': 'in-karimnagar', 'Karnaprayag': 'in-karnaprayag', 'Kaushambi': 'in-kaushambi', 'Kazhakkoottam': 'in-kazhakkoottam', 'Keelung City': 'in-keelung%20city', 'Kern County': 'in-kern%20county', 'Kharar': 'in-kharar', 'Khed': 'in-khed', 'Kheda': 'in-kheda', 'Khordha': 'in-khordha', 'Klosterneuburg': 'in-klosterneuburg', 'Kochi': 'in-kochi', 'Kolhapur': 'in-kolhapur', 'Kolkata': 'in-kolkata', 'Kompally': 'in-kompally', 'Koregaon': 'in-koregaon', 'Kozhikode': 'in-kozhikode', 'Krishna': 'in-krishna', 'Kurla': 'in-kurla', 'Leh': 'in-leh', 'Lonavala': 'in-lonavala', 'Lucknow': 'in-lucknow', 'Ludhiana': 'in-ludhiana', 'Madhapur': 'in-madhapur', 'Madurai': 'in-madurai', 'Malad': 'in-malad', 'Mandi': 'in-mandi', 'Mangalore': 'in-mangalore', 'Mangaluru': 'in-mangaluru', 'Medak': 'in-medak', 'Mehsana': 'in-mehsana', 'Mira Bhayandar': 'in-mira%20bhayandar', 'Mohali': 'in-mohali', 'Moradabad': 'in-moradabad', 'Mumbai': 'in-mumbai', 'Mysuru': 'in-mysuru', 'Nadiad': 'in-nadiad', 'Nagpur': 'in-nagpur', 'Nainital': 'in-nainital', 'Nalgonda': 'in-nalgonda', 'Namakkal': 'in-namakkal', 'Nanded': 'in-nanded', 'Nashik': 'in-nashik', 'Natham': 'in-natham', 'Navi Mumbai': 'in-navi%20mumbai', 'Navsari': 'in-navsari', 'Nayagarh': 'in-nayagarh', 'Neemrana': 'in-neemrana', 'New Town': 'in-new%20town', 'New York': 'in-new%20york', 'Nilakottai': 'in-nilakottai', 'Noida': 'in-noida', 'North 24 Parganas': 'in-north%2024%20parganas', 'North East Delhi': 'in-north%20east%20delhi', 'North West Delhi': 'in-north%20west%20delhi', 'Palakkad': 'in-palakkad', 'Palghar': 'in-palghar', 'Panchkula': 'in-panchkula', 'Panipat': 'in-panipat', 'Pashchim Champaran': 'in-pashchim%20champaran', 'Pataudi': 'in-pataudi', 'Pathankot': 'in-pathankot', 'Patiala': 'in-patiala', 'Patna': 'in-patna', 'Periyakulam': 'in-periyakulam', 'Pimpri-Chinchwad': 'in-pimpri-chinchwad', 'Pollachi': 'in-pollachi', 'Pondicherry': 'in-pondicherry', 'Puducherry': 'in-puducherry', 'Pune': 'in-pune', 'Raigad': 'in-raigad', 'Raipur': 'in-raipur', 'Rajahmundry': 'in-rajahmundry', 'Rajajinagar': 'in-rajajinagar', 'Rajkot': 'in-rajkot', 'Rajpura': 'in-rajpura', 'Ramprastha': 'in-ramprastha', 'Ranchi': 'in-ranchi', 'Ranga Reddy': 'in-ranga%20reddy', 'Ratlam': 'in-ratlam', 'Ratnagiri': 'in-ratnagiri', 'Rewari': 'in-rewari', 'Roopnagar': 'in-roopnagar', 'Rourkela': 'in-rourkela', 'Sahibzada Ajit Singh Nagar': 'in-sahibzada%20ajit%20singh%20nagar', 'Salem': 'in-salem', 'San Francisco': 'in-san%20francisco', 'San Francisco County': 'in-san%20francisco%20county', 'Sangrur': 'in-sangrur', 'Satara': 'in-satara', 'Sathyamangalam': 'in-sathyamangalam', 'Savli': 'in-savli', 'Secunderabad': 'in-secunderabad', 'Shahdara': 'in-shahdara', 'Shimla': 'in-shimla', 'Sikar': 'in-sikar', 'Singapore': 'in-singapore', 'Solan': 'in-solan', 'Solapur': 'in-solapur', 'Sonepat': 'in-sonepat', 'Sonipat': 'in-sonipat', 'South West Delhi': 'in-south%20west%20delhi', 'Sundargarh': 'in-sundargarh', 'Surat': 'in-surat', 'Texas City': 'in-texas%20city', 'Thane': 'in-thane', 'Theni': 'in-theni', 'Thiruvananthapuram': 'in-thiruvananthapuram',
    'Tiruchirappalli': 'in-tiruchirappalli', 'Tirunelveli': 'in-tirunelveli', 'Tirupati': 'in-tirupati', 'Tiruppur': 'in-tiruppur', 'Tiruvallur': 'in-tiruvallur', 'Udaipur': 'in-udaipur', 'Ujjain': 'in-ujjain', 'Uppal': 'in-uppal', 'Vadamadurai': 'in-vadamadurai', 'Vadodara': 'in-vadodara', 'Varanasi': 'in-varanasi', 'Vasai Road': 'in-vasai%20road', 'Vasai-Virar': 'in-vasai-virar', 'Vashi': 'in-vashi', 'Vashi Navi Mumbai': 'in-vashi%20navi%20mumbai', 'Vellore':
    'in-vellore', 'Vijayawada': 'in-vijayawada', 'Visakhapatnam': 'in-visakhapatnam', 'Vishakhapatnam': 'in-vishakhapatnam', 'Wakad': 'in-wakad', 'Wardha': 'in-wardha', 'Wien-Umgebung District': 'in-wien-umgebung%20district', 'Zürich District': 'in-z%C3%BCrich%20district', 'Zirakpur': 'in-zirakpur', 'Zurich': 'in-zurich'
    }


class NumberValidator(Validator):
    def validate(self, document):
        try:
            if int(document.text) >= 1000:
                return True
            else:
                raise ValidationError(
                    message="The value is too low!",
                    cursor_position=len(document.text)
                )
        except ValueError:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(document.text))  # Move cursor to end

class IntValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(document.text))  # Move cursor to end

def search(type, threshold, loc, remote, pages = 11):
    stipend_threshold = int(threshold)
    location = "-" + locations[loc] if loc != '' else ''
    internship_type = internship_types[type]
    file1 = open(type + ' Internships.txt', 'w+')
    file1.truncate(0)
    baseURL = ''
    if remote is False:
        file1.write('Internships with stipend greater than Rs. ' +
                    str(stipend_threshold) + " in " + loc + '\n\n')
        print("Finding " + type + " internships with stipend greater than " +
            str(stipend_threshold)+"...")
        baseURL = "https://internshala.com/internships/" + \
            internship_type + "-internship" + location
    else:
        file1.write('### Internships remote with stipend greater than Rs. ' +
                    str(stipend_threshold) + '\n\n')
        print("Finding " + type + " remote internships with stipend greater than " +
            str(stipend_threshold)+"...")
        baseURL = "https://internshala.com/internships/" + "work-from-home-" + internship_type + "-jobs" 
    i = 0
    for p in range(1, pages):
        url = baseURL + "/page-" + str(p)
        r = requests.get(url)
        doc = BeautifulSoup(r.text, "html.parser")
        internships = doc.select(".individual_internship")
        for iship in internships:
            try:
                header = iship.select(".individual_internship_header")[0]
                details = iship.select(".individual_internship_details")[0]
                title = header.select("h4")[0]['title']
                link = 'https://internshala.com' + \
                    header.select("a")[0]['href']
                stipend = details.select(".stipend_container_table_cell")[0]
                limit = stipend.text.find("/")
                amount = stipend.text[:limit-1].strip()
                m = re.match("\n*\d*(-)\d*", amount)
                if m is not None:
                    if int(amount[:m.start(1)]) >= stipend_threshold:
                        i = i + 1
                        file1.write(str(i) + ". Title: " + str(title) + "\nLink: " +
                                    str(link) + "\n Stipend starts from: Rs." + str((amount).strip()) + "\n")
                elif amount.strip() != "Unpaid" or amount.strip() != "Not Provided":
                    amount = amount.replace("Lump-Sum", '').replace("\n", '')
                    if int(amount) >= stipend_threshold:
                        i = i + 1
                        file1.write(str(i) + ". Title: " + str(title) + "\nLink: " +
                                    str(link) + "\n Stipend: Rs." + str((amount).strip()) + "\n")
            except Exception as e:
                traceback.format_exception(*sys.exc_info())
                continue
        sys.stdout.write("\rPage "+str(p) + " complete...")
        sys.stdout.flush()

    file1.close()
    print("\nDone!")


def main():
    print('Search for internships from Internshala ©:')
    print("------------------------------------------")
    questions = [
        {
            'type': 'input',
            'name': 'stipend',
            'message': 'What\'s minimum stipend to look for (Rs.)?',
            'validate': NumberValidator,
        },
        {
            'type': 'list',
            'name': 'category',
            'message': 'Category:',
            'choices': internship_types.keys(),
        },
        {
            'type': 'confirm',
            'name': 'remoteConfirm',
            'message': 'Do you want to look for a work-from-home internship?',
            'default': False
        },
        {
            "type": "confirm",
            "name": "locationConfirm",
            "message": "Do you want to select a location?",
            "default": False,
            'when': lambda answers: answers['remoteConfirm'] == False
        },
        {
            'type': 'list',
            'name': 'location',
            'message': 'Select a specific location:',
            'choices': locations.keys(),
            'when': lambda answers: "locationConfirm" in answers and answers['locationConfirm'] != False
        },
         {
            'type': 'input',
            'name': 'pages',
            'message': 'How many to search for (in terms of Internshala result pages)?',
            'validate': IntValidator,
        },
    ]
    answers = prompt(questions, style=style)
    category = answers['category'] if answers['category'] else 'Computer Science'
    threshold = answers['stipend'] if answers['stipend'] else 10000
    remote = answers['remoteConfirm'] if answers['remoteConfirm'] else False
    loc = None
    # loc = answers['location'] if answers['location'] else ''
    pages = int(answers['pages']) if answers['pages'] else 10
    # try:
    #     category = answers['category']
    # except KeyError:
    #     category = 'Computer Science'

    # try:
    #     threshold = answers['stipend']
    # except KeyError:
    #     threshold = 10000

    try:
        loc = answers['location']
    except KeyError:
        loc = ''

    search(category, threshold, loc, remote, pages + 1)


if __name__ == "__main__":
    main()
