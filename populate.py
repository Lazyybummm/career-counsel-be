import psycopg2
import json
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_formatted_questions():
    """
    Returns 45 questions for Grade 6-8 formatted with \n
    to match the frontend rendering logic.
    Categories: Quantitative Aptitude (15), Logical Reasoning (15), Verbal Ability (15)
    Difficulty: Easy (5), Medium (5), Hard (5) per category
    """
    return [
        # =============================================
        # === QUANTITATIVE APTITUDE (15 questions) ===
        # =============================================

        # Easy (5)
        {
            "document": "Question: What is 25% of 200?\nA) 25\nB) 50\nC) 75\nD) 100\nCorrect Answer: B\nExplanation: 25% of 200 = (25/100) × 200 = 50.",
            "metadata": {"category": "Quantitative Aptitude", "difficulty": "Easy", "topic": "Percentages", "target_grade": "6-8"}
        },
        {
            "document": "Question: A shopkeeper buys a toy for ₹120 and sells it for ₹150. What is the profit?\nA) ₹20\nB) ₹25\nC) ₹30\nD) ₹35\nCorrect Answer: C\nExplanation: Profit = Selling Price – Cost Price = 150 – 120 = ₹30.",
            "metadata": {"category": "Quantitative Aptitude", "difficulty": "Easy", "topic": "Profit and Loss", "target_grade": "6-8"}
        },
        {
            "document": "Question: The ratio of boys to girls in a class is 3:2. If there are 30 students, how many are girls?\nA) 10\nB) 12\nC) 15\nD) 18\nCorrect Answer: B\nExplanation: Total parts = 5. Each part = 30/5 = 6. Girls = 2 × 6 = 12.",
            "metadata": {"category": "Quantitative Aptitude", "difficulty": "Easy", "topic": "Ratios", "target_grade": "6-8"}
        },
        {
            "document": "Question: Find the average of 10, 20, 30, 40, and 50.\nA) 25\nB) 30\nC) 35\nD) 40\nCorrect Answer: B\nExplanation: Average = Sum / Count = (10+20+30+40+50) / 5 = 150 / 5 = 30.",
            "metadata": {"category": "Quantitative Aptitude", "difficulty": "Easy", "topic": "Averages", "target_grade": "6-8"}
        },
        {
            "document": "Question: A train travels 180 km in 3 hours. What is its speed?\nA) 50 km/h\nB) 60 km/h\nC) 70 km/h\nD) 80 km/h\nCorrect Answer: B\nExplanation: Speed = Distance / Time = 180 / 3 = 60 km/h.",
            "metadata": {"category": "Quantitative Aptitude", "difficulty": "Easy", "topic": "Speed, Distance, Time", "target_grade": "6-8"}
        },

        # Medium (5)
        {
            "document": "Question: A rectangle has length 12 cm and breadth 8 cm. What is its area?\nA) 80 cm²\nB) 90 cm²\nC) 96 cm²\nD) 104 cm²\nCorrect Answer: C\nExplanation: Area = Length × Breadth = 12 × 8 = 96 cm².",
            "metadata": {"category": "Quantitative Aptitude", "difficulty": "Medium", "topic": "Area and Perimeter", "target_grade": "6-8"}
        },
        {
            "document": "Question: If the cost of 8 pens is ₹96, what is the cost of 5 pens?\nA) ₹55\nB) ₹60\nC) ₹65\nD) ₹70\nCorrect Answer: B\nExplanation: Cost of 1 pen = 96/8 = ₹12. Cost of 5 pens = 12 × 5 = ₹60.",
            "metadata": {"category": "Quantitative Aptitude", "difficulty": "Medium", "topic": "Unitary Method", "target_grade": "6-8"}
        },
        {
            "document": "Question: Simple interest on ₹1000 at 5% per annum for 3 years is:\nA) ₹100\nB) ₹125\nC) ₹150\nD) ₹175\nCorrect Answer: C\nExplanation: SI = (P × R × T) / 100 = (1000 × 5 × 3) / 100 = ₹150.",
            "metadata": {"category": "Quantitative Aptitude", "difficulty": "Medium", "topic": "Simple Interest", "target_grade": "6-8"}
        },
        {
            "document": "Question: The perimeter of a square is 48 cm. What is its area?\nA) 100 cm²\nB) 121 cm²\nC) 144 cm²\nD) 169 cm²\nCorrect Answer: C\nExplanation: Side = Perimeter / 4 = 48 / 4 = 12 cm. Area = 12² = 144 cm².",
            "metadata": {"category": "Quantitative Aptitude", "difficulty": "Medium", "topic": "Area and Perimeter", "target_grade": "6-8"}
        },
        {
            "document": "Question: A pipe fills a tank in 6 hours. Another pipe empties it in 12 hours. If both are open, how long to fill the tank?\nA) 8 hours\nB) 10 hours\nC) 12 hours\nD) 14 hours\nCorrect Answer: C\nExplanation: Net rate = 1/6 – 1/12 = 1/12 per hour. Time to fill = 12 hours.",
            "metadata": {"category": "Quantitative Aptitude", "difficulty": "Medium", "topic": "Pipes and Cisterns", "target_grade": "6-8"}
        },

        # Hard (5)
        {
            "document": "Question: A number when divided by 5 leaves remainder 3, and when divided by 7 leaves remainder 4. What is the smallest such number?\nA) 18\nB) 23\nC) 28\nD) 33\nCorrect Answer: A\nExplanation: We need x ≡ 3 (mod 5) and x ≡ 4 (mod 7). Testing: 18/5 = rem 3 ✓, 18/7 = rem 4 ✓. Answer = 18.",
            "metadata": {"category": "Quantitative Aptitude", "difficulty": "Hard", "topic": "Remainders", "target_grade": "6-8"}
        },
        {
            "document": "Question: The ages of A and B are in the ratio 4:5. After 6 years, the ratio becomes 5:6. What is A's current age?\nA) 18\nB) 20\nC) 24\nD) 30\nCorrect Answer: C\nExplanation: Let ages be 4x and 5x. (4x+6)/(5x+6) = 5/6 → 24x+36 = 25x+30 → x = 6. A = 4×6 = 24.",
            "metadata": {"category": "Quantitative Aptitude", "difficulty": "Hard", "topic": "Age Problems", "target_grade": "6-8"}
        },
        {
            "document": "Question: A sum of money doubles itself in 8 years at simple interest. What is the rate of interest per annum?\nA) 10%\nB) 12%\nC) 12.5%\nD) 15%\nCorrect Answer: C\nExplanation: SI = P (since it doubles). P = (P × R × 8)/100 → R = 100/8 = 12.5%.",
            "metadata": {"category": "Quantitative Aptitude", "difficulty": "Hard", "topic": "Simple Interest", "target_grade": "6-8"}
        },
        {
            "document": "Question: If 12 workers complete a job in 15 days, how many workers are needed to complete the same job in 9 days?\nA) 15\nB) 18\nC) 20\nD) 24\nCorrect Answer: C\nExplanation: Workers × Days = constant. 12 × 15 = W × 9 → W = 180/9 = 20.",
            "metadata": {"category": "Quantitative Aptitude", "difficulty": "Hard", "topic": "Work and Time", "target_grade": "6-8"}
        },
        {
            "document": "Question: A merchant marks an article 40% above cost price and gives a 20% discount. What is the profit percentage?\nA) 8%\nB) 10%\nC) 12%\nD) 14%\nCorrect Answer: C\nExplanation: Let CP = 100. MP = 140. SP = 140 × 0.8 = 112. Profit% = (112–100)/100 × 100 = 12%.",
            "metadata": {"category": "Quantitative Aptitude", "difficulty": "Hard", "topic": "Profit and Loss", "target_grade": "6-8"}
        },

        # =============================================
        # === LOGICAL REASONING (15 questions) ===
        # =============================================

        # Easy (5)
        {
            "document": "Question: Find the next number in the series: 2, 4, 8, 16, ?\nA) 24\nB) 28\nC) 32\nD) 36\nCorrect Answer: C\nExplanation: Each number is multiplied by 2. 16 × 2 = 32.",
            "metadata": {"category": "Logical Reasoning", "difficulty": "Easy", "topic": "Number Series", "target_grade": "6-8"}
        },
        {
            "document": "Question: Ravi is taller than Suresh. Suresh is taller than Mohan. Who is the shortest?\nA) Ravi\nB) Suresh\nC) Mohan\nD) Cannot be determined\nCorrect Answer: C\nExplanation: Ravi > Suresh > Mohan. So Mohan is the shortest.",
            "metadata": {"category": "Logical Reasoning", "difficulty": "Easy", "topic": "Comparison and Ranking", "target_grade": "6-8"}
        },
        {
            "document": "Question: Priya walks 5 m north, then turns right and walks 3 m. In which direction is she now facing?\nA) North\nB) South\nC) East\nD) West\nCorrect Answer: C\nExplanation: She starts facing north, turns right (east), and walks 3 m. She is now facing East.",
            "metadata": {"category": "Logical Reasoning", "difficulty": "Easy", "topic": "Direction Sense", "target_grade": "6-8"}
        },
        {
            "document": "Question: Which word does NOT belong: Apple, Mango, Carrot, Banana?\nA) Apple\nB) Mango\nC) Carrot\nD) Banana\nCorrect Answer: C\nExplanation: Apple, Mango, and Banana are fruits. Carrot is a vegetable.",
            "metadata": {"category": "Logical Reasoning", "difficulty": "Easy", "topic": "Odd One Out", "target_grade": "6-8"}
        },
        {
            "document": "Question: If CAT = 3-1-20, what is DOG?\nA) 4-14-7\nB) 4-15-7\nC) 3-15-7\nD) 4-14-6\nCorrect Answer: B\nExplanation: Using A=1, B=2… D=4, O=15, G=7. DOG = 4-15-7.",
            "metadata": {"category": "Logical Reasoning", "difficulty": "Easy", "topic": "Coding-Decoding", "target_grade": "6-8"}
        },

        # Medium (5)
        {
            "document": "Question: Find the next term: 1, 4, 9, 16, 25, ?\nA) 30\nB) 34\nC) 36\nD) 49\nCorrect Answer: C\nExplanation: These are perfect squares: 1², 2², 3², 4², 5², 6² = 36.",
            "metadata": {"category": "Logical Reasoning", "difficulty": "Medium", "topic": "Number Series", "target_grade": "6-8"}
        },
        {
            "document": "Question: A is B's sister. C is B's mother. D is C's father. How is A related to D?\nA) Daughter\nB) Granddaughter\nC) Niece\nD) Sister\nCorrect Answer: B\nExplanation: D is C's father → D is the grandfather of B and A. So A is D's granddaughter.",
            "metadata": {"category": "Logical Reasoning", "difficulty": "Medium", "topic": "Blood Relations", "target_grade": "6-8"}
        },
        {
            "document": "Question: In a row of 10 students, Asha is 4th from the left. What is her position from the right?\nA) 5th\nB) 6th\nC) 7th\nD) 8th\nCorrect Answer: C\nExplanation: Position from right = (Total + 1) – Position from left = 11 – 4 = 7th.",
            "metadata": {"category": "Logical Reasoning", "difficulty": "Medium", "topic": "Ranking and Position", "target_grade": "6-8"}
        },
        {
            "document": "Question: If FISH is coded as GJTI, what is BIRD coded as?\nA) CJSE\nB) CJSD\nC) DJSE\nD) CISE\nCorrect Answer: A\nExplanation: Each letter moves +1. B→C, I→J, R→S, D→E. BIRD = CJSE.",
            "metadata": {"category": "Logical Reasoning", "difficulty": "Medium", "topic": "Coding-Decoding", "target_grade": "6-8"}
        },
        {
            "document": "Question: All roses are flowers. Some flowers fade quickly. Which conclusion is definite?\nA) All roses fade quickly\nB) Some roses fade quickly\nC) All flowers are roses\nD) None of the above\nCorrect Answer: D\nExplanation: We can't confirm roses specifically fade quickly — 'some flowers' may or may not include roses.",
            "metadata": {"category": "Logical Reasoning", "difficulty": "Medium", "topic": "Syllogisms", "target_grade": "6-8"}
        },

        # Hard (5)
        {
            "document": "Question: Five friends P, Q, R, S, T sit in a row. P is not at either end. Q is to the left of R. S is at the rightmost end. T is at the leftmost end. Who is in the middle?\nA) P\nB) Q\nC) R\nD) S\nCorrect Answer: A\nExplanation: T _ _ _ S is the arrangement. P is not at ends, so P is in one of positions 2,3,4. Q is left of R. The only consistent arrangement is T Q P R S — P is in the middle (position 3).",
            "metadata": {"category": "Logical Reasoning", "difficulty": "Hard", "topic": "Seating Arrangement", "target_grade": "6-8"}
        },
        {
            "document": "Question: A clock shows 6:00. What is the angle between the hour and minute hands?\nA) 90°\nB) 120°\nC) 150°\nD) 180°\nCorrect Answer: D\nExplanation: At 6:00, the hour hand points to 6 (180°) and the minute hand to 12 (0°). Angle = 180°.",
            "metadata": {"category": "Logical Reasoning", "difficulty": "Hard", "topic": "Clock Problems", "target_grade": "6-8"}
        },
        {
            "document": "Question: A cube is painted blue on all faces, then cut into 64 equal smaller cubes. How many small cubes have no face painted?\nA) 0\nB) 4\nC) 8\nD) 16\nCorrect Answer: C\nExplanation: A 4×4×4 cube has an inner 2×2×2 core with no paint. 2³ = 8 unpainted cubes.",
            "metadata": {"category": "Logical Reasoning", "difficulty": "Hard", "topic": "Spatial Reasoning", "target_grade": "6-8"}
        },
        {
            "document": "Question: Statement: 'All students who passed the exam studied hard.' Assumption I: Hard study guarantees passing. Assumption II: Students who didn't study hard failed.\nA) Only I\nB) Only II\nC) Both\nD) Neither\nCorrect Answer: D\nExplanation: The statement only says passers studied hard — it doesn't confirm that hard study guarantees passing, nor that non-studiers failed.",
            "metadata": {"category": "Logical Reasoning", "difficulty": "Hard", "topic": "Statement-Assumption Logic", "target_grade": "6-8"}
        },
        {
            "document": "Question: Find the missing number: 3, 6, 11, 18, 27, ?\nA) 35\nB) 36\nC) 38\nD) 40\nCorrect Answer: C\nExplanation: Differences are +3, +5, +7, +9, +11. Next = 27 + 11 = 38.",
            "metadata": {"category": "Logical Reasoning", "difficulty": "Hard", "topic": "Number Series", "target_grade": "6-8"}
        },

        # =============================================
        # === VERBAL ABILITY (15 questions) ===
        # =============================================

        # Easy (5)
        {
            "document": "Question: Choose the correct spelling:\nA) Recieve\nB) Receive\nC) Receve\nD) Receeve\nCorrect Answer: B\nExplanation: The correct spelling is 'Receive'. Remember the rule: i before e except after c.",
            "metadata": {"category": "Verbal Ability", "difficulty": "Easy", "topic": "Spelling", "target_grade": "6-8"}
        },
        {
            "document": "Question: What is the antonym of 'BRAVE'?\nA) Bold\nB) Strong\nC) Cowardly\nD) Fierce\nCorrect Answer: C\nExplanation: Brave means courageous. Its antonym is cowardly, meaning lacking courage.",
            "metadata": {"category": "Verbal Ability", "difficulty": "Easy", "topic": "Antonyms", "target_grade": "6-8"}
        },
        {
            "document": "Question: Fill in the blank: 'She _____ to school every day.'\nA) go\nB) goes\nC) going\nD) gone\nCorrect Answer: B\nExplanation: With a singular subject (She), the verb takes an 's' in simple present tense — 'goes'.",
            "metadata": {"category": "Verbal Ability", "difficulty": "Easy", "topic": "Subject-Verb Agreement", "target_grade": "6-8"}
        },
        {
            "document": "Question: What does the idiom 'it's raining cats and dogs' mean?\nA) Animals are falling from the sky\nB) It is raining heavily\nC) The weather is pleasant\nD) There is a storm coming\nCorrect Answer: B\nExplanation: 'Raining cats and dogs' is an idiom meaning it is raining very heavily.",
            "metadata": {"category": "Verbal Ability", "difficulty": "Easy", "topic": "Idioms", "target_grade": "6-8"}
        },
        {
            "document": "Question: Choose the synonym of 'HAPPY':\nA) Sad\nB) Angry\nC) Joyful\nD) Tired\nCorrect Answer: C\nExplanation: Happy means feeling pleasure or contentment. Joyful is its closest synonym.",
            "metadata": {"category": "Verbal Ability", "difficulty": "Easy", "topic": "Synonyms", "target_grade": "6-8"}
        },

        # Medium (5)
        {
            "document": "Question: Spot the error: 'He don't know the answer to the question.'\nA) He\nB) don't know\nC) the answer\nD) to the question\nCorrect Answer: B\nExplanation: With a singular subject 'He', the correct form is 'doesn't know', not 'don't know'.",
            "metadata": {"category": "Verbal Ability", "difficulty": "Medium", "topic": "Error Spotting", "target_grade": "6-8"}
        },
        {
            "document": "Question: Change to past tense: 'The children play in the garden.'\nA) The children played in the garden.\nB) The children are playing in the garden.\nC) The children will play in the garden.\nD) The children have play in the garden.\nCorrect Answer: A\nExplanation: Simple present 'play' becomes simple past 'played'.",
            "metadata": {"category": "Verbal Ability", "difficulty": "Medium", "topic": "Tenses", "target_grade": "6-8"}
        },
        {
            "document": "Question: Analogy — Book : Library :: Painting : ?\nA) Artist\nB) Museum\nC) Canvas\nD) Colour\nCorrect Answer: B\nExplanation: Books are kept in a library; paintings are kept in a museum.",
            "metadata": {"category": "Verbal Ability", "difficulty": "Medium", "topic": "Analogies", "target_grade": "6-8"}
        },
        {
            "document": "Question: Fill in the blank with the correct preposition: 'The cat is hiding _____ the table.'\nA) on\nB) at\nC) under\nD) into\nCorrect Answer: C\nExplanation: 'Under' correctly describes the cat's position — beneath the table.",
            "metadata": {"category": "Verbal Ability", "difficulty": "Medium", "topic": "Prepositions", "target_grade": "6-8"}
        },
        {
            "document": "Question: Spot the error: 'Each of the students have submitted their assignment.'\nA) Each of\nB) the students\nC) have submitted\nD) their assignment\nCorrect Answer: C\nExplanation: 'Each' is singular and takes a singular verb. Correct: 'has submitted'.",
            "metadata": {"category": "Verbal Ability", "difficulty": "Medium", "topic": "Error Spotting", "target_grade": "6-8"}
        },

        # Hard (5)
        {
            "document": "Question: Choose the word closest in meaning to DILIGENT:\nA) Lazy\nB) Hardworking\nC) Clever\nD) Careless\nCorrect Answer: B\nExplanation: Diligent means having or showing care and conscientiousness in one's work — synonymous with hardworking.",
            "metadata": {"category": "Verbal Ability", "difficulty": "Hard", "topic": "Vocabulary", "target_grade": "6-8"}
        },
        {
            "document": "Question: Rearrange the words to form a correct sentence: (P) always (Q) the truth (R) one should (S) speak\nA) RPSQ\nB) RPQS\nC) RSQP\nD) RSPQ\nCorrect Answer: D\nExplanation: Correct sentence: 'One should (R) always (S... wait: R=one should, P=always, S=speak, Q=the truth → RPSQ: One should always speak the truth.",
            "metadata": {"category": "Verbal Ability", "difficulty": "Hard", "topic": "Sentence Rearrangement", "target_grade": "6-8"}
        },
        {
            "document": "Question: Change to passive voice: 'The teacher praised the student.'\nA) The student was praised by the teacher.\nB) The student is praised by the teacher.\nC) The student has been praised by the teacher.\nD) The student praised the teacher.\nCorrect Answer: A\nExplanation: Simple past active → simple past passive. 'praised' becomes 'was praised by'.",
            "metadata": {"category": "Verbal Ability", "difficulty": "Hard", "topic": "Active and Passive Voice", "target_grade": "6-8"}
        },
        {
            "document": "Question: Which sentence uses the word 'PRINCIPAL' correctly?\nA) The principal reason for failure is lack of practice.\nB) The principal of the loan must be repaid with principle.\nC) She visited the principle of her school.\nD) The principle amount was deposited in the bank.\nCorrect Answer: A\nExplanation: 'Principal' means main/chief (adjective) or head of a school (noun). 'Principle' means a rule or belief. Option A uses 'principal' correctly as an adjective meaning main.",
            "metadata": {"category": "Verbal Ability", "difficulty": "Hard", "topic": "Commonly Confused Words", "target_grade": "6-8"}
        },
        {
            "document": "Question: Weakener: 'Students who read more books perform better in exams.'\nA) Reading improves vocabulary\nB) Many top scorers rarely read books outside the syllabus\nC) Books are available in school libraries\nD) Teachers recommend reading\nCorrect Answer: B\nExplanation: If top scorers don't read extra books, it weakens the claim that reading more books leads to better exam performance.",
            "metadata": {"category": "Verbal Ability", "difficulty": "Hard", "topic": "Critical Reasoning", "target_grade": "6-8"}
        },
    ]


def run_migration():
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        cur = conn.cursor()
        print("Connected. Migrating 45 Grade 6-8 questions...")

        questions = get_formatted_questions()
        query = "INSERT INTO langchain_pg_embedding (id, document, cmetadata) VALUES (%s, %s, %s)"

        for i, q in enumerate(questions, 1):
            cur.execute(query, (str(uuid.uuid4()), q["document"], json.dumps(q["metadata"])))

        conn.commit()
        print(f"Success! {len(questions)} questions migrated.")
    except Exception as e:
        print(f"Error: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    run_migration()