from bson import ObjectId


class QnAModel:
    def __init__(self, influencer_id, sample_question, sample_answer):
        if type(influencer_id) != str:
            raise TypeError("Invalid influencer_id format")
        if type(sample_question) != str:
            raise TypeError("Invalid sample_question format")
        if type(sample_answer) != str:
            raise TypeError("Invalid sample_answer format")

        self.influencer_id = ObjectId(influencer_id)
        self.sample_question = sample_question
        self.sample_answer = sample_answer
