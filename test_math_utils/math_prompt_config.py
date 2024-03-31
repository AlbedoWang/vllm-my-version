MATH_INSTRUCTION_PROMPT = """
Solve a math problem with thought, action, and observation steps. Thought can reason about the current situation, Action will be one of the following funcitons:
1. Add[a,b,c, ...]: calculate add, and result == a + b + c + ...
2. Subtract[a,b]: calculate subtract, and result == a - b
3. Multiply[a,b,c, ...]: calculate multiply, and result == a * b * c * ...
4. Divide[a,b]: calculate divide, and result == a / b
5. Finish[answer]: use Finish[answer] to finish the task.
And Observation will be the result of the action.
Here are some examples.
"""


REACT_MATH_PROMPT = """
Question: Mark has 3 tanks for pregnant fish. Each tank has 4 pregnant fish and each fish gives birth to 20 young. How many young fish does he have at the end?
Thought 1: I need to calculate the number of pregnant fish first. Then I can calculate the number of young fish. Mark has 4*3=Multiply[4,3] pregnant fish. I need to compute Multiply[4,3].
Action 1: Multiply[4,3]
Observation 1: The result is 12. 
Thought 2: Now I can calculate the number of young fish. They give birth to 12*20=Multiply[12,20] fish. I need to compute Multiply[12,20].
Action 2: Multiply[12,20]
Observation 2: The result is 240. 
Thought 3: The question is asking for the number of young fish, the result is 240.
Action 3: Finish[240]
Observation 3: Stopped.
Question: The math questions in a contest are divided into three rounds: easy, average, and hard. There are corresponding points given for each round. That is 2, 3, and 5 points for every correct answer in the easy, average, and hard rounds, respectively. Suppose Kim got 6 correct answers in the easy; 2 correct answers in the average; and 4 correct answers in the difficult round, what are her total points in the contest?
Thought 1: I need to calculate the points for each round first. Then I can calculate the total points. Kim got 6 points/round x 2 round = Multiply[6,2] points in the easy round. I need to compute Multiply[6,2].
Action 1: Multiply[6,2]
Observation 1: The result is 12.
Thought 2: Kim got 2 points/round x 3 rounds = Multiply[2,3] points in the average round. I need to compute Multiply[2,3].
Action 2: Multiply[2,3]
Observation 2: The result is 6.
Thought 3: Kim got 4 points/round x 5 rounds = Multiply[4,5] points in the difficult round. I need to compute Multiply[4,5].
Action 3: Multiply[4,5]
Observation 3: The result is 20.
Thought 4: So her total points is 12 points + 6 points + 20 points = Add[12,6,20] points. I need to compute Add[12,6,20].
Action 4: Add[12,6,20]
Observation 4: The result is 38.
Thought 5: The question is asking for her total points, the result is 38.
Action 5: Finish[38]
Observation 5: Stopped.
Question: Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May? 
Thought 1: I need to calculate the number of clips sold in May first. Then I can calculate the number of clips sold in April. Natalia sold 48/2=Divide[48,2] clips in May. I need to compute Divide[48,2].
Action 1: Divide[48,2]
Observation 1: The result is 24.
Thought 2: Now I can calculate the number of clips sold in April. Natalia sold 48+24=Add[48,24] clips altogether in April and May. I need to compute Add[48,24].
Action 2: Add[48,24]
Observation 2: The result is 72.
Thought 3: The question is asking for the number of clips sold, the result is 72.
Action 3: Finish[72]
Observation 3: Stopped.
Question: Julia just adopted a puppy for $20.00 from the local pet shelter.  Before she brings the puppy home, she needs to buy a bag of dog food for $20.00, 2 bags of treats for $2.50 a bag, an assortment box of toys for $15.00, a crate and a bed for $20.00 each, and the collar/leash combo for $15.00. The store offered Julia a 20% new-customer discount.  How much will Julia spend on the new puppy?
Thought 1: I need to calculate the total amount she will spend in the store first. Then I can calculate the amount she will save. And then calculate how much Julia spend. In the store Julia buy a bag of dog food, the cost is 1*20.00=Multiply[1,20.00]. I need to compute Multiply[1,20.00].
Action 1: Multiply[1,20.00]
Observation 1: The result is 20.00.
Thought 2: In the store Julia buy 2 bags of treats, the cost is 2*2.50=Multiply[2,2.50]. I need to compute Multiply[2,2.50].
Action 2: Multiply[2,2.50]
Observation 2: The result is 5.00.
Thought 3: In the store Julia buy an assortment box of toys, the cost is 1*15.00=Multiply[1,15.00]. I need to compute Multiply[1,15.00].
Action 3: Multiply[1,15.00]
Observation 3: The result is 15.00.
Thought 4: In the store Julia buy a crate and a bed, the cost is 2*20.00=Multiply[2,20.00]. I need to compute Multiply[2,20.00].
Action 4: Multiply[2,20.00]
Observation 4: The result is 40.00.
Thought 5: In the store Julia buy the collar/leash combo, the cost is 1*15.00=Multiply[1,15.00]. I need to compute Multiply[1,15.00].
Action 5: Multiply[1,15.00]
Observation 5: The result is 15.00.
Thought 6: So the total amount she will spend in the store is 20.00+5.00+15.00+40.00+15.00=Add[20.00,5.00,15.00,40.00,15.00]. I need to compute Add[20.00,5.00,15.00,40.00,15.00].
Action 6: Add[20.00,5.00,15.00,40.00,15.00]
Observation 6: The result is 95.00.
Thought 7: And she will get a 20% discount, so the money she can save is 95.00*0.2=Multiply[95.00,0.2]. I need to compute Multiply[95.00,0.2].
Action 7: Multiply[95.00,0.2]
Observation 7: The result is 19.00.
Thought 8: So the total amount she will spend in the store is 95.00-19.00=Subtract[95.00,19.00]. I need to compute Subtract[95.00,19.00].
Action 8: Subtract[95.00,19.00]
Observation 8: The result is 76.00.
Thought 9: So the total amount she will spend on the new puppy is 20.00+76.00=Add[20.00,76.00]. I need to compute Add[20.00,76.00].
Action 9: Add[20.00,76.00]
Observation 9: The result is 96.00.
Thought 10: The question is asking for the total amount she will spend on the new puppy, the result is 96.00.
Action 10: Finish[96.00]
Observation 10: Stopped.
"""


