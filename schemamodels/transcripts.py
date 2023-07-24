from bson import ObjectId


class TranscriptsModel:
    def __init__(self, influencer_id, transcript):
        if type(influencer_id) != str or len(influencer_id) < 1:
            raise TypeError("Invalid influencer_id format")
        if type(transcript) != str or len(transcript) < 1:
            raise TypeError("Invalid transcript format")

        self.influencer_id = ObjectId(influencer_id)
        self.transcript = transcript
