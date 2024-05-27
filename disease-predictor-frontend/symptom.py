symptom_list = ['abdominal pain', 'abnormal menstruation', 'acidity', 'acute liver failure', 'altered sensorium', 'anxiety', 'back pain', 'belly pain', 'blackheads',
                'bladder discomfort', 'blister', 'blood in sputum', 'bloody stool', 'blurred and distorted vision', 'breathlessness', 'brittle nails', 'bruising',
                'burning micturition', 'chest pain', 'chills', 'cold hands and feets', 'coma', 'congestion', 'constipation', 'continuous feel of urine',
                'continuous sneezing', 'cough', 'cramps', 'dark urine', 'dehydration', 'depression', 'diarrhoea', 'dischromic  patches', 'distention of abdomen',
                'dizziness', 'drying and tingling lips', 'enlarged thyroid', 'excessive hunger', 'extra marital contacts', 'family history', 'fast heart rate',
                'fatigue', 'fluid overload', 'foul smell of urine', 'headache', 'high fever', 'hip joint pain', 'history of alcohol consumption', 'increased appetite',
                'indigestion', 'inflammatory nails', 'internal itching', 'irregular sugar level', 'irritability', 'irritation in anus', 'joint pain', 'knee pain',
                'lack of concentration', 'lethargy', 'loss of appetite', 'loss of balance', 'loss of smell', 'malaise', 'mild fever', 'mood swings', 'movement stiffness',
                'mucoid sputum', 'muscle pain', 'muscle wasting', 'muscle weakness', 'nausea', 'neck pain', 'nodal skin eruptions', 'obesity', 'pain behind the eyes',
                'pain during bowel movements', 'pain in anal region', 'painful walking', 'palpitations', 'passage of gases', 'patches in throat', 'phlegm', 'polyuria',
                'prominent veins on calf', 'puffy face and eyes', 'pus filled pimples', 'receiving blood transfusion', 'receiving unsterile injections', 'red sore around nose',
                'red spots over body', 'redness of eyes', 'restlessness', 'runny nose', 'rusty sputum', 'scurring', 'shivering', 'silver like dusting', 'sinus pressure',
                'skin peeling', 'skin rash', 'slurred speech', 'small dents in nails', 'spinning movements', 'spotting  urination', 'stiff neck', 'stomach bleeding',
                'stomach pain', 'sunken eyes', 'sweating', 'swelled lymph nodes', 'swelling joints', 'swelling of stomach', 'swollen blood vessels', 'swollen extremeties',
                'swollen legs', 'throat irritation', 'toxic look (typhos)', 'ulcers on tongue', 'unsteadiness', 'visual disturbances', 'vomiting', 'watering from eyes',
                'weakness in limbs', 'weakness of one body side', 'weight gain', 'weight loss', 'yellow crust ooze', 'yellow urine', 'yellowing of eyes', 'yellowish skin',
                'itching']

def prepare_model_input(selected_elemets) :
    result = [0] * len(symptom_list)
    
    # Iterate over elements in B and set the corresponding positions in result to 1
    for element in symptom_list:
        if element in selected_elemets:
            index = symptom_list.index(element)
            result[index] = 1
    
    return result