
def recommend_fertilizer(n, p, k):
    recommendations = []
    if n < 50:
        recommendations.append("Add Urea (Nitrogen)")
    if p < 50:
        recommendations.append("Add DAP (Phosphorus)")
    if k < 50:
        recommendations.append("Add MOP (Potassium)")
    return recommendations
