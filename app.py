from flask import Flask, request, jsonify, render_template, redirect, url_for
import random

app = Flask(__name__)


# Stop words list (words we don't care about when scoring)
stop_words = {'the', 'a', 'and', 'in', 'of', 'when', 'is', 'by', 'to', 'for'}

# Function to filter out stop words from a list of words
def filter_stop_words(words):
    return [word for word in words if word not in stop_words]

# Updated Question Bank
question_bank = {
    1: {"question": "What is the difference between dry bulb and wet bulb temperature in data center cooling?", 
        "answer": "Dry bulb temperature measures the ambient air temperature, while wet bulb temperature accounts for humidity and is the lowest temperature air can reach through evaporation."},
    2: {"question": "What is the significance of the dew point in a data center environment?", 
        "answer": "Dew point is the temperature at which air becomes saturated and condensation begins. Maintaining the correct dew point prevents moisture from forming on sensitive equipment."},
    3: {"question": "What components are typically found in a UPS system in a data center?", 
        "answer": "A typical UPS system includes batteries, rectifiers, inverters, static bypass switches, and control systems, all working together to provide uninterruptible power to critical systems."},
    4: {"question": "What is an ATS (Automatic Transfer Switch), and what is its function in a data center?", 
        "answer": "An ATS is a device that automatically transfers power from the main source to a backup generator when the primary power source fails, ensuring continuous operation of critical equipment."},
    5: {"question": "What is dry cooling, and how is it used in data centers?", 
        "answer": "Dry cooling uses ambient air to dissipate heat without the use of water. It is often used in locations with low humidity or as part of a hybrid system to reduce water consumption."},
    6: {"question": "What role do transformers play in data center power distribution?", 
        "answer": "Transformers step down high-voltage electricity from the utility grid to lower voltages suitable for use by data center equipment."},
    7: {"question": "What is the function of circuit breakers in data centers?", 
        "answer": "Circuit breakers protect electrical circuits by interrupting power flow when an overload or fault occurs, preventing damage to equipment and ensuring safe operation."},
    8: {"question": "What is the typical sequence of power flow from the utility grid to a server rack in a data center?", 
        "answer": "The power flow typically goes from the utility grid to the switchgear, through transformers, circuit breakers, distribution panels, and PDUs, and finally to the server racks."},
    9: {"question": "What are the main components of a server in a data center?", 
        "answer": "A typical server consists of a CPU, memory, storage drives, network interface cards, power supply, and cooling systems. Together, these components process, store, and transmit data."},
    10: {"question": "How does humidity affect the operation of a data center, and what levels are typically maintained?", 
        "answer": "High humidity can cause condensation, while low humidity can lead to electrostatic discharge. Data centers typically maintain humidity levels between 40% and 60%."},
    11: {"question": "What is the purpose of a Remote Power Panel (RPP) in a data center?", 
        "answer": "An RPP extends power distribution from the PDU to server racks, allowing for additional circuit breakers and the distribution of electrical power closer to the load."},
    12: {"question": "What is a modular data center, and what are its advantages?", 
        "answer": "A modular data center is a prefabricated unit that includes power, cooling, and IT infrastructure. Its advantages include rapid deployment, scalability, and flexibility."},
    13: {"question": "What is the primary function of air economizers in data center cooling systems?", 
        "answer": "Air economizers use outside air to cool the data center when environmental conditions are favorable, reducing reliance on mechanical cooling."},
    14: {"question": "What is the function of fuses in a data center's electrical system?", 
        "answer": "Fuses protect electrical circuits by breaking the circuit if the current exceeds a certain threshold, preventing damage to equipment and minimizing fire hazards."},
    15: {"question": "What is the role of switchgear in a data center's power infrastructure?", 
        "answer": "Switchgear controls, protects, and isolates electrical equipment in the power distribution system, enabling safe maintenance and ensuring power reliability."},
    16: {"question": "How does airflow management contribute to data center cooling efficiency?", 
        "answer": "Airflow management, such as hot aisle/cold aisle containment, prevents the mixing of hot and cold air, improving cooling efficiency and reducing the workload on cooling systems."},
    17: {"question": "What is a battery monitoring system, and why is it important in data centers?", 
        "answer": "A battery monitoring system tracks the health and performance of UPS batteries, providing real-time data to ensure they are ready to supply power during outages."},
    18: {"question": "What is the difference between AC and DC power distribution in data centers?", 
        "answer": "AC is the standard power distribution method, while DC is sometimes used for its efficiency in reducing conversion losses and simplifying power distribution."},
    19: {"question": "What is the role of a chiller in a water-cooled data center?", 
        "answer": "A chiller removes heat from the data center by cooling water or a refrigerant that is circulated through cooling systems, ensuring optimal operating temperatures for IT equipment."},
    20: {"question": "How does a fire suppression system work in a data center, and what types are commonly used?", 
        "answer": "Fire suppression systems detect and extinguish fires without damaging sensitive equipment. Common types include gas-based and water mist systems."},
    21: {"question": "What is ESD (Electrostatic Discharge), and how is it prevented in data centers?", 
        "answer": "ESD occurs when static electricity discharges into sensitive electronic components, potentially causing damage. It is prevented through humidity control and antistatic materials."},
    22: {"question": "What is the significance of power factor correction in data centers?", 
        "answer": "Power factor correction improves the efficiency of power usage by reducing the amount of reactive power, lowering electricity costs and minimizing transmission losses."},
    23: {"question": "What is the function of a surge protector in a data center?", 
        "answer": "A surge protector safeguards equipment from voltage spikes by diverting excess electrical energy to ground, protecting servers and other sensitive components from damage."},
    24: {"question": "What is the difference between a diesel and a natural gas generator in data center applications?", 
        "answer": "Diesel generators are fast and reliable for backup power, while natural gas generators offer cleaner emissions and longer runtime capabilities."},
    25: {"question": "What is the purpose of dehumidification in a data center's HVAC system?", 
        "answer": "Dehumidification reduces excess moisture in the air, preventing condensation from forming on sensitive equipment and reducing the risk of hardware failure."}
}

@app.route('/')
def home():
    question_id = random.choice(list(question_bank.keys()))
    question = question_bank[question_id]["question"]
    return render_template('index.html', question=question, question_id=question_id)

@app.route('/submit', methods=['POST'])
def submit():
    question_id = int(request.form['question_id'])
    user_answer = request.form['answer'].lower().split()
    correct_answer = question_bank[question_id]["answer"].split()

    # Filter out stop words from the user's answer
    filtered_user_answer = filter_stop_words(user_answer)

    score = 0
    result_display = []

    # Check each word in the correct answer and highlight if it was in the user answer
    for word in correct_answer:
        if word.lower() in filtered_user_answer:
            result_display.append(f'<span style="color:green;">{word}</span>')
            score += 1
        else:
            result_display.append(word)

    total_keywords = len(filter_stop_words(correct_answer))
    
    # Return the result with colored words
    result_html = " ".join(result_display)
    
    return render_template('result.html', score=score, total=total_keywords, correct_answer=result_html)

@app.route('/ask_another')
def ask_another():
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