MATH_SPECULATIVE_INSTRUCTION_PROMPT="""
Answer the following questions with <add>, <subtract>, <multiply>, <divide> operators. Here are some examples.

Question: Mark has 3 tanks for pregnant fish. Each tank has 4 pregnant fish and each fish gives birth to 20 young. How many young fish does he have at the end?
Answer: He has 4*3=<multiply>(4, 3)=12 pregnant fish They give birth to 12*20=<multiply>(12, 20)=240 fish. The answer is 240. ###

Question: The math questions in a contest are divided into three rounds: easy, average, and hard. There are corresponding points given for each round. That is 2, 3, and 5 points for every correct answer in the easy, average, and hard rounds, respectively. Suppose Kim got 6 correct answers in the easy; 2 correct answers in the average; and 4 correct answers in the difficult round, what are her total points in the contest? 
Answer: Kim got 6 points/round x 2 round = <multiply>(6,2)=12 points in the easy round. She got 2 points/round x 3 rounds = <multiply>(2,3)=6 points in the average round. She got 4 points/round x 5 rounds = <multiply>(4,5)=20 points in the difficult round. So her total points is 12 points + 6 points + 20 points = <add>(12,6,20)=38 points. The answer is 38. ###

Question: A clothing store sells 20 shirts and 10 pairs of jeans. A shirt costs $10 each and a pair of jeans costs twice as much. How much will the clothing store earn if all shirts and jeans are sold?
Answer: Twenty shirts amount to $10 x 20 = $<multiply>(10, 20)=200. The cost of each pair of jeans is 10 x 2 = <multiply>(10,2)=20. So 10 pairs of jeans amount to 20 x 10 = <multiply>(20,10)=200. Therefore, the store will earn 200 + 200 = <add>(200,200)=400 if all shirts and jeans are sold. The answer is 400. ###
Question: Arnold’s collagen powder has 18 grams of protein for every 2 scoops. His protein powder has 21 grams of protein per scoop. And his steak has 56 grams of protein. If he has 1 scoop of collagen powder, 1 scoop of protein powder and his steak, how many grams of protein will he consume?
Answer: 2 scoops of collagen powder have 18 grams of protein and he only has 1 scoop so he consumes 18/2 = <divide>(18,2)=9 grams of protein He has 9 grams collagen powder, 21 grams of protein powder and 56 grams in his steak for a total of 9+21+56 = <add>(9,21,56)=86 grams of protein. The answer is 86. ###
"""


ENHANCED_MATH_INSTRUCTION_PROMPT = """
Solve a math problem with thought, action, and observation steps. Thought can reason about the current situation, Action will be one of the following funcitons:
1. Add[a,b,c, ...]: calculate add, and result == a + b + c + ...
2. Subtract[a,b]: calculate subtract, and result == a - b
3. Multiply[a,b,c, ...]: calculate multiply, and result == a * b * c * ...
4. Divide[a,b]: calculate divide, and result == a / b
5. Finish[answer]: use Finish[answer] to finish the task.
And Observation will be the result of the action.
Here are some examples.
"""

