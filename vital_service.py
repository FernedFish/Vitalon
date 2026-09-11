class VitalService:

    @staticmethod
    
    def assess_vitals(temp,heart_rate):
        if temp >= 38 or heart_rate >= 120:
            return "Severe"
        if temp < 36 or heart_rate < 60:
            return "Low"
        return "Normal"