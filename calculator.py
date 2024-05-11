class GradeCalculator:
    def __init__(self, best_score=100):
        self.best_score = best_score

    # This part is responsible for calculating the scores, and it will give the grades depending on the score of each student
    def calculate_grade(self, score):
        if score >= self.best_score - 10:
            return 'A'
        elif score >= self.best_score - 20:
            return 'B'
        elif score >= self.best_score - 30:
            return 'C'
        elif score >= self.best_score - 40:
            return 'D'
        else:
            return 'F'
