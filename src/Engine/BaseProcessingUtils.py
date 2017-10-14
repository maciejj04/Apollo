class BaseProcessingUtils:

    def getHighestFrequency(self, data):
        pass

    def findLoudestFrequency(self, list):  # arg type has to be regular (non numpy type) list
        max = 0
        for x in range(0, len(list)):
            if list[x] > max:
                max = list[x]
    
        return list.index(max)
