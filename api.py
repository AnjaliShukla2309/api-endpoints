from flask import Flask, jsonify, request

app = Flask(__name__)

doctors = [
    {
        'id': 1,
        'name': 'Dr. Misha',
        'schedule': {
            'Monday': '5:00 PM - 9:00 PM',
            'Tuesday': '5:00 PM - 9:00 PM',
            'Wednesday': '5:00 PM - 9:00 PM',
            'Thursday': '5:00 PM - 9:00 PM',
            'Friday': '5:00 PM - 9:00 PM',
            'Saturday': '5:00 PM - 9:00 PM',
            'Sunday': "Holiday"
        },
        'location': 'KIMS Hospital, kondapur, Hyderabad',
        'appointments' : [],
        'max_appointments' : 10
    },
    {
        'id': 2,
        'name': 'Dr. Reddy',
        'schedule': {
            'Monday': '5:00 PM - 9:00 PM',
            'Tuesday': '5:00 PM - 9:00 PM',
            'Wednesday': '5:00 PM - 9:00 PM',
            'Thursday': '5:00 PM - 9:00 PM',
            'Friday': '5:00 PM - 9:00 PM',
            'Saturday': '5:00 PM - 9:00 PM',
            'Sunday': "Holiday"
        },
        'location': 'KIMS Hospital, kondapur, Hyderabad',
        'appointments' : [],
        'max_appointments' : 10
    }
]

maxResponse = [{"result" : "Reached maximum numbers of appointments."}]

@app.route('/doctors', methods=['GET'])
def get_doctors():
    return jsonify(doctors)

@app.route('/doctors/<int:id>', methods=['GET'])
def get_doctor(id):
    doctor = [doctor for doctor in doctors if doctor['id'] == id]
    if len(doctor) == 0:
        return jsonify({"result": "Please enter correct doctor id"}), 400
    return jsonify(doctor[0])

@app.route('/appointments', methods=['GET'])
def get_appointment():
    return jsonify(doctors)

@app.route('/appointments/<int:id>', methods=['GET'])
def get_appointments(id):
    doctor = [doctor for doctor in doctors if doctor['id'] == id]
    if len(doctor) == 0:
        return jsonify({"result": "Please enter correct doctor id to fetch appointment details"}), 400
    return jsonify(doctor[0]['appointments'])

@app.route('/appointments', methods=['POST'])
def create_appointment():
    if not request.json or not 'doctor_id' in request.json or not \
       'patient_name' in request.json or not \
       'appointment_time' in request.json:
        return jsonify({"result" : "Please pass all the required parameters : doctor_id, patient_name, and appointment_time"}),400
    doctor = [doctor for doctor in doctors if doctor['id'] == request.json['doctor_id']]
    if len(doctor) == 0:
        return ({"result" : "Please enter correct doctor id"}),400

    appointments = doctor[0]["appointments"]

    if len([appointment for appointment in appointments if appointment['doctor_id'] == request.json['doctor_id']]) >= doctor[0]['max_appointments']:
        return jsonify(maxResponse), 400

    new_appointment = {
        'appointment_id': appointments[-1]['appointment_id'] + 1 if len(doctor[0]['appointments']) > 0 else 1,
        'patient_name': request.json['patient_name'],
        'doctor_id' : request.json['doctor_id'],
        'appointment_time': request.json['appointment_time']
    }
    doctor[0]['appointments'].append(new_appointment)
    new_appointment["status"] = "appointment created successfully."
    return jsonify(new_appointment), 201
if __name__ == '__main__':
    app.run(debug=True)