ENHANCED_REACT_MATH_PROMPT = """
Question: Mark has 3 tanks for pregnant fish. Each tank has 4 pregnant fish and each fish gives birth to 20 young. How many young fish does he have at the end?
Reference: Multiply[4,3]=12, Multiply[12,20]=240
Thought 1: I need to calculate the number of pregnant fish first. Then I can calculate the number of young fish. Mark has 4*3=Multiply[4,3] pregnant fish. The result of Multiply[4,3]=12 is given in the reference. Now I can calculate the number of young fish. They give birth to 12*20=Multiply[12,20] fish. The result of Multiply[12,20]=240 is given in the reference. The question is asking for the number of young fish, the result is 240.
Action 1: Finish[240]
Observation 3: Stopped.
Question: The math questions in a contest are divided into three rounds: easy, average, and hard. There are corresponding points given for each round. That is 2, 3, and 5 points for every correct answer in the easy, average, and hard rounds, respectively. Suppose Kim got 6 correct answers in the easy; 2 correct answers in the average; and 4 correct answers in the difficult round, what are her total points in the contest?
Reference: Multiply[6,2]=12, Multiply[4,5]=20, Add[12,6,20]=38
Thought 1: I need to calculate the points for each round first. Then I can calculate the total points. Kim got 6 points/round x 2 round = Multiply[6,2] points in the easy round. The result of Multiply[6,2]=12 is given in the reference. Kim got 2 points/round x 3 rounds = Multiply[2,3] points in the average round. I can not find the result of Multiply[2,3] in the reference. I need to calculate the result.
Action 1: Multiply[2,3]
Observation 1: The result is 6.
Thought 2: Kim got 4 points/round x 5 rounds = Multiply[4,5] points in the difficult round. The result of Multiply[4,5]=20 is given in the reference. So her total points is 12 points + 6 points + 20 points = Add[12,6,20] points. The result of Add[12,6,20]=38 is given in the reference. The question is asking for her total points, the result is 38.
Action 2: Finish[38]
Observation 2: Stopped.
Question: Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May? 
Reference: Add[48,24]=72
Thought 1: I need to calculate the number of clips sold in May first. Then I can calculate the number of clips sold in April. Natalia sold 48/2=Divide[48,2] clips in May. I can not find the result of Divide[48,2] in the reference. I need to calculate the result.
Action 1: Divide[48,2]
Observation 1: The result is 24.
Thought 2: Now I can calculate the number of clips sold in April. Natalia sold 48+24=Add[48,24] clips altogether in April and May. The result of Add[48,24]=72 is given in the reference. The question is asking for the number of clips sold, the result is 72.
Action 2: Finish[72]
Observation 2: Stopped.
Question: Julia just adopted a puppy for $20.00 from the local pet shelter.  Before she brings the puppy home, she needs to buy a bag of dog food for $20.00, 2 bags of treats for $2.50 a bag, an assortment box of toys for $15.00, a crate and a bed for $20.00 each, and the collar/leash combo for $15.00. The store offered Julia a 20% new-customer discount.  How much will Julia spend on the new puppy?
Reference: Multiply[1,20.00]=20.00, Multiply[2,2.50]=5.00, Multiply[1,15.00]=15.00, Multiply[2,20.00]=40.00
Thought 1: I need to calculate the total amount she will spend in the store first. Then I can calculate the amount she will save. And then calculate how much Julia spend. In the store Julia buy a bag of dog food, the cost is 1*20.00=Multiply[1,20.00]. The result of Multiply[1,20.00]=20.00 is given in the reference. In the store Julia buy 2 bags of treats, the cost is 2*2.50=Multiply[2,2.50]. The result of Multiply[2,2.50]=5.00 is given in the reference. In the store Julia buy an assortment box of toys, the cost is 1*15.00=Multiply[1,15.00]. The result of Multiply[1,15.00]=15.00 is given in the reference. In the store Julia buy the collar/leash combo, the cost is 1*15.00=Multiply[1,15.00]. The result of Multiply[1,15.00]=15.00 is given in the reference. So the total amount she will spend in the store is 20.00+5.00+15.00+40.00+15.00=Add[20.00,5.00,15.00,40.00,15.00]. I can not find the result of Add[20.00,5.00,15.00,40.00,15.00] in the reference. I need to calculate the result.
Action 1: Add[20.00,5.00,15.00,40.00,15.00]
Observation 1: The result is 95.00.
Thought 2: And she will get a 20% discount, so the money she can save is 95.00*0.2=Multiply[95.00,0.2]. I can not find the result of Multiply[95.00,0.2] in the reference. I need to calculate the result.
Action 2: Multiply[95.00,0.2]
Observation 2: The result is 19.00.
Thought 3: So the total amount she will spend in the store is 95.00-19.00=Subtract[95.00,19.00]. I can not find the result of Subtract[95.00,19.00] in the reference. I need to calculate the result.
Action 3: Subtract[95.00,19.00]
Observation 3: The result is 76.00.
Thought 4: So the total amount she will spend on the new puppy is 20.00+76.00=Add[20.00,76.00]. I can not find the result of Add[20.00,76.00] in the reference. I need to calculate the result.
Action 4: Add[20.00,76.00]
Observation 4: The result is 96.00.
Thought 5: The question is asking for the total amount she will spend on the new puppy, the result is 96.00.
Action 5: Finish[96.00]
Observation 5: Stopped.
"""

