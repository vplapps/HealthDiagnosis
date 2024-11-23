from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import datetime

app = Flask(__name__)

# Налаштування для PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@34.44.101.138:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель бази даних
class HealthData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    temperature = db.Column(db.Float, nullable=False)
    pressure = db.Column(db.Integer, nullable=False)
    pulse = db.Column(db.Integer, nullable=False)
    spo2 = db.Column(db.Integer, nullable=False)
    risk_level = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


# Ініціалізація бази даних
with app.app_context():
    db.create_all()

# Нечітка логіка
def fuzzy_diagnose(temp, pressure, pulse, spo2):
    # Вхідні змінні
    temperature = ctrl.Antecedent(np.arange(35, 41, 0.1), 'temperature')
    blood_pressure = ctrl.Antecedent(np.arange(80, 181, 1), 'blood_pressure')
    heart_rate = ctrl.Antecedent(np.arange(40, 141, 1), 'heart_rate')
    oxygen_level = ctrl.Antecedent(np.arange(70, 101, 1), 'oxygen_level')

    # Вихідна змінна
    risk = ctrl.Consequent(np.arange(0, 101, 1), 'risk')

    # Функції приналежності
    temperature['low'] = fuzz.trapmf(temperature.universe, [35, 35, 36.5, 37])
    temperature['normal'] = fuzz.trimf(temperature.universe, [36.5, 37, 37.5])
    temperature['high'] = fuzz.trapmf(temperature.universe, [37.5, 38, 40, 40])

    blood_pressure['low'] = fuzz.trapmf(blood_pressure.universe, [80, 80, 90, 100])
    blood_pressure['normal'] = fuzz.trimf(blood_pressure.universe, [90, 120, 140])
    blood_pressure['high'] = fuzz.trapmf(blood_pressure.universe, [130, 150, 180, 180])

    heart_rate['slow'] = fuzz.trapmf(heart_rate.universe, [40, 40, 60, 70])
    heart_rate['normal'] = fuzz.trimf(heart_rate.universe, [60, 75, 90])
    heart_rate['fast'] = fuzz.trapmf(heart_rate.universe, [80, 100, 140, 140])

    oxygen_level['low'] = fuzz.trapmf(oxygen_level.universe, [70, 70, 85, 90])
    oxygen_level['normal'] = fuzz.trapmf(oxygen_level.universe, [85, 90, 100, 100])

    risk['low'] = fuzz.trimf(risk.universe, [0, 25, 50])
    risk['medium'] = fuzz.trimf(risk.universe, [25, 50, 75])
    risk['high'] = fuzz.trimf(risk.universe, [50, 75, 100])

    # Правила
    rule1 = ctrl.Rule(temperature['high'] & blood_pressure['low'], risk['high'])
    rule2 = ctrl.Rule(temperature['normal'] & heart_rate['normal'], risk['low'])
    rule3 = ctrl.Rule(oxygen_level['low'], risk['high'])
    rule4 = ctrl.Rule(blood_pressure['high'] & heart_rate['fast'], risk['medium'])

    # Контролер
    risk_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4])
    risk_simulation = ctrl.ControlSystemSimulation(risk_ctrl)

    # Вхідні значення
    risk_simulation.input['temperature'] = temp
    risk_simulation.input['blood_pressure'] = pressure
    risk_simulation.input['heart_rate'] = pulse
    risk_simulation.input['oxygen_level'] = spo2

    # Розрахунок
    risk_simulation.compute()
    return risk_simulation.output['risk']

# Ендпоінти

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
@app.route('/diagnose', methods=['POST'])
def diagnose():
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')
    temp = data.get('temperature')
    pressure = data.get('pressure')
    pulse = data.get('pulse')
    spo2 = data.get('spo2')

    # Перевірка наявності всіх параметрів
    if None in [name, age, temp, pressure, pulse, spo2]:
        return jsonify({"error": "Missing data"}), 400

    # Нечітка логіка
    risk_score = fuzzy_diagnose(temp, pressure, pulse, spo2)

    # Класифікація рівня ризику
    if risk_score < 33:
        risk_level = 'Low'
    elif 33 <= risk_score < 66:
        risk_level = 'Medium'
    else:
        risk_level = 'High'

    # Збереження в базу даних
    record = HealthData(
        name=name,
        age=age,
        temperature=temp,
        pressure=pressure,
        pulse=pulse,
        spo2=spo2,
        risk_level=risk_level
    )
    db.session.add(record)
    db.session.commit()

    return jsonify({
        'name': name,
        'age': age,
        'temperature': temp,
        'pressure': pressure,
        'pulse': pulse,
        'spo2': spo2,
        'risk_level': risk_level
    })
@app.route('/history', methods=['GET'])
def history():
    records = HealthData.query.all()
    return jsonify([{
        'id': r.id,
        'name': r.name,
        'age': r.age,
        'temperature': r.temperature,
        'pressure': r.pressure,
        'pulse': r.pulse,
        'spo2': r.spo2,
        'risk_level': r.risk_level,
        'created_at': r.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for r in records])

@app.route('/history/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    record = HealthData.query.get(record_id)
    if record:
        db.session.delete(record)
        db.session.commit()
        return jsonify({"message": "Record deleted successfully"}), 200
    else:
        return jsonify({"error": "Record not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