ENHANCED_REACT_MATH_PROMPT_SHORT = """
Question: Mark has 3 tanks for pregnant fish. Each tank has 4 pregnant fish and each fish gives birth to 20 young. How many young fish does he have at the end?
Reference: Multiply[4,3]=12, Multiply[12,20]=240
Thought 1: I need to calculate the number of pregnant fish first. Then I can calculate the number of young fish. Mark has 4*3=Multiply[4,3] pregnant fish. From Reference get Multiply[4,3]=12. Now I can calculate the number of young fish. They give birth to 12*20=Multiply[12,20] fish. From Reference get Multiply[12,20]=240.
Action 1: Finish[240]
Observation 3: Stopped.
Question: The math questions in a contest are divided into three rounds: easy, average, and hard. There are corresponding points given for each round. That is 2, 3, and 5 points for every correct answer in the easy, average, and hard rounds, respectively. Suppose Kim got 6 correct answers in the easy; 2 correct answers in the average; and 4 correct answers in the difficult round, what are her total points in the contest?
Reference: Multiply[6,2]=12, Multiply[4,5]=20, Add[12,6,20]=38
Thought 1: I need to calculate the points for each round first. Then I can calculate the total points. Kim got 6 points/round x 2 round = Multiply[6,2] points in the easy round. From Reference get Multiply[6,2]=12. Kim got 2 points/round x 3 rounds = Multiply[2,3] points in the average round. No Multiply[2,3] in Reference.
Action 1: Multiply[2,3]
Observation 1: The result is 6.
Thought 2: Kim got 4 points/round x 5 rounds = Multiply[4,5] points in the difficult round. From Reference get Multiply[4,5]=20. So her total points is 12 points + 6 points + 20 points = Add[12,6,20] points. From Reference get Add[12,6,20]=38.
Action 2: Finish[38]
Observation 2: Stopped.
Question: Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May? 
Reference: Add[48,24]=72
Thought 1: I need to calculate the number of clips sold in May first. Then I can calculate the number of clips sold in April. Natalia sold 48/2=Divide[48,2] clips in May. No Divide[48,2] in Reference.
Action 1: Divide[48,2]
Observation 1: The result is 24.
Thought 2: Now I can calculate the number of clips sold in April. Natalia sold 48+24=Add[48,24] clips altogether in April and May. From Reference get Add[48,24]=72.
Action 2: Finish[72]
Observation 2: Stopped.
Question: Julia just adopted a puppy for $20.00 from the local pet shelter.  Before she brings the puppy home, she needs to buy a bag of dog food for $20.00, 2 bags of treats for $2.50 a bag, an assortment box of toys for $15.00, a crate and a bed for $20.00 each, and the collar/leash combo for $15.00. The store offered Julia a 20% new-customer discount.  How much will Julia spend on the new puppy?
Reference: Multiply[1,20.00]=20.00, Multiply[2,2.50]=5.00, Multiply[1,15.00]=15.00, Multiply[2,20.00]=40.00
Thought 1: I need to calculate the total amount she will spend in the store first. Then I can calculate the amount she will save. And then calculate how much Julia spend. In the store Julia buy a bag of dog food, the cost is 1*20.00=Multiply[1,20.00]. From Reference get Multiply[1,20.00]=20.00. In the store Julia buy 2 bags of treats, the cost is 2*2.50=Multiply[2,2.50]. From Reference get Multiply[2,2.50]=5.00. In the store Julia buy an assortment box of toys, the cost is 1*15.00=Multiply[1,15.00]. From Reference get Multiply[1,15.00]=15.00. In the store Julia buy the collar/leash combo, the cost is 1*15.00=Multiply[1,15.00]. From Reference get Multiply[1,15.00]=15.00. So the total amount she will spend in the store is 20.00+5.00+15.00+40.00+15.00=Add[20.00,5.00,15.00,40.00,15.00]. No Add[20.00,5.00,15.00,40.00,15.00] in Reference.
Action 1: Add[20.00,5.00,15.00,40.00,15.00]
Observation 1: The result is 95.00.
Thought 2: And she will get a 20% discount, so the money she can save is 95.00*0.2=Multiply[95.00,0.2]. No Multiply[95.00,0.2] in Reference.
Action 2: Multiply[95.00,0.2]
Observation 2: The result is 19.00.
Thought 3: So the total amount she will spend in the store is 95.00-19.00=Subtract[95.00,19.00]. No Subtract[95.00,19.00] in Reference.
Action 3: Subtract[95.00,19.00]
Observation 3: The result is 76.00.
Thought 4: So the total amount she will spend on the new puppy is 20.00+76.00=Add[20.00,76.00]. No Add[20.00,76.00] in Reference.
Action 4: Add[20.00,76.00]
Observation 4: The result is 96.00.
Thought 5: The question is asking for the total amount she will spend on the new puppy, the result is 96.00.
Action 5: Finish[96.00]
Observation 5: Stopped.
"""







# """
# 5. power:use power(a, b, c, ...) and result == a ** b ** c ** ...
# 6. square root: sqrt(a)
# 7. 10th log: log(a) or log(a, base)
# 8. natural log: ln(a)
# 9. choose: use choose(n, r) and result == C(n, r)
# 10. permutation: permutate(n, r) and result == P(n, r)
# 11. greatest common divisor: gcd(a, b, c, ...) and result == gcd(a, b, c, ...)
# 12. least common multiple: lcm(a, b, c, ...) and result == lcm(a, b, c, ...)
# 13. remainder: remainder(a, b) and result == a mod b
# 14. Finish[answer]: use Finish[answer] to finish the task.
# """
GSM8K_XL_PROMPT_SINGLESTEP = """
Question:Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May? 
Thought: Let's think step by step. Natalia sold result[0] = divide[48, 2] clips in May.\nNatalia sold result[1] = add[48, result[0]] clips altogether in April and May.
Action 1: result[0] = divide[48, 2]
Action 2: result[1] = add[48, result[0]]
Action 3: result[2] = Finish[result[1]]
Observation: Stopped.
Question: James creates a media empire.  He creates a movie for $2000.  Each DVD cost $6 to make.  He sells it for 2.5 times that much.  He sells 500 movies a day for 5 days a week.  How much profit does he make in 20 weeks?
Thought: Let's think step by step. He sold each DVD for result[0] = multiply[6, 2.5]\nSo for each DVD he has a profit of result[1] = subtract[result[0], 6]\nAnd he sells 500 movies a day for 5 days a week for 20 weeks. So he sells result[2] = multiply[500, 5, 20] movies\nSo the total profit he has for all the DVDs is result[3] = multiply[result[2], result[1]]\nHe also spent $2000 to create the movie. So his total profit is result[4] = subtract[result[3], 2000]\n
Action 1: result[0] = multiply[6, 2.5]
Action 2: result[1] = subtract[result[0], 6]
Action 3: result[2] = multiply[500, 5, 20]
Action 4: result[3] = multiply[result[2], result[1]]
Action 5: result[4] = subtract[result[3], 2000]
Action 6: result[5] = Finish[result[4]]
Observation: Stopped.
Question: A king gets a crown made that costs $20,000.  He tips the person 10%.  How much did the king pay after the tip?
Thought: Let's think step by step. The king paid result[0] = multiply[20000, 0.1] as tip.\nSo the king paid result[1] = add[20000, result[0]] after the tip.
Action 1: result[0] = multiply[20000, 0.1]
Action 2: result[1] = add[20000, result[0]]
Action 3: result[2] = Finish[result[1]]
Observation: Stopped.
Question: Julia just adopted a puppy for $20.00 from the local pet shelter.  Before she brings the puppy home, she needs to buy a bag of dog food for $20.00, 2 bags of treats for $2.50 a bag, an assortment box of toys for $15.00, a crate and a bed for $20.00 each, and the collar/leash combo for $15.00.  The store offered Julia a 20% new-customer discount.  How much will Julia spend on the new puppy?
Thought: Julia has already paid result[0] = 20.00, and to get the money she will pay in the store, I should accumulate bag of dog food result[1] = 20.00, 2 bags of treats result[2] = multiply[2, 2.5], an assortment box of toys result[3] = 15.00, a crate and a bed result[4] = multiply[2, 20.00], and the collar/leash combo result[5] = 15.00. So the total amount she will spend in store is result[6] = add[result[1], result[2], result[3], result[4], result[5]]\nAnd she will get a 20% discount, so the money she can save is result[7] = multiply[result[6], 0.2]\nSo the total amount she will spend in the store is result[8] = subtract[result[6], result[7]]\n. So the total amount she will spend on the new puppy is result[9] = add[result[0], result[8]]\n
Action 1: result[0] = 20.00
Action 2: result[1] = multiply[2, 2.5]
Action 3: result[2] = 15.00
Action 4: result[3] = multiply[2, 20.00]
Action 5: result[4] = 15.00
Action 6: result[5] = add[result[1], result[2], result[3], result[4]]
Action 7: result[6] = multiply[result[5], 0.2]
Action 8: result[7] = subtract[result[5], result[6]]
Action 9: result[8] = add[result[0], result[7]]
Action 10: result[9] = Finish[result[8]]
Observation: Stopped.
Question: Parker and Richie split a sum of money in the ratio 2:3. If Parker got $50 (which is the smaller share), how much did they share? 
Thought: Let's think step by step. If Parker got $50 with a ratio of 2, then the unit share is result[0] = divide[50, 2]\nUsing the sharing ratio, Richie gets 3 unit shares which total to result[1] = multiply[3, result[0]]\nThe money they shared was result[2] = add[50, result[1]]\n
Action 1: result[0] = divide[50, 2]
Action 2: result[1] = multiply[3, result[0]]
Action 3: result[2] = add[50, result[1]]
Action 4: result[3] = Finish[result[2]]
Observation: Stopped.
"""
GSM8K_XL_PROMPT_MULTISTEPS = """
You will be given a question, to answer it you will need to perform a series of calculations.
To solve the math problem, you should write the thought, action, and observation steps. Thought can reason about the current situation, Action will be one of the following funcitons, and Observation will be the result of the action and possibly the next step.
1. add: use add(a, b, c, ...) and result == a + b + c + ...
2. subtract: use subtract(a, b) and result == a - b
3. multiply: use multiply(a, b , c ...) and result == a * b * c * ...
4. divide: use divide(a, b) and result == a / b
5. Finish[answer]: use Finish[answer] to finish the task.
Meanwhile, some calculation steps are provided for your reference, and you can directly use the result if you need it.
Here are some examples:
Example 1:
Question: Of the 3 friends, Harry has 4 times as many fish as Joe, and Joe has 8 times as many fish as Sam does. If Sam has 7 fish, how many fish does Harry have?
Reference Steps:
Action 1: result[0] = multiply[4, result[1]]
result[0] = 224.0
Action 2: result[1] = multiply[8, 7]
result[1] = 56.0
Action 3: result[2] = add[result[0], result[1]]
result[2] = 280.0
Action 4: result[3] = Finish[result[2]]
result[3] = 280.0

You should answer:
Thought 1: Let's think step by step. Sam has result 7 fish, so Joe has result[0] = multiply[7, 8] fish, and the reference tells me that result[0] = 56. Now, Harry has result[1] = multiply[result[0], 4] fish, and and the reference tells me that result[1] = 224. The question is asking for the number of fish Harry has, so I can finish now.
Action 1: result[0] = Finish[224]
Observation 1: Stopped.

Example 2:
Question: Parker and Richie split a sum of money in the ratio 2:3. If Parker got $50 (which is the smaller share), how much did they share?
Reference Steps:
Action 1: result[0] = divide[50, 2]
result[0] = 25.0
Action 2: result[1] = multiply[3, 25]
result[1] = 75.0
Action 3: result[2] = add[50, result[1]]
result[2] = 125.0
Action 4: result[3] = Finish[result[2]], result: 125.0
result[3] = 125.0
You should answer:
Thought 1: Let's think step by step. If Parker got $50 with a ratio of 2, then the unit share is result[0] = divide[50, 2], and the reference tells me that result[0] = 25. Using the sharing ratio, Richie gets 3 unit shares which total to result[1] = multiply[3, 25], and the reference tells me that result[1] = 75. The money they shared was result[2] = add[50, 75], and the reference tells me that result[2] = 125. The question is asking for the amount they shared, so I can finish now.
Action 1: result[0] = Finish[125]
Observation 1: Stopped.

Example 3:
Question: After five years, Ron will be four times as old as Maurice. If Ron's age now is 43, how old is Maurice now?
Reference Steps:
Action 1: result[0] = subtract[43, 5]
result[0] = 38
Action 2: result[1] = divide[38, 3]
result[1] = 12.6666666667
Action 3: result[2] = Finish[result[1]]
result[2] = 12.6666666667

You should answer:

Thought 1: Let's think step by step. Ron's age now is 43, so after five years, Ron will be result[0] = add[43, 5] years old
Action 1: result[0] = add[43, 5]
Observation 1: Let's think step by step. Ron's age now is 43, so after five years, Ron will be 48 years old
Action 1: result[0] = 48
Thought 2: After five years, Ron will be four times as old as Maurice, so Maurice's age after five years is result[1] = divide[48, 4]
Action 2: result[1] = divide[48, 4]
Observation 2: After five years, Ron will be four times as old as Maurice, so Maurice's age after five years is result[1] = 12
Thought 3: Maurice's age after five years is 12, so Maurice's age now is result[2] = subtract[12, 5]
Action 3: result[2] = subtract[12, 5]
Observation 3: Maurice's age after five years is 12, so Maurice's age now is result[2] = 7
Thought 4: The question is asking for Maurice's age now, so I can finish now.
Action 4: result[3] = Finish[result[2]]
Observation 4: Stopped.
"""
GSM8K_XL_PROMPT_MULTISTEPS_OLD = """
You will be given a question, to answer it you will need to perform a series of calculations.
To solve the math problem, you should write the thought, action, and observation steps. Thought can reason about the current situation, Action will be one of the following funcitons, and Observation will be the result of the action and possibly the next step.
1. add: use add(a, b, c, ...) and result == a + b + c + ...
2. subtract: use subtract(a, b) and result == a - b
3. multiply: use multiply(a, b , c ...) and result == a * b * c * ...
4. divide: use divide(a, b) and result == a / b
5. Finish[answer]: use Finish[answer] to finish the task.
Meanwhile, you will get a solution from a less capable language model. Some steps are true, and you can directly use the results (calculations are done by hard-coded functions so no calculation fault here).
Here are some examples.
Question: Of the 3 friends, Harry has 4 times as many fish as Joe, and Joe has 8 times as many fish as Sam does. If Sam has 7 fish, how many fish does Harry have?
Small_model:
Thought: Let's think step by step. Harry has 4 times as many fish as Joe, so Harry has result[0] = multiply[4, result[1]] times as many fish as Joe
Joe has 8 times as many fish as Sam, so Joe has result[1] = multiply[8, 7] times as many fish as Sam
So Harry has result[2] = add[result[0], result[1]] times as many fish as Sam

Action 1: result[0] = multiply[4, result[1]]
Action 2: result[1] = multiply[8, 7]
Action 3: result[2] = add[result[0], result[1]]
Action 4: result[3] = Finish[result[2]]

Below are the results of each action, and not the steps you need to take, just for your reference
operation_with_operands: multiply[4, result[1]], result: 224.0
operation_with_operands: multiply[8, 7], result: 56.0
operation_with_operands: add[result[0], result[1]], result: 280.0
operation_with_operands: Finish[result[2]], result: 280.0

Large_model:
Thought 1: Let's think step by step. Sam has result 7 fish, so Joe has result[0] = multiply[7, 8] fish, and small_model has result[0] = 56 fish. Now, Harry has result[1] = multiply[result[0], 4] fish, and small_model has result[1] = 224 fish. The question is asking for the number of fish Harry has, so I can finish now.
Action 1: result[0] = Finish[224]
Observation 1: Stopped.

Question: Parker and Richie split a sum of money in the ratio 2:3. If Parker got $50 (which is the smaller share), how much did they share?
Small_model:
Thought: Let's think step by step. If Parker got $50 with a ratio of 2, then the unit share is result[0] = divide[50, 2]
Using the sharing ratio, Richie gets 3 unit shares which total to result[1] = multiply[3, result[0]]
The money they shared was result[2] = add[50, result[1]]

Action 1: result[0] = divide[50, 2]
Action 2: result[1] = multiply[3, result[0]]
Action 3: result[2] = add[50, result[1]]
Action 4: result[3] = Finish[result[2]]

Below are the results of each action, and not the steps you need to take, just for your reference
operation_with_operands: divide[50, 2], result: 25.0
operation_with_operands: multiply[3, result[0]], result: 75.0
operation_with_operands: add[50, result[1]], result: 125.0
operation_with_operands: Finish[result[2]], result: 125.0

Thought 1: Let's think step by step. If Parker got $50 with a ratio of 2, then the unit share is result[0] = divide[50, 2], and the small model has result[0] = 25. Using the sharing ratio, Richie gets 3 unit shares which total to result[1] = multiply[3, 25], and the small model has result[1] = 75. The money they shared was result[2] = add[50, 75], and the small model has result[2] = 125. The question is asking for the amount they shared, so I can finish now.
Action 1: result[0] = Finish[125]
Observation 1: Stopped.

Question: After five years, Ron will be four times as old as Maurice. If Ron's age now is 43, how old is Maurice now?
Small_model:
Thought: Let's think step by step. Ron's age now is result[0] = 43.
And after five years, Ron will be four times as old as Maurice, so Maurice's age now is result[1] = multiply[4, result[0]]


Action 1: result[0] = 43
Action 2: result[1] = multiply[4, result[0]]
Action 3: result[2] = Finish[result[1]]
Below are the results of each action, and not the steps you need to take, just for your reference
operation_with_operands: 43, result: 43.0
operation_with_operands: multiply[4, result[0]], result: 172.0
operation_with_operands: Finish[result[1]], result: 172.0

Large_model:
Thought 1: Let's think step by step. Ron's age now is 43, so after five years, Ron will be result[0] = add[43, 5] years old
Action 1: result[0] = add[43, 5]
Observation 1: Let's think step by step. Ron's age now is 43, so after five years, Ron will be 48 years old
Action 1: result[0] = 48
Thought 2: After five years, Ron will be four times as old as Maurice, so Maurice's age after five years is result[1] = divide[48, 4]
Action 2: result[1] = divide[48, 4]
Observation 2: After five years, Ron will be four times as old as Maurice, so Maurice's age after five years is result[1] = 12
Thought 3: Maurice's age after five years is 12, so Maurice's age now is result[2] = subtract[12, 5]
Action 3: result[2] = subtract[12, 5]
Observation 3: Maurice's age after five years is 12, so Maurice's age now is result[2] = 7
Thought 4: The question is asking for Maurice's age now, so I can finish now.
Action 4: result[3] = Finish[result[2]]
Observation 4: Stopped.

Question: Colin ran his first mile in 6 minutes.  He ran his next two miles in 5 minutes each and finished his 4th mile in 4 minutes.  What was the average time it took him to run a mile? 
Small_model:
Action 1: result[0] = 6
Action 2: result[1] = 5
Action 3: result[2] = 5
Action 4: result[3] = 4
Action 5: result[4] = add[result[0], result[1], result[2], result[3]]
Action 6: result[5] = divide[result[4], 4]
Action 7: result[6] = Finish[result[5]]

Below are the results of each action, and not the steps you need to take, just for your reference
operation_with_operands: 6, result: 6.0
operation_with_operands: 5, result: 5.0
operation_with_operands: 5, result: 5.0
operation_with_operands: 4, result: 4.0
operation_with_operands: add[result[0], result[1], result[2], result[3]], result: 20.0
operation_with_operands: divide[result[4], 4], result: 5.0
operation_with_operands: Finish[result[5]], result: 5.0

Large_model:
Thought 1: Let's think step by step. Colin ran his first mile in 6 minutes, his next two miles in 5 minutes each, and his 4th mile in 4 minutes. So the total time he took to run 4 miles is result[0] = add[6, 5, 5, 4] minutes, and the small model has result[0] = 20 minutes. The question is asking for the average time it took him to run a mile, so the average time is result[1] = divide[20, 4] minutes, and the small model has result[1] = 5 minutes. I can finish now.
Action 1: result[0] = Finish[5]
Observation 1: Stopped.

Question: Mona plays a multiplayer video game on the weekends. She joins groups with four other players to complete objectives in the game. The past weekend, she joined 9 groups. One of the groups included two players she had grouped with before that weekend, and another group included one person she had grouped with before. How many unique players did Mona group with on the video game that weekend?
Small_model:
Thought: Let's think step by step.
Mona grouped with result[0] = 2 players in one group.
She grouped with result[1] = 9 - result[0] unique players in the other groups.
Action 1: result[0] = 2
Action 2: result[1] = 9 - result[0]
Action 3: result[2] = Finish[result[1]]

Below are the results of each action, and not the steps you need to take, just for your reference
operation_with_operands: 2, result: 2.0
operation_with_operands: 9 - result[0], result: 7.0
operation_with_operands: Finish[result[1]], result: 7.0

Large_model:
Thought 1: Let's think step by step. Mona join 9 groups, and each group has 4 players. So she grouped with result[0] = multiply[9, 4] players if we don't consider the players she grouped with before.
Action 1: result[0] = multiply[9, 4]
Observation 1: Let's think step by step. Mona join 9 groups, and each group has 4 players. So she grouped with 36 players if we don't consider the players she grouped with before. 
Thought 2: Now we know that in one of the groups, she grouped with 2 players she had grouped with before, and in another group, she grouped with 1 person she had grouped with before. So in total, she had grouped with result[1] = add[2, 1] players before.
Action 2: result[1] = add[2, 1]
Observation 2: Now we know that in one of the groups, she grouped with 2 players she had grouped with before, and in another group, she grouped with 1 person she had grouped with before. So in total, she had grouped with 3 players before.
Thought 3: So the number of unique players she grouped with on the video game that weekend is result[2] = subtract[result[0], result[1]]
Action 3: result[2] = subtract[result[0], result[1]]
Observation 3: So the number of unique players she grouped with on the video game that weekend is 33
Thought 4: The question is asking for the number of unique players she grouped with on the video game that weekend, so I can finish now.
Action 4: result[3] = Finish[result[2]]
Observation 4: Stopped.

Please Note that while small models can perform multiple actions in a step, large model should only do one action each step to ensure accuracy, your output format is
Thought 1:
Action 1:
"""

GSM8K_XL_PROMPT_SPECULATIVE = """
You will be given a question, to answer it you will need to perform a series of calculations.
Tell me what calculations you need to perform with the format "Action[calculation]".
Here are some examples:
Question:Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May? 
Action 1: result[0] = divide[48, 2]
Action 2: result[1] = add[48, result[0]]
Action 3: Finish[result[1]]
END

Question: James creates a media empire.  He creates a movie for $2000.  Each DVD cost $6 to make.  He sells it for 2.5 times that much.  He sells 500 movies a day for 5 days a week.  How much profit does he make in 20 weeks?
Action 1: result[0] = multiply[6, 2.5]
Action 2: result[1] = subtract[result[0], 6]
Action 3: result[2] = multiply[500, 5, 20]
Action 4: result[3] = multiply[result[2], result[1]]
Action 5: result[4] = subtract[result[3], 2000]
Action 6: Finish[result[4]]
END

Question: A king gets a crown made that costs $20,000.  He tips the person 10%.  How much did the king pay after the tip?
Action 1: result[0] = multiply[20000, 0.1]
Action 2: result[1] = add[20000, result[0]]
Action 3: Finish[result[1]]
END

Question: Julia just adopted a puppy for $20.00 from the local pet shelter.  Before she brings the puppy home, she needs to buy a bag of dog food for $20.00, 2 bags of treats for $2.50 a bag, an assortment box of toys for $15.00, a crate and a bed for $20.00 each, and the collar/leash combo for $15.00.  The store offered Julia a 20% new-customer discount.  How much will Julia spend on the new puppy?
Action 1: result[1] = 20.00
Action 2: result[2] = multiply[2, 2.5]
Action 3: result[3] = 15.00
Action 4: result[4] = multiply[2, 20.00]
Action 5: result[5] = 15.00
Action 6: result[6] = add[result[1], result[2], result[3], result[4], result[5]]
Action 7: result[7] = multiply[result[6], 0.2]
Action 8: result[8] = subtract[result[6], result[7]
Action 9: result[9] = add[result[0], result[8]]
END

Question: Parker and Richie split a sum of money in the ratio 2:3. If Parker got $50 (which is the smaller share), how much did they share?
Action 1: result[0] = divide[50, 2]
Action 2: result[1] = multiply[3, result[0]]
Action 3: result[2] = add[50, result[1]]
END
"""